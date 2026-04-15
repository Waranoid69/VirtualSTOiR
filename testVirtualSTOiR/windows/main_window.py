import sqlite3
from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QMessageBox,
    QInputDialog, QGraphicsView, QProgressDialog
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

        # Сцена и вид
        self.scene = SchemaScene()
        self.view = QGraphicsView(self.scene)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.view.setRenderHint(__import__('PyQt5.QtGui', fromlist=['QPainter']).QPainter.Antialiasing)
        self.view.setRenderHint(__import__('PyQt5.QtGui', fromlist=['QPainter']).QPainter.SmoothPixmapTransform)
        self.view.setRenderHint(__import__('PyQt5.QtGui', fromlist=['QPainter']).QPainter.HighQualityAntialiasing)

        # Заменяем scrollArea на QGraphicsView
        self.centralWidget().layout().replaceWidget(self.scrollArea, self.view)
        self.scrollArea.hide()

        self._connect_actions()
        self._update_status()

    # ------------------------------------------------------------------ #
    #  Сигналы                                                             #
    # ------------------------------------------------------------------ #
    def _connect_actions(self):
        # Меню «Схема» — только схема
        self.Load.triggered.connect(self._load_pdf)
        self.ZoomIn.triggered.connect(lambda: self.view.scale(1.2, 1.2))
        self.ZoomOut.triggered.connect(lambda: self.view.scale(1 / 1.2, 1 / 1.2))

        # Тулбар
        self.actionOpenReestr.triggered.connect(self._open_registry)
        self.actionUpdate.triggered.connect(self._refresh_markers)
        self.actionEditorMode.toggled.connect(self._toggle_editor_mode)
        self.actionAddSensorPoint.triggered.connect(self._add_sensor_point_manually)

        # Отдельное действие для загрузки БД — добавляем в меню «Схема»
        from PyQt5.QtWidgets import QAction
        self.actionOpenDB = QAction("Открыть базу данных…", self)
        self.actionOpenDB.triggered.connect(self._open_db)
        self.Schema.addSeparator()
        self.Schema.addAction(self.actionOpenDB)
        # Также в тулбар
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionOpenDB)

        # Сцена
        self.scene.marker_double_clicked.connect(self._show_sensor_info)
        self.scene.add_marker_requested.connect(self._on_add_marker_requested)

    # ------------------------------------------------------------------ #
    #  Загрузка БД — независимо от схемы                                  #
    # ------------------------------------------------------------------ #
    def _open_db(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть базу данных", "",
            "SQLite (*.db *.sqlite *.sqlite3);;Все файлы (*)"
        )
        if not path:
            return
        try:
            if self.db:
                self.db.close()
            self.db = Database(path)
            self._update_status()
            # Если схема уже загружена — обновить цвета маркеров
            if self.scene._bg_item is not None:
                self.scene.update_marker_colors(self.db.get_all_sensors())
            QMessageBox.information(self, "БД открыта", f"База данных подключена:\n{path}")
        except ValueError as e:
            QMessageBox.critical(self, "Неверный файл", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть БД:\n{e}")

    # ------------------------------------------------------------------ #
    #  Загрузка PDF — независимо от БД                                    #
    # ------------------------------------------------------------------ #
    def _load_pdf(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Загрузить схему (PDF)", "", "PDF (*.pdf)"
        )
        if not path:
            return

        # Индикатор прогресса — рендер x4 занимает время
        progress = QProgressDialog("Рендеринг схемы...", None, 0, 0, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        progress.show()
        QApplication_processEvents()

        ok = self.scene.load_pdf(path)
        progress.close()

        if not ok:
            QMessageBox.critical(
                self, "Ошибка",
                "Не удалось загрузить PDF.\nУстановите: pip install pypdfium2 Pillow"
            )
            return

        # Загружаем маркеры если БД уже подключена
        if self.db:
            sensors = self.db.get_all_sensors()
            self.scene.load_layout(sensors)
        else:
            # Загружаем маркеры без цветов (БД ещё не открыта)
            self.scene.load_layout([])

        self._update_status()
        self.statusBar().showMessage(f"Схема загружена: {path}")

    # ------------------------------------------------------------------ #
    #  Реестр                                                              #
    # ------------------------------------------------------------------ #
    def _open_registry(self):
        if not self.db:
            reply = QMessageBox.question(
                self, "База данных не открыта",
                "Сначала откройте базу данных?\n(Схема → Открыть базу данных…)",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self._open_db()
            return
        if self.registry_window is None:
            self.registry_window = RegistryWindow(shared_conn=self.db.conn)
        self.registry_window.show()
        self.registry_window.raise_()

    # ------------------------------------------------------------------ #
    #  Маркеры                                                             #
    # ------------------------------------------------------------------ #
    def _toggle_editor_mode(self, enabled: bool):
        self.scene.set_editor_mode(enabled)
        if enabled:
            self.view.setDragMode(QGraphicsView.NoDrag)
            self.statusBar().showMessage(
                "Режим редактора ВКЛ — кликните на схему чтобы добавить датчик"
            )
        else:
            self.scene.save_layout()
            self.view.setDragMode(QGraphicsView.ScrollHandDrag)
            self.statusBar().showMessage("Расположение маркеров сохранено")

    def _add_sensor_point_manually(self):
        if not self.db:
            QMessageBox.warning(self, "Нет БД", "Сначала откройте базу данных.")
            return
        tags = self.db.get_all_tags()
        if not tags:
            QMessageBox.information(self, "Нет данных", "В базе нет датчиков.")
            return
        tag, ok = QInputDialog.getItem(
            self, "Добавить датчик", "Выберите TAG:", tags, 0, False
        )
        if ok and tag:
            from core.db import get_sensor_status_color
            sensor = self.db.get_sensor_by_tag(tag)
            color  = get_sensor_status_color(
                sensor.get("Дата_поверки", "") if sensor else ""
            )
            self.scene.add_marker(tag, 100, 100, color)
            self.scene.save_layout()

    def _on_add_marker_requested(self, x: float, y: float):
        if not self.db:
            QMessageBox.warning(self, "Нет БД", "Сначала откройте базу данных.")
            return
        tags = self.db.get_all_tags()
        if not tags:
            return
        tag, ok = QInputDialog.getItem(
            self, "Добавить датчик", "Выберите TAG:", tags, 0, False
        )
        if ok and tag:
            from core.db import get_sensor_status_color
            sensor = self.db.get_sensor_by_tag(tag)
            color  = get_sensor_status_color(
                sensor.get("Дата_поверки", "") if sensor else ""
            )
            self.scene.add_marker(tag, x, y, color)
            self.scene.save_layout()

    def _refresh_markers(self):
        if not self.db:
            QMessageBox.warning(self, "Нет БД", "Сначала откройте базу данных.")
            return
        self.scene.update_marker_colors(self.db.get_all_sensors())
        self.statusBar().showMessage("Цвета маркеров обновлены")

    # ------------------------------------------------------------------ #
    #  SensorInfo                                                          #
    # ------------------------------------------------------------------ #
    def _show_sensor_info(self, tag: str):
        if not self.db:
            return
        sensor = self.db.get_sensor_by_tag(tag)
        if not sensor:
            QMessageBox.warning(self, "Не найдено",
                                f"Датчик с TAG '{tag}' не найден в БД.")
            return
        dlg    = SensorInfoDialog(sensor, parent=self)
        result = dlg.exec_()
        if result == dlg.Accepted and hasattr(dlg, 'parent_open_registry_tag'):
            self._open_registry()
            if self.registry_window:
                self.registry_window.scroll_to_tag(dlg.parent_open_registry_tag)

    # ------------------------------------------------------------------ #
    #  Статусбар                                                           #
    # ------------------------------------------------------------------ #
    def _update_status(self):
        db_status = f"БД: {self.db.path}" if self.db else "БД: не открыта"
        schema_status = "Схема: загружена" if self.scene._bg_item else "Схема: не загружена"
        self.statusBar().showMessage(f"{db_status}   |   {schema_status}")

    # ------------------------------------------------------------------ #
    #  Закрытие / зум                                                      #
    # ------------------------------------------------------------------ #
    def closeEvent(self, event):
        self.scene.save_layout()
        if self.db:
            self.db.close()
        event.accept()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.view.scale(1.15, 1.15)
        else:
            self.view.scale(1 / 1.15, 1 / 1.15)


# Хелпер для processEvents без импорта на уровне модуля
def QApplication_processEvents():
    from PyQt5.QtWidgets import QApplication
    QApplication.processEvents()