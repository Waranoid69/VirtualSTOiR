import dbinout


if __name__ == '__main__':
    dbinout.ods_to_sqlite('SensorsDB.ods', 'toir.db')
    dbinout.sqlite_to_ods('toir.db', ['sensors'], 'SensorsDBnew.ods')