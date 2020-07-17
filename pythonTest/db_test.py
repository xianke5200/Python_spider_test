#!usr/bin/env python

from random import randrange as rrange
from pythonTest.db_sqlite_class import db_sqlite_class

COLSIZ = 10
RDBMSs = {'s':'sqlite', 'm':'mysql', 'g':'gadfly'}

def setup():
    return RDBMSs[input('''Choose a database system:
    
    (M)ySQL
    (G)adfly
    (S)QLite
    
    Enter chioce: ''').strip().lower()[0]]

def connect(dbsel, db):
    if dbsel == 'sqlite':
        db.connect()

    elif dbsel == 'mysql':
        '''
        try:
            import MySQLdb
            import _mysql_execptions as DB_EXC
        except ImportError as e:
            return None

        try:
            cxn = MySQLdb.connect(db=dbName)
        except DB_EXC.OperationalError as e:
            pass
        cxn = MySQLdb.connect(user='root')
        try:
            cxn.query('DROP DATABASE %s' %dbName)
        except DB_EXC.OperationalError as e:
            pass
        cxn.query('CREATE DATABASE %s' %dbName)
        cxn.query("GRANT ALL ON %s.* to ''@'localhost'" %dbName)
        cxn.commit()
        cxn.close()
        cxn = MySQLdb.connect(db=dbName)
        '''
        pass

    elif dbsel == 'fadfly':
        '''
        try:
            from gadfly import gadfly
            DB_EXC = gadfly
        except ImportError as e:
            return None

        try:
            cxn = gadfly(dbName, dbDir)
        except IOError as e:
            cxn = gadfly()
            if not os.path.isdir(dbDir):
                os.mkdir(dbName, dbDir)
            cxn.startup(dbName, dbDir)
        else:
            return None
        '''

def create(db):
    db.create('''CREATE TABLE '''+ '%s' %db.tableName+'''(
                    login VARCHAR (8),
                    uid INTEGER ,
                    prid INTEGER )
                    ''')

drop = lambda cur: cur.execute('DROP TABLE users')

NAMES = (
    ('aaron', 8312), ('angela', 7603), ('dave', 7306),
    ('davina', 7902), ('elliot', 7911), ('ernie', 7410),
    ('jess', 7912), ('jim', 7512), ('larry', 7311),
    ('leslie', 7808), ('melissa', 8602), ('pat', 7711),
    ('serana', 7003), ('stan', 7607), ('faye', 6812),
    ('amy', 7209),
)

def randName():
    pick = list(NAMES)
    while len(pick) > 0:
        yield pick.pop(rrange(len(pick)))

def insert(dbsel, db):
    if dbsel == 'sqlite':
        db.insert("INSERT INTO %s VALUES(?, ?, ?)" %db.tableName,
                  [(who, uid, rrange(1, 5)) for who, uid in randName()])
    elif dbsel == 'gadfly':
        '''
        for who, uid in randName():
            cur.execute("INSERT INTO users VALUES(?, ?, ?)",
                        (who, uid, rrange(1, 5)))
        '''
        pass
    elif dbsel == 'mysql':
        '''
        cur.executemany("INSERT INTO users VALUES(?, ?, ?)",
        [(who, uid, rrange(1, 5)) for who, uid in randName()])
        '''
        pass

getRC = lambda cur: cur.rowcount if hasattr(cur, 'rowcount') else -1

def update(db):
    fr = rrange(1, 5)
    to = rrange(1, 5)
    db.update("UPDATE %s SET prid=%d WHERE prid=%d" % (db.tableName, to, fr))
    return fr, to, db.getRC()

def delete(db):
    rm = rrange(1, 5)
    db.delete('DELETE FROM %s WHERE prid=%d' %(db.tableName, rm))
    return rm, db.getRC()

def dbDump(db):
    print('\n%s%s%s' %('LOGIN'.ljust(COLSIZ),
        'USERID'.ljust(COLSIZ), 'PROJ#'.ljust(COLSIZ)))
    db.dbDump()


def main():
    dbsel = setup()
    print('*** Connecting to %r database' % dbsel)
    dbname = 'test'
    table = 'users'
    db = db_sqlite_class(dbname, table, COLSIZ)
    connect(dbsel, db)

    print('\n*** Creating users table')
    create(db)

    print('\n*** Inserting names into table')
    insert(dbsel, db)
    dbDump(db)

    print('\n*** Randomly moving folks')
    fr, to, num = update(db)
    print('from one group (%d) to another (%d)' %(fr, to))
    print('\t(%d users moved)' %num)
    dbDump(db)

    print('\n*** Randomly choosing group')
    rm, num = delete(db)
    print('(%d) to delete' %rm)
    print('\t(%d users removed)' %num)
    dbDump(db)

    print('\n*** Dropping users table')
    db.close()

if __name__ == '__main__':
    main()