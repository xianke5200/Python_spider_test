#!usr/bin/env python
import os
from random import randrange as rrange
from db_sqlite_class import db_sqlite_class

COLSIZ = 10

class excel_db():
    def __init__(self, dbname = 'excel_db', table = 'lang', colsiz = 10):
        self.table = table
        self.db = db_sqlite_class(dbname, table, colsiz)

    def connect(self):
        self.db.connect()

    def create(self):
        self.db.create('''CREATE TABLE '''+ '%s' %self.table+'''(
                        filepath VARCHAR (8),
                        langtype VARCHAR (8),
                        prid INTEGER )
                        ''')

    def insert(self, filepath, language, index):
        self.db.insert("INSERT INTO %s VALUES(?, ?, ?)" % self.table,
                  [(filepath, language, index)])

    def getAll(self, index):
        return self.db.query("SELECT * FROM %s" % self.table)

    getRC = lambda cur: cur.rowcount if hasattr(cur, 'rowcount') else -1

    def delete(self, index):
        self.db.delete('DELETE FROM %s WHERE prid=%d' % (self.table, index))
        return

    def dbDump(self):
        print('\n%s%s%s' % ('FILE_PATH'.ljust(COLSIZ),
                            'LANG_TYPE'.ljust(COLSIZ), 'INDEX#'.ljust(COLSIZ)))
        self.db.dbDump()

    def dbClose(self):
        self.db.close()

    def dbRemove(self):
        self.db.remove()

def main():
    excel_calss = excel_db()
    excel_calss.connect()

    print('\n*** Creating users table')
    excel_calss.create()

    print('\n*** Inserting names into table')
    excel_calss.insert('1234', '1234', 1)
    excel_calss.dbDump()

    print('\n*** Randomly choosing group')
    excel_calss.delete(1)
    excel_calss.dbDump()

    print('\n*** Dropping users table')
    excel_calss.dbClose()


if __name__ == '__main__':
    main()