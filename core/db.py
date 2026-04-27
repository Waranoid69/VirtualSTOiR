import sqlite3
from datetime import date, datetime
from typing import Optional

COLUMNS = ["№", "Заводской_номер", "Тип_датчика", "Производитель",
           "Узел", "Шкаф", "ПЛК", "Код_параметра", "Наименование_параметра",
           "Статус", "Причина_ремонта", "Дата_производства", "Межповерочный_интервал",
           "Дата_последней_поверки"]

# Сколько дней до поверки считать
WARN_DAYS = 30   # жёлтый
ALERT_DAYS = 7    # красный

def get_sensor_status_color(date_str: str) -> str:
    """
      'red'    — до поверки <= ALERT_DAYS дней (или дата прошла)
      'yellow' — до поверки <= WARN_DAYS дней
      'black'  — всё в порядке
      'gray'   — дата не указана / неверный формат
    """
    if not date_str or not str(date_str).strip():
        return "gray"
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
        try:
            check_date = datetime.strptime(str(date_str).strip(), fmt).date()
            delta = (check_date - date.today()).days
            if delta <= ALERT_DAYS:
                return "red"
            if delta <= WARN_DAYS:
                return "yellow"
            return "black"
        except ValueError:
            continue
    return "gray"

class Database:
    def __init__(self, path: str):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    def get_all_sensors(self) -> list[dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sensors")
        return [dict(row) for row in cursor.fetchall()]

    def get_sensor_by_tag(self, tag: str) -> Optional[dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sensors WHERE [Заводской_номер] = ?", (tag,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_tags(self) -> list[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT [Заводской_номер] FROM sensors ORDER BY [Заводской_номер]")
        return [row[0] for row in cursor.fetchall()]