from sqlite3 import connect
from datetime import datetime
class Database:

    @staticmethod
    def insert(name, text, time):
        try:
            con = connect("MessageDB.db")
            cr = con.cursor()
            cr.execute(f"INSERT INTO Message(Name,Text,Time)VALUES('{name}','{text}','{time}')")
            con.commit()
            con.close()
            return True
        except:
            return False

    @staticmethod
    def delete(id):
        try:
            con = connect("MessageDB.db")
            cr = con.cursor()
            cr.execute(f'DELETE FROM Message WHERE Message.Id={id}')
            con.commit()
            con.close()
            return True
        except:
            return False

    @staticmethod
    def deleteAll():
        try:
            con = connect("MessageDB.db")
            cr = con.cursor()
            cr.execute(f'DELETE FROM Message')
            con.commit()
            con.close()
            return True
        except:
            return False


    @staticmethod
    def select():
        try:
            con=connect("MessageDB.db")
            cr=con.cursor()
            cr.execute("SELECT * FROM Message")
            res=cr.fetchall()
            return res
        except:
            return []
