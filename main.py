# This Python file uses the following encoding: utf-8
import sys
from datetime import datetime
from  functools import partial
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
from database import Database


class MessageBox(QWidget):
    def __init__(self):
        super(MessageBox, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load("form.ui")
        self.dark = False
        self.ui.show()
        self.readMessage()
        self.ui.btn_send.clicked.connect(self.addNewMessage)
        self.ui.btn_Dall.clicked.connect(self.deleteAll)
        self.ui.btn_dark.clicked.connect(self.mode)
        self.check(name=5)


    def readMessage(self):
        for i in reversed(range(self.ui.gl_message.count())):
            self.ui.gl_message.itemAt(i).widget().setParent(None)
        msgs = Database.select()
        for i, msg in enumerate(msgs):
            label = QLabel()
            label.setText(msg[3] + '-   ' + msg[1] + ' : ' + msg[2])
            label.setFixedHeight(25)
            self.ui.gl_message.addWidget(label, i, 0)
            btn = QPushButton()
            btn.setMinimumSize(25, 25)
            btn.setMaximumSize(25, 25)
            btn.clicked.connect(partial(self.delete,i))
            btn.setStyleSheet("background-image:url(images/trsh.png);")
            btn.setFixedHeight(25)
            self.ui.gl_message.addWidget(btn, i, 1)


    def addNewMessage(self):
        name = self.ui.txt_name.text()
        text = self.ui.txt_text.text()
        time = datetime.now()
        time = time.strftime("%d %b - %H:%M")
        if self.check(name):
            if name != "" and text != "" :
                res = Database.insert(name, text, time)
                if res:
                    msgBox = QMessageBox()
                    msgBox.setText("Your message sent successfully")
                    msgBox.exec_()
                    label = QLabel()
                    label.setText(time + '-  ' + name + ' : ' + text)
                    label.setFixedHeight(25)
                    btn = QPushButton()
                    btn.setMinimumSize(25,25)
                    btn.setMaximumSize(25,25)
                    btn.setStyleSheet("background-image:url(images/trsh.png);")

                    msgs = Database.select()
                    for i in range(len(msgs), 0, -1):
                        btn.clicked.connect(partial(self.delete,i))
                        self.ui.gl_message.addWidget(label, i, 0)
                        self.ui.gl_message.addWidget(btn, i, 1)
                        break

                    self.ui.txt_name.setText("")
                    self.ui.txt_text.setText("")
                else:
                    msgBox = QMessageBox()
                    msgBox.setText("DB Error")
                    msgBox.exec_()


            else:
                msgBox = QMessageBox()
                msgBox.setText("Error Fields are empty")
                msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setText("you can send message after 1 minute....")
            msgBox.exec_()



    def delete(self,id):
        msgs=Database.select()
        ids=[]
        for msg in msgs:
            ids.append(msg[0])
        Database.delete(ids[id])
        self.readMessage()

    def deleteAll(self):
        Database.deleteAll()
        self.readMessage()

    def mode(self):
        if self.dark==False:
            self.ui.btn_dark.setStyleSheet("background-image:url(images/moon.png);")
            self.ui.setStyleSheet("background-color:rgb(30, 30, 30);color:rgb(255, 200, 144);")
            self.dark=True
        else:
            self.ui.btn_dark.setStyleSheet("background-image:url(images/sun.png);")
            self.ui.setStyleSheet("background-color:rgb(255, 200, 144);color:rgb(255, 0, 0);")
            self.dark = False

    def check(self,name):
        msgs=Database.select()
        time = datetime.now().strftime("%d %b - %H:%M")
        for msg in msgs:
            time_m=msg[3]
            if msg[1]==name:
                if time[:6] ==time_m[:6] and (time_m[-2:] ==time[-2:] and time_m[9:-3] == time[9:-3]):
                    return False

        else:
            return True


if __name__ == "__main__":
    app = QApplication([])
    widget = MessageBox()
    sys.exit(app.exec_())
