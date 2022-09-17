from email.mime import image
from signal import Signals
import sys
import pandas as pd
from plate_detection import plaka_detection_
from crop import crop_plate
from png_to_text import png_to_text
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
  
import datetime
import cv2
import time
import os
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt


class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    global img

    def run(self):
        cap = cv2.VideoCapture('rtsp://username:password@10.33.112.152')#****************152******************
        
        
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.img=frame
                self.changePixmap.emit(p)
                cv2.waitKey(10)
               
e = datetime.datetime.now()
timee=str(e.day)+'/'+ str(e.month)+'/'+ str(e.year) +'  '+str(e.hour) +':'+ str(e.minute) +':'+ str(e.second)
class App(QMainWindow):
    global save_con
    save_con=False
    def __init__(self):
        super().__init__()
        self.title = 'Plaka Detection System
        self.text='***Demo***'
        self.left = 50
        self.top = 50
        self.width = 500
        self.height = 200
      
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)
        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()
        # Create textbox
        # self.textbox = QLineEdit(self.text,self)
        # self.textbox.move(20, 20)
        # self.textbox.resize(280,40)
        # self.text='Koluman Plaka Tanıma Sistemi'
        self.textbox = QLineEdit(self.text,self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)
        f = self.textbox.font()
        f.setPointSize(14) # sets the size to 27
        self.textbox.setFont(f)
        
        # Create a button in the window
        self.button = QPushButton('Plakayı Kaydet', self)
        self.button.move(20,100)
        f2=self.button.font()
        f2.setPointSize(14) # sets the size to 27
        self.button.setFont(f2)
        self.button.resize(175,50)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)


        self.button = QPushButton('Foto Çek', self)
        self.button.move(20,230)
        f3=self.button.font()
        f3.setPointSize(14) # sets the size to 27
        self.button.setFont(f3)
        self.button.resize(175,50)
        self.button.clicked.connect(self.on_click_save)
        
        
        self.show()
        
    @pyqtSlot()
    def on_click(self):
        self.th.changePixmap.disconnect(self.setImage)

        textboxValue = self.textbox.text()
        df = pd.read_excel('C:\\Users\\omeresktop\\plate\\excel\\Plate_detect.xlsx')
        df=df.drop(df.columns[0],axis=1)
        e = datetime.datetime.now()
        timee=str(e.day)+'/'+ str(e.month)+'/'+ str(e.year) +'  '+str(e.hour) +':'+ str(e.minute) +':'+ str(e.second)
        
        #            Time    , Plaka  
        df.loc[df.index[-1]+1]=[timee,textboxValue]
        
        df.to_excel('C:\\Users\\oozer\\Desktop\\plate\\excel\\Plate_detect.xlsx')
        
        self.model = pandasModel(df)
        self.view = QTableView(self)
        self.view.setModel(self.model)
        self.view.move(1000, 120)

        self.view.resize(500, 750)
        self.view.show()
        self.th.changePixmap.connect(self.setImage)
        # QMessageBox.question(self, 'Typed Mesage box', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        # self.textbox.setText(textboxValue)
        

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
        

    @pyqtSlot()
    def on_click_save(self):
        e = datetime.datetime.now()
        timee=str(e.day)+'+'+ str(e.month)+'+'+ str(e.year) +'  '+str(e.hour) +'+'+ str(e.minute) +'+'+ str(e.second)
        
        original_image_path=f'C:\\Users\\oozer\\Desktop\\plate\\Kamre_Foto\\Orginal\\image_{timee}.png'
        self.th.changePixmap.disconnect(self.setImage)
        cv2.imwrite(original_image_path,self.th.img)
        self.mask_path=plaka_detection_(original_image_path)
        self.crop_image_path=crop_plate(self.mask_path,original_image_path)
        plate=png_to_text(self.crop_image_path)
       
        print(plate)
        # # plate='BOF_Tesla'#AI output
        # print('saasadsasad')
        self.textbox.setText(plate)
        # print('saasadsasad')
        self.th.changePixmap.connect(self.setImage)
        # self.com=show_plate()
        # self.com.text.connect(self.text_viewer)
        # self.com.text.emit('Lolo')
    
# """To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
# 1/1 [==============================] - 1s 714ms/step
# 1/1 [==============================] - 0s 89ms/step
# Traceback (most recent call last):
#   File "c:\Users\CDUKUNLU\Desktop\interface\opencv_interface.py", line 112, in on_click_save
# mask_path=plaka_detection_(original_image_path)
# File "c:\Users\CDUKUNLU\Desktop\interface\plate_detection.py", line 108, in plaka_detection_
# pred = np.array(df_pred.predicted_mask[0],dtype = np.uint8).squ
# genel hata düzeltilecek"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
