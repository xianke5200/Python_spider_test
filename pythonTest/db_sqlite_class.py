#!usr/bin/env python

import os
import sqlite3 as db_sql

class db_sqlite_class():

    def __init__(self, dbName, tableName, colsize):
        self.dbName = dbName
        self.tableName = tableName
        self.colsize = colsize
        self.dbDir = 'sqlite_db'

    def connect(self):
        if not os.path.isdir(self.dbDir):
            os.mkdir(self.dbDir)
        self.cxn = db_sql.connect(os.path.join(self.dbDir, self.dbName))
        self.cur = self.cxn.cursor()

    def create(self, dbCmd, *args, **kwargs):
        try:
            self.cur.execute(dbCmd, *args, **kwargs)
        except db_sql.OperationalError as e:
            dropCmd = 'DROP TABLE %s' %self.tableName
            self.cur.execute(dropCmd)
            self.cur.execute(dbCmd, *args, **kwargs)

    def insert(self, dbCmd, *args, **kwargs):
        self.cur.executemany(dbCmd, *args, **kwargs)

    def update(self, dbCmd, *args, **kwargs):
        self.cur.execute(dbCmd, *args, **kwargs)

    def delete(self, dbCmd, *args, **kwargs):
        self.cur.execute(dbCmd, *args, **kwargs)

    def delete_all(self):
        dumpCmd = 'DELETE FROM %s' % self.tableName
        self.cur.execute(dumpCmd)

    def delete_db(self):
        os.remove(os.path.join(self.dbDir, self.dbName))

    def dbDump(self):
        dumpCmd = 'SELECT * FROM %s' % self.tableName
        self.cur.execute(dumpCmd)
        for data in self.cur.fetchall():
            print('%s%s%s' % (tuple([str(s).title().ljust(self.colsize)
                                     for s in data])))

    def getRC(self):
        return self.cur.rowcount if hasattr(self.cur, 'rowcount') else -1

    def close(self):
        dropCmd = 'DROP TABLE %s' % self.tableName
        self.cur.execute(dropCmd)
        self.cur.close()
        self.cxn.commit()
        self.cxn.close()