import json
from pathlib import Path

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSignal, Qt

from core.sensor_marker import SensorMarker
from core.db import get_sensor_status_color

class SchemaScene(QGraphicsScene):
    marker_double_clicked = pyqtSignal(str)   # передаёт TAG

    def __init__(self):
        super().__init__()
        self._bg_item: QGraphicsPixmapItem | None = None
        self._markers: dict[str, SensorMarker] = {}   # tag → marker
        self._layout_path: Path | None = None
        self._editor_mode = False

    # ------------------------------------------------------------------ #
    #  PDF / фон                                                           #
    # ------------------------------------------------------------------ #
    def load_pdf(self, pdf_path: str) -> bool:
        """Рендерит первую страницу PDF как фоновое изображение."""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(pdf_path)
            page = doc[0]
            mat = fitz.Matrix(2.0, 2.0)   # x2 разрешение
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = QImage(pix.samples, pix.width, pix.height,
                         pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.clear()
            self._markers.clear()
            self._bg_item = self.addPixmap(pixmap)
            self._bg_item.setZValue(-1)
            self.setSceneRect(self._bg_item.boundingRect())
            # Путь к JSON — рядом с PDF, то же имя
            self._layout_path = Path(pdf_path).with_suffix(".json")
            return True
        except ImportError:
            print("Установите PyMuPDF: pip install pymupdf")
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
        """Обновляет цвета всех маркеров по актуальным данным из БД."""
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
    #  Сохранение / загрузка JSON                                          #
    # ------------------------------------------------------------------ #
    def save_layout(self):
        if not self._layout_path:
            return
        data = [m.to_dict() for m in self._markers.values()]
        with open(self._layout_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_layout(self, sensors: list[dict]):
        """Загружает позиции маркеров из JSON и расставляет их на сцене."""
        if not self._layout_path or not self._layout_path.exists():
            return
        color_by_tag = {
            s.get("TAG", ""): get_sensor_status_color(s.get("Дата_поверки", ""))
            for s in sensors
        }
        with open(self._layout_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for entry in data:
            tag = entry["tag"]
            color = color_by_tag.get(tag, entry.get("color", "black"))
            self.add_marker(tag, entry["x"], entry["y"], color)

    # ------------------------------------------------------------------ #
    #  Клик по пустому месту в режиме редактора → добавить маркер          #
    # ------------------------------------------------------------------ #
    def mousePressEvent(self, event):
        if (self._editor_mode
                and event.button() == Qt.LeftButton
                and not self.itemAt(event.scenePos(), __import__('PyQt5.QtGui', fromlist=['QTransform']).QTransform())):
            # Сигнал наверх — MainWindow спросит TAG
            self.add_marker_requested.emit(event.scenePos().x(), event.scenePos().y())
            return
        super().mousePressEvent(event)

    # Дополнительный сигнал для запроса TAG при добавлении
    add_marker_requested = pyqtSignal(float, float)