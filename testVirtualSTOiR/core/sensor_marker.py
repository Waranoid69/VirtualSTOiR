from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsItemGroup
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QRectF

COLOR_MAP = {
    "black":  QColor("#1a1a1a"),
    "yellow": QColor("#f39c12"),
    "red":    QColor("#e74c3c"),
    "gray":   QColor("#95a5a6"),
}

class SensorMarker(QGraphicsItemGroup):
    """
    УГО датчика: окружность с крестом внутри (стандарт ГОСТ для КИП)
    + подпись TAG снизу.
    Цвет меняется в зависимости от даты поверки.
    """
    SIZE = 28  # диаметр кружка

    def __init__(self, tag: str, color: str = "black", parent=None):
        super().__init__(parent)
        self.tag = tag
        self._color_name = color
        self._build(color)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setCursor(Qt.PointingHandCursor)

    def _build(self, color: str):
        # Удаляем старые дочерние элементы
        for child in self.childItems():
            self.removeFromGroup(child)

        qcolor = COLOR_MAP.get(color, COLOR_MAP["black"])
        pen = QPen(qcolor, 2)
        s = self.SIZE
        r = s / 2

        # Окружность
        circle = QGraphicsEllipseItem(-r, -r, s, s)
        circle.setPen(pen)
        circle.setBrush(QBrush(QColor(255, 255, 255, 180)))

        # Крест (КИП-стиль)
        from PyQt5.QtWidgets import QGraphicsLineItem
        line_h = QGraphicsLineItem(-r + 4, 0, r - 4, 0)
        line_v = QGraphicsLineItem(0, -r + 4, 0, r - 4)
        line_h.setPen(pen)
        line_v.setPen(pen)

        # Подпись TAG
        label = QGraphicsTextItem(self.tag)
        font = QFont("Monospace", 7, QFont.Bold)
        label.setFont(font)
        label.setDefaultTextColor(qcolor)
        lw = label.boundingRect().width()
        label.setPos(-lw / 2, r + 2)

        for item in (circle, line_h, line_v, label):
            self.addToGroup(item)

    def set_color(self, color: str):
        self._color_name = color
        self._build(color)

    def to_dict(self) -> dict:
        """Сериализация для сохранения в JSON."""
        return {
            "tag": self.tag,
            "x": self.x(),
            "y": self.y(),
            "color": self._color_name,
        }

    def mouseDoubleClickEvent(self, event):
        """Двойной клик — открыть SensorInfoDialog."""
        self.scene().marker_double_clicked.emit(self.tag)
        super().mouseDoubleClickEvent(event)