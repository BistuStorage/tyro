#coding=utf-8

import psycopg2
import xlrd

dbcursor=None
db=None

def connect():
    global db,dbcursor
    db=psycopg2.connect(database='mydb',user='postgres',password='123456')
    dbcursor=db.cursor()

def disconnect():
    dbcursor.close()
    db.close()
    dbcursor=None
    db=None

def any2str(data):
    if isinstance(data,unicode):
        return "'" + data.encode('utf-8') + "'"
    else:
        return "'" + str(data) + "'"

def intodb(file):
    global db,dbcursor
    data=xlrd.open_workbook(file)
    table=data.sheets()[0]
    for r in xrange(1,table.nrows):
        cmdstr = "insert into book values(" 
        for c in xrange(table.ncols):
            cmdstr += any2str(table.row(r)[c].value)
            if c != table.ncols-1:
                cmdstr += ","
        cmdstr += ")"
        dbcursor.execute(cmdstr)
    db.commit()
def search(content):
    global db,dbcursor
    #cmdstr = "select * from book where to_tsvector('chinesecfg',isbn || name)@@to_tsquery('chinesecfg','"+content+"')"
    cmdstr="select * from book where tokenize(isbn)@@tokenize('"+content+"') or tokenize(name)@@tokenize('"+content+"')"
    dbcursor.execute(cmdstr)
    rtdata=dbcursor.fetchall()
    db.commit()
    return rtdata
