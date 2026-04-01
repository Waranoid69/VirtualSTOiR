import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton,
    QTableView, QFileDialog, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import QColor

class SqliteTableModel(QAbstractTableModel):
    """
    Модель данных: хранит строки таблицы в памяти,
    отслеживает изменённые и новые строки,
    умеет сохранять всё обратно в SQLite.
    """

    def __init__(self):
        super().__init__()
        self._headers: list[str] = []
        self._rows: list[list] = []
        self._original_rows: list[list] = []    # копия для сравнения
        self._new_row_indices: set[int] = set() # индексы новых (несохранённых) строк
        self._changed_cells: set[tuple] = set() # (row, col) изменённых ячеек

    # ------------------------------------------------------------------ #
    #  Обязательные методы QAbstractTableModel                           #
    # ------------------------------------------------------------------ #
    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self._headers)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        row, col = index.row(), index.column()

        if role in (Qt.DisplayRole, Qt.EditRole):
            return str(self._rows[row][col]) if self._rows[row][col] is not None else ""

        if role == Qt.BackgroundRole:
            if row in self._new_row_indices:
                return QColor("#d4edda")          # зелёный — новая строка
            if (row, col) in self._changed_cells:
                return QColor("#fff3cd")          # жёлтый — изменённая ячейка

        return QVariant()

    def headerData(self, section: int, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section] if section < len(self._headers) else ""
        return QVariant()

    def flags(self, index: QModelIndex):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def setData(self, index: QModelIndex, value, role=Qt.EditRole) -> bool:
        if not index.isValid() or role != Qt.EditRole:
            return False
        row, col = index.row(), index.column()
        self._rows[row][col] = value
        self._changed_cells.add((row, col))
        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.BackgroundRole])
        return True

    # ------------------------------------------------------------------ #
    #  Загрузка / сохранение                                              #
    # ------------------------------------------------------------------ #
    def load(self, conn: sqlite3.Connection, table: str) -> None:
        """Загружает таблицу из БД в модель."""
        self.beginResetModel()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM [{table}]")
        self._headers = [d[0] for d in cursor.description]
        self._rows = [list(row) for row in cursor.fetchall()]
        self._original_rows = [row.copy() for row in self._rows]
        self._new_row_indices.clear()
        self._changed_cells.clear()
        self.endResetModel()

    def save(self, conn: sqlite3.Connection, table: str) -> int:
        """
        Сохраняет изменения и новые строки в SQLite.
        Возвращает количество затронутых строк.
        """
        cursor = conn.cursor()
        saved = 0

        # Определяем есть ли столбец rowid/id для UPDATE
        # Используем rowid SQLite напрямую — он есть у каждой таблицы
        cursor.execute(f"SELECT rowid, * FROM [{table}]")
        rowid_map = {
            tuple(row[1:]): row[0]
            for row in cursor.fetchall()
        }

        cols = ", ".join(f"[{h}] = ?" for h in self._headers)
        placeholders = ", ".join(["?"] * len(self._headers))

        for i, row in enumerate(self._rows):
            if i in self._new_row_indices:
                # INSERT новой строки
                cursor.execute(
                    f"INSERT INTO [{table}] VALUES ({placeholders})",
                    row
                )
                saved += 1
            else:
                # UPDATE только изменённых строк
                changed_in_row = {c for (r, c) in self._changed_cells if r == i}
                if changed_in_row:
                    original_key = tuple(self._original_rows[i])
                    rowid = rowid_map.get(original_key)
                    if rowid is not None:
                        cursor.execute(
                            f"UPDATE [{table}] SET {cols} WHERE rowid = ?",
                            row + [rowid]
                        )
                        saved += 1

        conn.commit()

        # Сбрасываем флаги после сохранения
        self._original_rows = [r.copy() for r in self._rows]
        self._new_row_indices.clear()
        self._changed_cells.clear()
        self.layoutChanged.emit()
        return saved

    def add_empty_row(self) -> None:
        """Добавляет пустую строку в конец таблицы."""
        pos = len(self._rows)
        self.beginInsertRows(QModelIndex(), pos, pos)
        self._rows.append([""] * len(self._headers))
        self._new_row_indices.add(pos)
        self.endInsertRows()

    def remove_row(self, row: int, conn: sqlite3.Connection, table: str) -> None:
        """Удаляет строку из модели и из БД (если она уже сохранена)."""
        if row < 0 or row >= len(self._rows):
            return

        # Удаляем из БД только сохранённые строки
        if row not in self._new_row_indices:
            cursor = conn.cursor()
            cursor.execute(f"SELECT rowid, * FROM [{table}]")
            rowid_map = {tuple(r[1:]): r[0] for r in cursor.fetchall()}
            original_key = tuple(self._original_rows[row])
            rowid = rowid_map.get(original_key)
            if rowid is not None:
                cursor.execute(f"DELETE FROM [{table}] WHERE rowid = ?", (rowid,))
                conn.commit()

        self.beginRemoveRows(QModelIndex(), row, row)
        self._rows.pop(row)
        if row < len(self._original_rows):
            self._original_rows.pop(row)

        # Пересчитываем индексы новых строк
        self._new_row_indices = {
            (i - 1 if i > row else i)
            for i in self._new_row_indices if i != row
        }
        self._changed_cells = {
            (r - 1 if r > row else r, c)
            for (r, c) in self._changed_cells if r != row
        }
        self.endRemoveRows()

    def filter(self, text: str) -> None:
        """Простая фильтрация: показывает строки содержащие text (по всем столбцам)."""
        # Реализована через proxy-модель снаружи — см. Registry
        pass

# ------------------------------------------------------------------ #
#  Главное окно                                                        #
# ------------------------------------------------------------------ #
class Registry(QWidget):
    TABLE_NAME = "sensors"   # имя таблицы в SQLite

    def __init__(self):
        super().__init__()
        self.conn: sqlite3.Connection | None = None
        self.model = SqliteTableModel()
        self._setup_ui()
        self._connect_signals()

    # ------------------------------------------------------------------ #
    #  UI                                                                 #
    # ------------------------------------------------------------------ #
    def _setup_ui(self):
        self.setWindowTitle("Реестр оборудования КИПиА")
        self.resize(900, 550)

        root = QVBoxLayout(self)

        # --- Панель подключения к БД ---
        db_group = QGroupBox("База данных")
        db_layout = QHBoxLayout(db_group)
        self.lbl_db = QLabel("Файл не выбран")
        self.btn_open_db = QPushButton("Открыть БД…")
        db_layout.addWidget(self.lbl_db, stretch=1)
        db_layout.addWidget(self.btn_open_db)
        root.addWidget(db_group)

        # --- Фильтры ---
        filter_group = QGroupBox("Фильтры и поиск")
        filter_group.setStyleSheet("QGroupBox { font-size: 12pt; font-style: italic; }")
        filter_layout = QHBoxLayout(filter_group)
        filter_layout.addWidget(QLabel("Поиск по TAG"))
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Введите TAG…")
        self.btn_search = QPushButton("Найти")
        filter_layout.addWidget(self.lineEdit)
        filter_layout.addWidget(self.btn_search)
        root.addWidget(filter_group)

        # --- Таблица ---
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(False)   # сортировка через proxy
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setDefaultSectionSize(24)
        root.addWidget(self.table_view)

        # --- Нижняя панель ---
        self.lbl_count = QLabel("Всего записей в базе: 0")
        self.lbl_count.setStyleSheet("font-size: 14pt;")

        self.btn_add = QPushButton("Добавить новый прибор")
        self.btn_delete = QPushButton("Удалить выбранную строку")
        self.btn_save = QPushButton("Сохранить изменения")
        self.btn_delete.setStyleSheet("color: #c0392b;")
        self.btn_save.setStyleSheet("background: #2980b9; color: white; font-weight: bold;")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addStretch()

        bottom = QVBoxLayout()
        bottom.addWidget(self.lbl_count)
        bottom.addLayout(btn_layout)
        root.addLayout(bottom)

        # По умолчанию кнопки заблокированы до открытия БД
        self._set_buttons_enabled(False)

    def _set_buttons_enabled(self, enabled: bool):
        for btn in (self.btn_add, self.btn_delete, self.btn_save,
                    self.btn_search, self.lineEdit):
            btn.setEnabled(enabled)

    # ------------------------------------------------------------------ #
    #  Сигналы                                                            #
    # ------------------------------------------------------------------ #
    def _connect_signals(self):
        self.btn_open_db.clicked.connect(self._open_db)
        self.btn_search.clicked.connect(self._search)
        self.lineEdit.returnPressed.connect(self._search)
        self.btn_add.clicked.connect(self._add_row)
        self.btn_delete.clicked.connect(self._delete_row)
        self.btn_save.clicked.connect(self._save)
        self.model.rowsInserted.connect(self._update_count)
        self.model.rowsRemoved.connect(self._update_count)
        self.model.modelReset.connect(self._update_count)

    # ------------------------------------------------------------------ #
    #  Слоты                                                              #
    # ------------------------------------------------------------------ #
    def _open_db(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть базу данных", "", "SQLite (*.db *.sqlite *.sqlite3);;Все файлы (*)"
        )
        if not path:
            return
        try:
            if self.conn:
                self.conn.close()
            self.conn = sqlite3.connect(path)
            self.model.load(self.conn, self.TABLE_NAME)
            self.lbl_db.setText(path)
            self._set_buttons_enabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть БД:\n{e}")

    def _search(self):
        """Скрывает строки не содержащие текст поиска."""
        text = self.lineEdit.text().strip().lower()
        for row in range(self.model.rowCount()):
            match = any(
                text in str(self.model._rows[row][col]).lower()
                for col in range(self.model.columnCount())
            )
            self.table_view.setRowHidden(row, not match if text else False)

    def _add_row(self):
        self.model.add_empty_row()
        # Прокручиваем к новой строке
        last = self.model.index(self.model.rowCount() - 1, 0)
        self.table_view.scrollTo(last)
        self.table_view.setCurrentIndex(last)

    def _delete_row(self):
        index = self.table_view.currentIndex()
        if not index.isValid():
            QMessageBox.information(self, "Удаление", "Выберите строку для удаления.")
            return
        row = index.row()
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Удалить строку {row + 1}? Это действие нельзя отменить.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.model.remove_row(row, self.conn, self.TABLE_NAME)

    def _save(self):
        if not self.conn:
            return
        try:
            saved = self.model.save(self.conn, self.TABLE_NAME)
            QMessageBox.information(self, "Сохранено", f"Сохранено изменений: {saved}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка сохранения", str(e))

    def _update_count(self):
        self.lbl_count.setText(f"Всего записей в базе: {self.model.rowCount()}")

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Registry()
    window.show()
    sys.exit(app.exec_())
