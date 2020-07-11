import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import  uic

import cv2 as cv
import time


import pyautogui as pag

import threading as thr 

# form_class = uic.loadUiType("main.ui")[0]
form_class = uic.loadUiType("/Users/yukyungmu/anaconda3/envs/macro/project/macro_test/main.ui")[0]

def click(event):
    print('click position = ', event.x, event.y)


def getPosition(self, data):
        print(thr.currentThread().getName())
        while True:
            x_1, y_1 = pag.position()
            postion_str = 'X:'+ str(x_1) + ' Y:' + str(y_1)
            time.sleep(0.1)
            print(postion_str)

class Work(QThread):

    finished = pyqtSignal(dict)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.working = True
        print('work init()')

    def run(self):
        while self.working:
            data = {}
            x, y = pag.position()
            data[0] = x
            data[1] = y
            # data[0] = x
            # data[1] = str(y)
            # self.TEXT_CUR_POS_Y.setText(str(y))
            # self.finished.emit(str(x), str(y))
            self.finished.emit(data)
            time.sleep(0.1)
    def stop(self):
        self.working = False


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('macro v.1.0')

        self.BTN_GET_MOUSE_POS.clicked.connect(self.getMousePos)
        # self.pushButton_2.clicked.connect(self.button1Function)
        # self.mouse
        # pag.click

        self.work = Work(self)
        # self.work.finished.connect(self.updatePosition)

    def keyPressEvent(self, e):
        # super().keyPressEvent(self, e)
        print('key press')
        # if e == Qt.ControlModifier:
            # print('press ctrl')
        if e.key() == Qt.Key_Control:
            print('press key crtl')
        if e.key() == Qt.Key_Meta:
            print('press key crtl meta mac ')
        if e.modifiers():
            print('e.modifiers()')
        if e.modifiers() & Qt.MetaModifier:
            print('meta e.modifiers')
              
        # return super().keyPressEvent(self, e)
        # return True 
        # Qt.Key_Shift
        
    def getMousePos(self):
        if self.BTN_GET_MOUSE_POS.text() == 'STOP':
            self.BTN_GET_MOUSE_POS.setText('Get Mouse position')
            # self.work = Work(self)
            self.work.stop()
            print('stop thread [work] [get mouse position]')
        else :
            # self.work = Work(self)
            self.work.finished.connect(self.updatePosition)
            self.work.start()
            self.work.working = True
            print('started thread [work] [get mouse position]')
            self.BTN_GET_MOUSE_POS.setText('STOP')


        if False : 
            
            print('ERROR!')
    



    def button2Function(self):
        print('clicked button2')

    def updatePosition(self, data):
        self.TEXT_CUR_POS_X.setText(str(data[0]))
        self.TEXT_CUR_POS_Y.setText(str(data[1]))
        # print('x : {}, y : {}', data[0], data[1])
        # print('In updatePosition')




    # def getPosition(self):
    #     # while(True):
    #     x, y, = pag.position()
    #     self.textEdit.setText(str(x))d
    #     self.plainTextEdit.setText(str(y))

    

    
    
if __name__ == "__main__" : 
    
    #  app 실행
    
    app = QApplication(sys.argv)
    # windowClass의 인스턴스 생성
    myWindow = WindowClass()
    # 프로드램 화면을 보여주는 코드
    myWindow.show()
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
    # pass

    # t = thr.Thread(target = getPosition(''))
    # t.start()

    print('main started')

