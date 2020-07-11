import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtWidgets
from PyQt5 import QtGui as qg
import work_scheduler as wk

import cv2 as cv
import time

import pyautogui as pag

import threading as thr

# import pygame

form_class = uic.loadUiType("ui/main.ui")[0]

nTblSchCnt = 0
aScheduler = []


# form_class = uic.loadUiType("/Users/yukyungmu/anaconda3/envs/macro/project/macro_test/main.ui")[0]


def click(event):
    print('click position = ', event.x, event.y)


def getPosition(self, data):
    print(thr.currentThread().getName())
    while True:
        x_1, y_1 = pag.position()
        strPosition = 'X:' + str(x_1) + ' Y:' + str(y_1)
        time.sleep(0.1)
        print(strPosition)


class Work(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.working = True
        print('work init()')

        b_recent = False

        # 최근 파일 있을 경우 불러오기
        if b_recent:
            self.load_recent(self)

    # 최근 파일이 있을 경우
    def load_recent(self):
        #
        path = 'temp/recent.csv'
        self.load_from_save(self, path)
        pass

    # 세이브 파일 불러오
    def load_from_save(self, path):
        pass

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

    # pag.mouse


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setupUi(self)

        self.setWindowTitle('macro v.1.0')

        width, height = pag.size()

        # self.main(self)

        self.BTN_GET_MOUSE_POS.clicked.connect(self.getMousePos)
        self.BTN_POS_ADD.clicked.connect(self.addPos)
        self.BTN_START.clicked.connect(self.start)
        self.BTN_LEFT_CLICK_ADD.clicked.connect(lambda: self.addClick('LEFT'))
        self.BTN_RIGHT_CLICK_ADD.clicked.connect(lambda: self.addClick('RIGHT'))

        # self.work.finished.connect(self.updatePosition)
        self.work = Work(self)

    def initUI(self):
        # exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Crtl+Q')
        exitAction.setStatusTip('Exit application')
        # exitAction.triggered(qApp.quit())
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        menubar.addAction(exitAction)

        # self.setWindowTitle("Macro MenuBar")
        self.setGeometry(300, 300, 300, 200)
        # self.show()

    def main(self):
        # self.pushButton_2.clicked.connect(self.button1Function)
        # self.mouse
        # pag.click
        pass

    def start(self):
        w = wk.work()
        w.start(aScheduler)
        pass

    def save(self):
        pass

    def keyPressEvent(self, e):
        # super().keyPressEvent(self, e)
        # print('key press')
        # if e == Qt.ControlModifier:
        # print('press ctrl')

        if e.key() == Qt.Key_Control:
            print('press key crtl')
        # crtl in mac
        elif e.key() == Qt.Key_Meta:
            print('press key crtl meta mac ')
        elif e.modifiers() == Qt.Key_Meta:
            print('meta e.modifiers')
        elif e.modifiers() == Qt.MetaModifier & e.key() == Qt.Key_P:
            print('set position')
        if e.key() == Qt.Key_P:
            print('press Key P')

            # f type(event) == QtGui.QKeyEvent and event.key() == QtCore.Qt.Key_A :

        # return super().keyPressEvent(self, e)
        # return True
        # Qt.Key_Shift

    def keyReleaseEvent(self, e):

        modifiers = QtWidgets.QApplication.keyboardModifiers()

        if type(e) == qg.QKeyEvent and e.key() == Qt.Key_P:
            print('aaa')

        if e.key == Qt.Key_P:
            print('release Key P')
        # if e.key
        elif e.key == Qt.Key_Q:
            print('stop sheduler')

    def mouseReleaseEvent(self, e):
        if self.BTN_GET_MOUSE_POS.text() == 'STOP':
            self.TEXT_POS_X.setText(self.TEXT_CUR_POS_X.toPlainText())
            self.TEXT_POS_Y.setText(self.TEXT_CUR_POS_Y.toPlainText())

    def addClick(self, direction):

        # pag.press('p')
        self.AddAction('CLICK', direction)

    def addPos(self):
        data = [self.TEXT_POS_X.toPlainText(), self.TEXT_POS_Y.toPlainText()]
        self.AddAction('POS', data)

    def AddAction(self, actionType, obj):
        global aScheduler

        action_map = {"action": actionType, "obj": obj}
        aScheduler.append(action_map)

        self.add_table(action_map)

    def add_table(self, scmap):
        global nTblSchCnt
        global aScheduler

        tblScheduler = self.TABLE_SCHEDULER
        nTblSchCnt = nTblSchCnt + 1
        tblScheduler.setRowCount(nTblSchCnt)

        tblScheduler.setItem(nTblSchCnt - 1, 0, QTableWidgetItem(scmap.get('action')))
        tblScheduler.setItem(nTblSchCnt - 1, 1, QTableWidgetItem(str(scmap.get('obj'))))

    def minus_table(self):
        global nTblSchCnt
        global aScheduler

        tblScheduler = self.TABLE_SCHEDULER
        nTblSchCnt = nTblSchCnt + 1
        tblScheduler.setRowCount(nTblSchCnt)

    def getMousePos(self):
        if self.BTN_GET_MOUSE_POS.text() == 'STOP':
            self.BTN_GET_MOUSE_POS.setText('Get Mouse position')
            # self.work = Work(self)
            self.work.stop()
            print('stop thread [work] [get mouse position]')
        else:
            # self.work = Work(self)
            self.work.finished.connect(self.updatePosition)
            self.work.start()
            self.work.working = True
            print('started thread [work] [get mouse position]')
            self.BTN_GET_MOUSE_POS.setText('STOP')

        if False:
            print('ERROR!')

    def button2Function(self):
        print('clicked button2')

    def updatePosition(self, data):
        self.TEXT_CUR_POS_X.setText(str(data[0]))
        self.TEXT_CUR_POS_Y.setText(str(data[1]))
        # print('x : {}, y : {}', data[0], data[1])
        # print('In updatePosition')

    def click(self, position):
        pag.click(position)

    def writeKeyboard(self, keyword):
        pag.typewrite(keyword)

    # def getPosition(self):
    #     # while(True):
    #     x, y, = pag.position()
    #     self.textEdit.setText(str(x))
    #     self.plainTextEdit.setText(str(y))


if __name__ == "__main__":
    #  app 실행
    app = QApplication(sys.argv)
    # windowClass의 인스턴스 생성
    myWindow = WindowClass()
    # 프로드램 화면을 보여주는 코드
    myWindow.show()
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    # app.exec_()
    sys.exit(app.exec_())
    # t = thr.Thread(target = getPosition(''))
    # t.start()
    print('main started')
