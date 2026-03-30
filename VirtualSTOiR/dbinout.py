import sqlite3
import pyexcel_ods3
from pathlib import Path

def sanitize_name(name: str) -> str:
    """Приводит имя к безопасному виду для SQLite (таблица / столбец)."""
    name = name.strip().replace(" ", "_")
    if name and name[0].isdigit():               # имя не может начинаться с цифры
        name = f"_{name}"
    return name or "unnamed"

def ods_to_sqlite(ods_file: str, db_name: str) -> None:
    """
    Загружает все листы ODS-файла в SQLite.
    Каждый лист → отдельная таблица; имя листа → имя таблицы.

    :param ods_file:  путь к входному ODS-файлу
    :param db_name:   путь к файлу БД SQLite
    """
    ods_path = Path(ods_file)
    if not ods_path.exists():
        raise FileNotFoundError(f"Файл не найден: {ods_file}")

    # --- 1. Читаем ODS напрямую, без промежуточного CSV ---
    sheets: dict = pyexcel_ods3.get_data(str(ods_path))

    if not sheets:
        raise ValueError("ODS-файл не содержит листов с данными.")

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        for sheet_name, rows in sheets.items():
            # Пропускаем пустые листы
            if not rows:
                print(f"  [пропущен] Лист '{sheet_name}' пуст.")
                continue

            # --- 2. Заголовки — первая строка листа ---
            raw_headers = [str(cell) for cell in rows[0]]
            headers = [sanitize_name(h) for h in raw_headers if str(h).strip()]

            if not headers:
                print(f"  [пропущен] Лист '{sheet_name}': не удалось прочитать заголовки.")
                continue

            table_name = sanitize_name(sheet_name)

            # --- 3. Пересоздаём таблицу ---
            cursor.execute(f"DROP TABLE IF EXISTS [{table_name}]")
            cols_def = ", ".join(f"[{h}] TEXT" for h in headers)
            cursor.execute(f"CREATE TABLE [{table_name}] ({cols_def})")

            # --- 4. Фильтруем и нормализуем строки данных ---
            data_rows = []
            for row in rows[1:]:
                # Приводим все ячейки к str, добиваем до нужной длины если строка короче
                normalized = [str(cell) for cell in row] + [""] * len(headers)
                normalized = normalized[:len(headers)]

                # Пропускаем полностью пустые строки
                if any(cell.strip() for cell in normalized):
                    data_rows.append(normalized)

            # --- 5. Пакетная вставка ---
            placeholders = ", ".join(["?"] * len(headers))
            cursor.executemany(
                f"INSERT INTO [{table_name}] VALUES ({placeholders})",
                data_rows
            )

            print(f"  [OK] '{sheet_name}' → таблица '{table_name}': "
                  f"{len(headers)} столбцов, {len(data_rows)} строк.")

    print(f"\nГотово! База данных сохранена: {db_name}")

def sqlite_to_ods(db_name: str, table_names: list[str], output_file: str):
    """
    Выгружает указанные таблицы из SQLite в один ODS-файл.
    Каждая таблица — отдельный лист.

    :param db_name:      путь к файлу БД, например "test_excel_to_sqlite.db"
    :param table_names:  список таблиц, например ["sensors", "devices"]
    :param output_file:  имя выходного файла, например "output.ods"
    """
    sheets = {}

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        for table in table_names:
            # Получаем данные
            cursor.execute(f"SELECT * FROM [{table}]")
            rows = cursor.fetchall()

            # Получаем заголовки столбцов
            headers = [description[0] for description in cursor.description]

            # Лист = заголовки + строки данных
            sheets[table] = [headers] + [list(row) for row in rows]

            print(f"Таблица '{table}': {len(headers)} столбцов, {len(rows)} строк.")

    pyexcel_ods3.save_data(output_file, sheets)
    print(f"\nГотово! Файл сохранён: {output_file}")
