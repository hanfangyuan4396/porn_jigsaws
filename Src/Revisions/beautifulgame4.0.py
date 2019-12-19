import sys
import random
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *


SIZE = 150
GAP = 20
BTNSIZE = 100

EASYSHUFFLE = [[0,7,1,3,2,6,5,4,8],
               [3,7,2,1,5,6,0,4,8],
               [5,0,6,7,4,2,3,1,8]]

ORDINARYSHUFFLE = [[1,7,5,4,6,0,10,2,8,13,3,11,9,14,12,15],
                   [4,1,3,11,0,2,6,9,8,13,5,14,7,10,13,15],
                   [12,1,2,9,6,0,7,4,14,8,5,3,13,10,11,15]]
                
HARDSHUFFLE = [[7,5,3,6,4,1,11,8,2,18,10,23,13,19,16,12,17,0,9,22,15,21,14,20,24],
               [1,12,5,8,3,0,17,16,22,2,10,20,19,18,6,11,15,13,9,4,7,21,23,14,24],
               [11,2,8,6,9,5,19,0,3,7,10,16,21,20,23,13,22,18,1,17,15,12,14,4,24]]

class BlockWindow(QWidget):

    finished = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)
        self.mode = 'Ordinary'
        self.level = 'Level 1'
        self.mode_num = 4
        self.shuffle_list = ORDINARYSHUFFLE
        self.readResources()
        

    def paintEvent(self, event):
        self.setFixedSize(SIZE * self.mode_num, SIZE * self.mode_num)
        qp = QPainter()
        qp.begin(self)
        self.drawMe(qp)
        qp.end()


    #定义判断是否完成函数，返回在正确位置滑块的数目
    def isFinished(self):
        counter = 0
        for i in range(self.mode_num ** 2 - 1):
            if self.data[i][1] == i:
                counter += 1
        return counter

    def readResources(self):
        self.data = []
        for i in range(self.mode_num ** 2):
            img_num = []
            img = QImage(f'{self.mode}/{self.level}/{i}.png')
            img_num.append(img)
            img_num.append(i)
            self.data.append(img_num)
            

    #画出滑块界面



    def drawMe(self, qp):
        pen = QPen(Qt.white, 1, Qt.SolidLine)
        brush = QBrush(QColor('white'))
        qp.setPen(pen)
        qp.setBrush(brush)
        for i in range(self.mode_num):
            for j in range(self.mode_num):
                ix = i * self.mode_num + j
                if self.data[ix][1] != self.mode_num ** 2 - 1:
                    x = SIZE * j
                    y = SIZE * i 
                    qp.drawRect(x, y, SIZE, SIZE)
                    img_scaled = self.data[ix][0].scaled(SIZE, SIZE, Qt.KeepAspectRatio)
                    qp.drawImage(x, y, img_scaled)


    #读出所在滑块的数字
    def getNum(self, i, j):
        if 0 <= i < self.mode_num and 0 <= j < self.mode_num:
            ix = i * self.mode_num + j
            return self.data[ix][1]
        else:
            return -1

    #定义交换函数，交换两个滑块 
    def swap(self, i, j, m, n):
        ix1 = i * self.mode_num + j
        ix2 = m * self.mode_num + n
        tmp = self.data[ix1][0]
        self.data[ix1][0] = self.data[ix2][0]
        self.data[ix2][0] = tmp
        tmp = self.data[ix1][1]
        self.data[ix1][1] = self.data[ix2][1]
        self.data[ix2][1] = tmp
        if self.isFinished() == self.mode_num ** 2 - 1:
            self.finished.emit()
        self.update()

    #当鼠标点击空白滑块周围的滑块时交换
    def mousePressEvent(self, evt):
        x, y = evt.x(), evt.y()
        j = int(x/SIZE)
        i = int(y/SIZE)
        if 0 <= i < self.mode_num and 0 <= j < self.mode_num:
            if self.getNum(i-1, j) == self.mode_num ** 2 - 1:
                self.swap(i, j, i - 1, j)
            elif self.getNum(i + 1, j) == self.mode_num ** 2 - 1:
                self.swap(i, j, i + 1, j)
            elif self.getNum(i, j - 1) == self.mode_num ** 2 - 1:
                self.swap(i, j, i, j - 1)
            elif self.getNum(i, j + 1) == self.mode_num ** 2 - 1:
                self.swap(i, j, i, j + 1)

    #打乱滑块，因为不能随意打乱，所以定义了三种打乱方式
    def shuffle(self):
        rand = random.randint(0,2)
        rand_list = self.shuffle_list[rand]
        index = -1
        for i in rand_list:
            img_num = []
            img = QImage(f'{self.mode}/{self.level}/{i}.png')
            img_num.append(img)
            img_num.append(i)
            index = index + 1
            self.data[index] = img_num
            self.update()



    def changeModeToEasy(self):
        global SIZE
        SIZE = 150
        self.mode = 'Easy'
        self.level = 'Level 1'
        self.mode_num = 3
        self.shuffle_list = EASYSHUFFLE
        self.readResources()
        self.update()

    def changeModeToOrdinary(self):
        global SIZE
        SIZE = 150
        self.mode = 'Ordinary'
        self.level = 'Level 1'
        self.mode_num = 4
        self.shuffle_list = ORDINARYSHUFFLE
        self.readResources()
        self.update()

        

    def changeModeToHard(self):
        global SIZE
        SIZE = 125
        self.mode = 'Hard'
        self.level = 'Level 1'
        self.mode_num = 5
        self.shuffle_list = HARDSHUFFLE
        self.readResources()
        self.update()
   
    def changeLevelTo1(self):
        self.level = 'Level 1'
        self.readResources()
        self.update()


    def changeLevelTo2(self):
        self.level = 'Level 2'
        self.readResources()
        self.update()

        

    def changeLevelTo3(self):
        self.level = 'Level 3'
        self.readResources()
        self.update()

       





class TopWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initSignalSlot()
        self.timer.start(5000)
        self.setWindowTitle('game')

    
    def initUI(self):
        vLayout = QVBoxLayout()
        grid = QGridLayout()
        self.canvas = BlockWindow(self)
        self.easyButton = QPushButton('Easy', self)
        self.ordinaryButton = QPushButton('Ordinary', self)
        self.hardButton = QPushButton('Hard', self)
        self.level1Button = QPushButton('Level 1', self)
        self.level2Button = QPushButton('Level 2', self)
        self.level3Button = QPushButton('Level 3', self) 
        grid.addWidget(self.easyButton, 0, 0)  
        grid.addWidget(self.ordinaryButton, 0, 1) 
        grid.addWidget(self.hardButton, 0, 2)
        grid.addWidget(self.level1Button, 1, 0)
        grid.addWidget(self.level2Button, 1, 1) 
        grid.addWidget(self.level3Button, 1, 2)       
        vLayout.addWidget(self.canvas, stretch = 1)
        vLayout.addLayout(grid)
        self.setLayout(vLayout)

    def paintEvent(self, event):
        self.setFixedSize(SIZE * self.canvas.mode_num + GAP,
         SIZE * self.canvas.mode_num + BTNSIZE )



    def initSignalSlot(self):
        self.timer = QTimer(self)
        self.easyButton.clicked.connect(self.onEasy)
        self.ordinaryButton.clicked.connect(self.onOrdinary)
        self.hardButton.clicked.connect(self.onHard)
        self.level1Button.clicked.connect(self.onLevel1)
        self.level2Button.clicked.connect(self.onLevel2)
        self.level3Button.clicked.connect(self.onLevel3)
        self.canvas.finished.connect(self.onFinished)
        self.timer.timeout.connect(self.onTimer)

    def onEasy(self):
        self.canvas.changeModeToEasy()
        self.timer.start(5000)
        QMessageBox.question(self, '消息框', '5秒之后打乱图片', 
        QMessageBox.Ok)
    
    def onOrdinary(self):
        self.canvas.changeModeToOrdinary()
        self.timer.start(5000)
        QMessageBox.question(self, '消息框', '5秒之后打乱图片', 
        QMessageBox.Ok)        

    def onHard(self):
        self.canvas.changeModeToHard()
        self.timer.start(5000)
        QMessageBox.question(self, '消息框', '5秒之后打乱图片', 
        QMessageBox.Ok)       

    def onLevel1(self):
        self.canvas.changeLevelTo1()
        self.timer.start(5000)
        QMessageBox.question(self, '消息框', '5秒之后打乱图片', 
        QMessageBox.Ok)        

    def onLevel2(self):
        self.canvas.changeLevelTo2()
        self.timer.start(5000)
        QMessageBox.question(self, '消息框', '5秒之后打乱图片', 
        QMessageBox.Ok)        

    def onLevel3(self):
        self.canvas.changeLevelTo3()
        self.timer.start(5000)
        QMessageBox.question(self, '消息框', '5秒之后打乱图片', 
        QMessageBox.Ok)    
    
    def onTimer(self):
        self.canvas.shuffle()
        self.timer.stop()
    
    def onFinished(self):
        QMessageBox.question(self, '消息框', '祝贺，成功复原！', QMessageBox.Ok)
    

app = QApplication(sys.argv)
w = TopWindow()
w.show()
app.exec_()
