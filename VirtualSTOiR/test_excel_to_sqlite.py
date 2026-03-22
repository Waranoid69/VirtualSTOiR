import sqlite3
import csv
from aspose.cells import Workbook
NAME = "test_excel_to_sqlite"

def ods_to_sqlite(ods_file, db_name):
    workbook = Workbook(ods_file)
    workbook.save('tablecsv.csv')

    with open('tablecsv.csv', 'r', encoding='utf-8-sig') as f:  # utf-8-sig уберет лишние символы в начале
        # 1. Определяем разделитель автоматически
        content = f.read(2048)  # Читаем кусочек файла для анализа
        dialect = csv.Sniffer().sniff(content)
        f.seek(0)  # Возвращаемся в начало файла

        reader = csv.reader(f, dialect)
        headers = next(reader)

        # Очищаем заголовки (убираем пробелы и странные символы)
        headers = [h.strip().replace(" ", "_") for h in headers if h.strip()]

        # 2. Подключаемся к БД
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # 3. Пересоздаем таблицу
        cursor.execute("DROP TABLE IF EXISTS sensors")

        # Формируем запрос: [ID] TEXT, [Название] TEXT...
        cols_query = ", ".join([f"[{h}] TEXT" for h in headers])
        cursor.execute(f"CREATE TABLE sensors ({cols_query})")

        # 4. Загружаем данные по столбцам
        placeholders = ", ".join(["?" for _ in headers])
        query = f"INSERT INTO sensors VALUES ({placeholders})"

        count = 0
        for row in reader:
            if row and len(row) >= len(headers):
                # Берем только то количество данных, сколько у нас заголовков
                cursor.execute(query, row[:len(headers)])
                count += 1

        conn.commit()
        conn.close()
        print(f"Успех! Создано {len(headers)} столбцов и загружено {count} строк.")
        print(f"Список столбцов: {headers}")
    print('Zaversheno')

#ods_to_sqlite('Perechen_HART_brazets_studentam.ods', 'toir.db')