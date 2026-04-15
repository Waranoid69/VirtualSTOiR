import json
from pathlib import Path

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSignal, Qt

from core.sensor_marker import SensorMarker
from core.db import get_sensor_status_color


class SchemaScene(QGraphicsScene):
    marker_double_clicked = pyqtSignal(str)
    add_marker_requested  = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self._bg_item: QGraphicsPixmapItem | None = None
        self._markers: dict[str, SensorMarker] = {}
        self._layout_path: Path | None = None
        self._editor_mode = False

    # ------------------------------------------------------------------ #
    #  PDF / фон                                                           #
    # ------------------------------------------------------------------ #
    def load_pdf(self, pdf_path: str) -> bool:
        """Рендерит первую страницу PDF в x4 качестве."""
        try:
            import pypdfium2 as pdfium

            doc    = pdfium.PdfDocument(pdf_path)
            page   = doc[0]

            # x4 — очень чёткое изображение
            bitmap    = page.render(scale=6.0, rotation=0)
            pil_image = bitmap.to_pil()

            from io import BytesIO
            buf = BytesIO()
            pil_image.save(buf, format="PNG")
            buf.seek(0)

            pixmap = QPixmap()
            pixmap.loadFromData(buf.read())

            self.clear()
            self._markers.clear()

            self._bg_item = self.addPixmap(pixmap)
            self._bg_item.setZValue(-1)
            # Фоновый элемент не должен перехватывать события мыши
            self._bg_item.setFlag(QGraphicsPixmapItem.ItemIsMovable, False)
            self._bg_item.setFlag(QGraphicsPixmapItem.ItemIsSelectable, False)
            self._bg_item.setAcceptedMouseButtons(Qt.NoButton)

            self.setSceneRect(self._bg_item.boundingRect())
            self._layout_path = Path(pdf_path).with_suffix(".json")
            return True

        except ImportError:
            print("Установите pypdfium2: pip install pypdfium2")
            return False
        except Exception as e:
            print(f"Ошибка загрузки PDF: {e}")
            return False

    # ------------------------------------------------------------------ #
    #  Маркеры                                                             #
    # ------------------------------------------------------------------ #
    def add_marker(self, tag: str, x: float, y: float, color: str = "black"):
        if tag in self._markers:
            return
        marker = SensorMarker(tag, color)
        marker.setPos(x, y)
        marker.setFlag(marker.ItemIsMovable, self._editor_mode)
        self.addItem(marker)
        self._markers[tag] = marker

    def remove_marker(self, tag: str):
        if tag in self._markers:
            self.removeItem(self._markers.pop(tag))

    def update_marker_colors(self, sensors: list[dict]):
        color_by_tag = {
            s.get("TAG", ""): get_sensor_status_color(s.get("Дата_поверки", ""))
            for s in sensors
        }
        for tag, marker in self._markers.items():
            marker.set_color(color_by_tag.get(tag, "gray"))

    def set_editor_mode(self, enabled: bool):
        self._editor_mode = enabled
        for marker in self._markers.values():
            marker.setFlag(marker.ItemIsMovable, enabled)

    # ------------------------------------------------------------------ #
    #  JSON                                                                #
    # ------------------------------------------------------------------ #
    def save_layout(self):
        if not self._layout_path:
            return
        data = [m.to_dict() for m in self._markers.values()]
        with open(self._layout_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_layout(self, sensors: list[dict]):
        if not self._layout_path or not self._layout_path.exists():
            return
        color_by_tag = {
            s.get("TAG", ""): get_sensor_status_color(s.get("Дата_поверки", ""))
            for s in sensors
        }
        with open(self._layout_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for entry in data:
            tag   = entry["tag"]
            color = color_by_tag.get(tag, entry.get("color", "black"))
            self.add_marker(tag, entry["x"], entry["y"], color)

    # ------------------------------------------------------------------ #
    #  События мыши — исправленный клик для добавления маркера            #
    # ------------------------------------------------------------------ #
    def mousePressEvent(self, event):
        if self._editor_mode and event.button() == Qt.LeftButton:
            # Проверяем — кликнули по пустому месту (не по маркеру)
            item = self.itemAt(event.scenePos(), __import__('PyQt5.QtGui', fromlist=['QTransform']).QTransform())
            # Фоновый pixmap не считается — только реальные маркеры
            if item is None or item is self._bg_item or isinstance(item, QGraphicsPixmapItem):
                self.add_marker_requested.emit(
                    event.scenePos().x(),
                    event.scenePos().y()
                )
                event.accept()
                return
        super().mousePressEvent(event)