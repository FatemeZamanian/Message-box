from sqlite3 import connect
class Database:

    @staticmethod
    def insert(code,name, family,birthdate, image):
        try:
            con = connect("Employee.db")
            cr = con.cursor()
            cr.execute(f"INSERT INTO Employee(CodeMelli,Name,Family,BirthDate,Image)VALUES('{code}','{name}','{family}','{birthdate}','{image}')")
            con.commit()
            con.close()
            return True
        except:
            return False

    @staticmethod
    def edit(i,code,n, f,b, img):
        # try:
        con = connect("Employee.db")
        cr = con.cursor()
        cr.execute(f"UPDATE Employee SET CodeMelli='{code}' ,Name='{n}', Family='{f}',BirthDate='{b}',Image='{img}' WHERE Id='{i}'")
        con.commit()
        con.close()
        return True
        # except:
        #     return False



    @staticmethod
    def select():
        try:
            con=connect("Employee.db")
            cr=con.cursor()
            cr.execute("SELECT * FROM Employee")
            res=cr.fetchall()
            return res
        except:
            return []
