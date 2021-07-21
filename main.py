# This Python file uses the following encoding: utf-8
import sys
from functools import partial
import sys
from PySide6 import QtGui
sys.modules['PyQt5.QtGui'] = QtGui
from PIL import ImageQt
import os
from PyQt5.QtGui import QImage
from PySide6.QtGui import QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
from PySide6.QtCore import QThread, Signal, QDir, QSize
from database import Database
import cv2

def convertCVImage2QtImage(cv_img):
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    height, width, channel = cv_img.shape
    bytesPerLine = 3 * width
    qimg = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return QPixmap.fromImage(qimg)

class Camera(QThread):
    set_camera_signal = Signal(object,object)

    def __init__(self):
        super(Camera, self).__init__()
        self.image_face=cv2.imread('images/sun.png')
    def run(self):
        self.video = cv2.VideoCapture(0)

        face_detector = cv2.CascadeClassifier('fd.xml')
        while True:
            valid, self.frame = self.video.read()
            if valid is not True:
                break
            frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(frame_gray, 3.1)

            for face in faces:
                x, y, w, h = face
                self.image_face = self.frame[y:y + h, x:x + w]
            self.set_camera_signal.emit(self.frame,self.image_face)
            cv2.waitKey(30)

    def stop(self):
        try:
            self.video.release()
        except:
            pass

class MessageBox(QWidget):

    def __init__(self):
        super(MessageBox, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load("form.ui")
        self.Addui = loader.load("Addform.ui")
        self.cameraui = loader.load("pictureform.ui")
        self.editui=loader.load("Editform.ui")
        self.ui.show()
        self.readInfo()
        self.ui.btn_Add.clicked.connect(self.openAdd)
        self.thread_cameras = Camera()
        self.thread_cameras.set_camera_signal.connect(self.show_e)

        self.cameraui.fbtn_00.clicked.connect(self.save0)
        self.cameraui.fbtn_01.clicked.connect(self.save1)
        self.cameraui.fbtn_02.clicked.connect(self.save2)
        self.cameraui.fbtn_10.clicked.connect(self.save3)
        self.cameraui.fbtn_11.clicked.connect(self.save4)
        self.cameraui.fbtn_12.clicked.connect(self.save5)
        self.cameraui.fbtn_20.clicked.connect(self.save6)
        self.cameraui.fbtn_21.clicked.connect(self.save7)
        self.cameraui.fbtn_22.clicked.connect(self.save8)

        self.dir ='/home/fateme/Desktop/PyClass/PyCourse30-miniproject/Employees/images/'


    def readInfo(self):
        for i in reversed(range(self.ui.gl_info.count())):
            self.ui.gl_info.itemAt(i).widget().setParent(None)
        infos = Database.select()
        for i, info in enumerate(infos):
            label = QLabel()
            label.setText(info[2] + '  ' + info[3])
            label.setFixedHeight(25)
            self.ui.gl_info.addWidget(label, i, 0)
            labell = QLabel()
            labell.setMinimumSize(30, 30)
            labell.setMaximumSize(30, 30)
            t=cv2.imread(str(info[5]))
            t=cv2.resize(t,(30,30))
            t= convertCVImage2QtImage(t)
            pixmap = QPixmap(t)
            labell.setPixmap(pixmap)
            labell.setFixedHeight(25)
            self.ui.gl_info.addWidget(labell, i, 1)
            btn = QPushButton()
            btn.setMinimumSize(25, 25)
            btn.setMaximumSize(25, 25)
            btn.clicked.connect(partial(self.openEdite,i))
            btn.setText("Edit")
            btn.setFixedHeight(25)
            self.ui.gl_info.addWidget(btn, i, 2)

    def openAdd(self):
        self.Addui.show()
        self.Addui.btnAdd.clicked.connect(self.addNewEmployee)
        self.Addui.btn_pic.clicked.connect(self.getPicture)

    def getPicture(self):
        self.thread_cameras.start()
        self.cameraui.show()

    def show_e(self,img,face):

        self.face=face
        img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

        # img0=cv2.applyColorMap(img,cv2.COLORMAP_JET)
        img0=cv2.transform(img,10)
        res_img = convertCVImage2QtImage(img0)
        self.cameraui.fbtn_00.setIcon(res_img)
        self.cameraui.fbtn_00.setIconSize(QSize(150, 150))
        self.cameraui.fbtn_00.setStyleSheet('QPushButton{border: 0px solid;}')

        img1 = cv2.applyColorMap(img, cv2.COLORMAP_COOL)
        res_img = convertCVImage2QtImage(img1)
        self.cameraui.fbtn_01.setIcon(res_img)
        self.cameraui.fbtn_01.setIconSize(QSize(150, 150))
        self.cameraui.fbtn_01.setStyleSheet('QPushButton{border: 0px solid;}')

        img2 = cv2.applyColorMap(img, cv2.COLORMAP_VIRIDIS)
        res_img = convertCVImage2QtImage(img2)
        self.cameraui.fbtn_02.setIcon(res_img)
        self.cameraui.fbtn_02.setIconSize(QSize(150, 150))
        self.cameraui.fbtn_02.setStyleSheet('QPushButton{border: 0px solid;}')

        img3 = cv2.applyColorMap(img, cv2.COLORMAP_TWILIGHT_SHIFTED)
        res_img = convertCVImage2QtImage(img3)
        self.cameraui.fbtn_10.setIcon(res_img)
        self.cameraui.fbtn_10.setIconSize(QSize(150, 150))
        self.cameraui.fbtn_10.setStyleSheet('QPushButton{border: 0px solid;}')

        img4 = cv2.applyColorMap(img, cv2.COLORMAP_HOT)
        res_img = convertCVImage2QtImage(img4)
        self.cameraui.fbtn_11.setIcon(res_img)
        self.cameraui.fbtn_11.setIconSize(QSize(150, 150))
        self.cameraui.fbtn_11.setStyleSheet('QPushButton{border: 0px solid;}')

        img5 = cv2.applyColorMap(img, cv2.COLORMAP_TURBO)
        res_img = convertCVImage2QtImage(img5)
        self.cameraui.fbtn_12.setIcon(res_img)
        self.cameraui.fbtn_12.setIconSize(QSize(150, 150))
        self.cameraui.fbtn_12.setStyleSheet('QPushButton{border: 0px solid;}')

        img6 = cv2.applyColorMap(img, cv2.COLORMAP_CIVIDIS)
        res_img = convertCVImage2QtImage(img6)
        self.cameraui.fbtn_20.setIcon(res_img)
        self.cameraui.fbtn_20.setIconSize(QSize(150, 150))
        self.cameraui.fbtn_20.setStyleSheet('QPushButton{border: 0px solid;}')

        img7 = cv2.applyColorMap(img, cv2.COLORMAP_SUMMER)
        res_img = convertCVImage2QtImage(img7)
        self.cameraui.fbtn_21.setIcon(res_img)
        self.cameraui.fbtn_21.setIconSize(QSize(150, 150))
        self.cameraui.fbtn_21.setStyleSheet('QPushButton{border: 0px solid;}')

        img8 = cv2.applyColorMap(img, cv2.COLORMAP_SPRING)
        res_img = convertCVImage2QtImage(img8)
        self.cameraui.fbtn_22.setIcon(res_img)
        self.cameraui.fbtn_22.setIconSize(QSize(150, 150))
        self.cameraui.fbtn_22.setStyleSheet('QPushButton{border: 0px solid;}')

    def directory(self):
        l=0
        for f in os.scandir(self.dir):
            l+=1
        return l

    def save(self,img):
        n = self.directory()
        cv2.imwrite(f'images/employee{n}.jpg', img)
        self.image = f'images/employee{n}.jpg'
        self.thread_cameras.stop()
        self.cameraui.close()
    def save0(self):
        img0= cv2.applyColorMap(self.face, cv2.COLORMAP_JET)
        self.save(img0)
    def save1(self):
        img0 = cv2.applyColorMap(self.face, cv2.COLORMAP_COOL)
        self.save(img0)
    def save2(self):
        img0 = cv2.applyColorMap(self.face, cv2.COLORMAP_VIRIDIS)
        self.save(img0)
    def save3(self):
        img0 = cv2.applyColorMap(self.face, cv2.COLORMAP_TWILIGHT_SHIFTED)
        self.save(img0)
    def save4(self):
        img0 = cv2.applyColorMap(self.face, cv2.COLORMAP_HOT)
        self.save(img0)
    def save5(self):
        img0 = cv2.applyColorMap(self.face, cv2.COLORMAP_TURBO)
        self.save(img0)
    def save6(self):
        img0 = cv2.applyColorMap(self.face, cv2.COLORMAP_CIVIDIS)
        self.save(img0)
    def save7(self):
        img0 = cv2.applyColorMap(self.face, cv2.COLORMAP_SUMMER)
        self.save(img0)
    def save8(self):
        img0 = cv2.applyColorMap(self.face, cv2.COLORMAP_SPRING)
        self.save(img0)

    def addNewEmployee(self):
        code=self.Addui.txt_codemelli.text()
        name = self.Addui.txt_name.text()
        family=self.Addui.txt_family.text()
        birthdate=self.Addui.txt_birthdate.text()
        image=self.image
        if name != "" and code != "" and family !="" and birthdate !="" and image != None:
            res = Database.insert(code,name,family,birthdate,image)
            if res:
                label = QLabel()
                label.setText(name + ' ' + family)
                label.setFixedHeight(25)
                btn = QPushButton()
                btn.setMinimumSize(25,25)
                btn.setMaximumSize(25,25)
                btn.setText("Edit")
                labell = QLabel()
                labell.setMinimumSize(30, 30)
                labell.setMaximumSize(30, 30)
                t = cv2.imread(image)
                t = cv2.resize(t, (30, 30))
                t = convertCVImage2QtImage(t)
                pixmap = QPixmap(t)
                labell.setPixmap(pixmap)
                labell.setFixedHeight(25)
                infos = Database.select()
                for i in range(len(infos), 0, -1):
                    btn.clicked.connect(partial(self.openEdite,i))
                    self.ui.gl_info.addWidget(label, i, 0)
                    self.ui.gl_info.addWidget(btn, i, 2)
                    self.ui.gl_info.addWidget(labell, i, 1)
                    break
                self.Addui.close()
            else:
                msgBox = QMessageBox()
                msgBox.setText("DB Error")
                msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setText("Error Fields are empty")
            msgBox.exec_()

    def openEdite(self,i):
        self.image = None
        self.editui.show()
        infos = Database.select()
        ids = []
        for info in infos:
            ids.append({"id": info[0], "code": info[1], "name": info[2], "family": info[3], "birthdate": info[4],"image":info[5]})
        temp = ids[i]
        self.editui.ecode.setText(str(temp["code"]))
        self.editui.ename.setText(temp["name"])
        self.editui.efamily.setText(temp["family"])
        self.editui.ebirthdate.setText(temp["birthdate"])
        self.img=temp["image"]


        self.editui.e_pic.clicked.connect(self.getPicture)
        self.editui.esave.clicked.connect(partial(self.edit,i))

    def edit(self, id):
        infos=Database.select()
        ids=[]
        for info in infos:
            ids.append({"id":info[0],"code":info[1],"name":info[2],"family":info[3],"birthdate":info[4]})
        temp=ids[id]
        code=self.editui.ecode.text()
        name=self.editui.ename.text()
        family=self.editui.efamily.text()
        birthdate=self.editui.ebirthdate.text()
        if self.image == None:
            image=self.img
        else:
            image=self.image
        Database.edit(temp["id"],code,name,family,birthdate,image)
        self.readInfo()
        self.editui.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = MessageBox()
    sys.exit(app.exec())
