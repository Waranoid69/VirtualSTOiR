import sqlite3
from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QMessageBox,
    QInputDialog, QGraphicsView
)
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from core.schema_scene import SchemaScene
from core.db import Database
from windows.registry_window import RegistryWindow
from windows.sensor_info_dialog import SensorInfoDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/main_window.ui", self)

        self.db: Database | None = None
        self.registry_window: RegistryWindow | None = None

        # Сцена
        self.scene = SchemaScene()
        self.view = QGraphicsView(self.scene)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # Заменяем scrollArea на QGraphicsView
        self.centralWidget().layout().replaceWidget(self.scrollArea, self.view)
        self.scrollArea.hide()

        self._connect_actions()

    # ------------------------------------------------------------------ #
    #  Подключение сигналов                                                #
    # ------------------------------------------------------------------ #
    def _connect_actions(self):
        # Меню
        self.Load.triggered.connect(self._load_pdf)
        self.ZoomIn.triggered.connect(lambda: self.view.scale(1.2, 1.2))
        self.ZoomOut.triggered.connect(lambda: self.view.scale(1/1.2, 1/1.2))

        # Тулбар
        self.actionOpenReestr.triggered.connect(self._open_registry)
        self.actionUpdate.triggered.connect(self._refresh_markers)
        self.actionEditorMode.toggled.connect(self._toggle_editor_mode)
        self.actionAddSensorPoint.triggered.connect(self._add_sensor_point_manually)

        # Сцена
        self.scene.marker_double_clicked.connect(self._show_sensor_info)
        self.scene.add_marker_requested.connect(self._on_add_marker_requested)

    # ------------------------------------------------------------------ #
    #  БД                                                                  #
    # ------------------------------------------------------------------ #
    def _ensure_db(self) -> bool:
        if self.db:
            return True
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть базу данных", "",
            "SQLite (*.db *.sqlite *.sqlite3);;Все файлы (*)"
        )
        if not path:
            return False
        self.db = Database(path)
        self.statusBar().showMessage(f"БД: {path}")
        return True

    # ------------------------------------------------------------------ #
    #  PDF                                                                 #
    # ------------------------------------------------------------------ #
    def _load_pdf(self):
        if not self._ensure_db():
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Загрузить схему (PDF)", "", "PDF (*.pdf)"
        )
        if not path:
            return
        if not self.scene.load_pdf(path):
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить PDF.\nУстановите: pip install pymupdf")
            return
        sensors = self.db.get_all_sensors()
        self.scene.load_layout(sensors)
        self.statusBar().showMessage(f"Схема: {path}")

    # ------------------------------------------------------------------ #
    #  Реестр                                                              #
    # ------------------------------------------------------------------ #
    def _open_registry(self):
        if not self._ensure_db():
            return
        if self.registry_window is None:
            self.registry_window = RegistryWindow(shared_conn=self.db.conn)
        self.registry_window.show()
        self.registry_window.raise_()

    # ------------------------------------------------------------------ #
    #  Маркеры
#
    # ------------------------------------------------------------------ #
    def _toggle_editor_mode(self, enabled: bool):
        self.scene.set_editor_mode(enabled)
        if enabled:
            self.view.setDragMode(QGraphicsView.NoDrag)
            self.statusBar().showMessage("Режим редактора: кликните на схему чтобы добавить датчик")
        else:
            self.scene.save_layout()
            self.view.setDragMode(QGraphicsView.ScrollHandDrag)
            self.statusBar().showMessage("Расположение сохранено")

    def _add_sensor_point_manually(self):
        """Кнопка в тулбаре — добавить маркер (выбрать TAG из списка)."""
        if not self._ensure_db():
            return
        tags = self.db.get_all_tags()
        if not tags:
            QMessageBox.information(self, "Нет данных", "В базе нет датчиков.")
            return
        tag, ok = QInputDialog.getItem(self, "Добавить датчик", "Выберите TAG:", tags, 0, False)
        if ok and tag:
            self.scene.add_marker(tag, 100, 100)
            self.scene.save_layout()

    def _on_add_marker_requested(self, x: float, y: float):
        """Клик по пустому месту в режиме редактора."""
        if not self._ensure_db():
            return
        tags = self.db.get_all_tags()
        tag, ok = QInputDialog.getItem(self, "Добавить датчик", "Выберите TAG:", tags, 0, False)
        if ok and tag:
            from core.db import get_sensor_status_color
            sensor = self.db.get_sensor_by_tag(tag)
            color = get_sensor_status_color(sensor.get("Дата_поверки", "") if sensor else "")
            self.scene.add_marker(tag, x, y, color)
            self.scene.save_layout()

    def _refresh_markers(self):
        if self.db:
            self.scene.update_marker_colors(self.db.get_all_sensors())

    # ------------------------------------------------------------------ #
    #  SensorInfo                                                          #
    # ------------------------------------------------------------------ #
    def _show_sensor_info(self, tag: str):
        if not self.db:
            return
        sensor = self.db.get_sensor_by_tag(tag)
        if not sensor:
            QMessageBox.warning(self, "Не найдено", f"Датчик с TAG '{tag}' не найден в БД.")
            return
        dlg = SensorInfoDialog(sensor, parent=self)
        result = dlg.exec_()
        # Если нажали "Редактировать" — открываем реестр и прокручиваем к строке
        if result == dlg.Accepted and hasattr(dlg, 'parent_open_registry_tag'):
            self._open_registry()
            if self.registry_window:
                self.registry_window.scroll_to_tag(dlg.parent_open_registry_tag)

    def closeEvent(self, event):
        self.scene.save_layout()
        if self.db:
            self.db.close()
        event.accept()

    # Zoom колесом мыши
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.view.scale(1.15, 1.15)
        else:
            self.view.scale(1/1.15, 1/1.15)