import sys
#import random
#import time
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


    
    finished00 = pyqtSignal()
    finished01 = pyqtSignal()
    finished02 = pyqtSignal()
    finished10 = pyqtSignal()
    finished11 = pyqtSignal()
    finished12 = pyqtSignal()
    finished20 = pyqtSignal()
    finished21 = pyqtSignal()
    finished22 = pyqtSignal()
    
    
    


    def __init__(self, parent = None):
        super().__init__(parent)
        self.mode = 'Easy'
        self.level = 'Level 1'
        self.egg = 0
        self.box_num = 3
        self.mode_num = 0
        self.level_num = 0
        self.shuffle_list = EASYSHUFFLE
        self.readResources()
        

    def paintEvent(self, event):
        self.setFixedSize(SIZE * self.box_num, SIZE * self.box_num)
        qp = QPainter()
        qp.begin(self)
        self.drawMe(qp)
        qp.end()


    #定义判断是否完成函数，返回在正确位置滑块的数目
    def isFinished(self):
        counter = 0
        for i in range(self.box_num ** 2 - 1):
            if self.data[i][1] == i:
                counter += 1
        return counter

    def readResources(self):
        self.data = []
        for i in range(self.box_num ** 2):
            img_num = []
            if self.egg:
                img = img = QImage(f'{self.mode}/{self.level}/{i}.png')
            else:
                img = QImage(f'{self.mode}/{self.level}/{i}.jpg')
            img_num.append(img)
            img_num.append(i)
            self.data.append(img_num)
            

    #画出滑块界面



    def drawMe(self, qp):
        pen = QPen(Qt.white, 1, Qt.SolidLine)
        brush = QBrush(QColor('white'))
        qp.setPen(pen)
        qp.setBrush(brush)
        for i in range(self.box_num):
            for j in range(self.box_num):
                ix = i * self.box_num + j
                if self.data[ix][1] != self.box_num ** 2 - 1:
                    x = SIZE * j
                    y = SIZE * i 
                    qp.drawRect(x, y, SIZE, SIZE)
                    img_scaled = self.data[ix][0].scaled(SIZE, SIZE, Qt.KeepAspectRatio)
                    qp.drawImage(x, y, img_scaled)


    #读出所在滑块的数字
    def getNum(self, i, j):
        if 0 <= i < self.box_num and 0 <= j < self.box_num:
            ix = i * self.box_num + j
            return self.data[ix][1]
        else:
            return -1

    #定义交换函数，交换两个滑块 
    def swap(self, i, j, m, n):
        ix1 = i * self.box_num + j
        ix2 = m * self.box_num + n
        tmp = self.data[ix1][0]
        self.data[ix1][0] = self.data[ix2][0]
        self.data[ix2][0] = tmp
        tmp = self.data[ix1][1]
        self.data[ix1][1] = self.data[ix2][1]
        self.data[ix2][1] = tmp
        if self.isFinished() == self.box_num ** 2 - 1:

            if self.mode_num == 0 and self.level_num == 0:
                self.finished00.emit()
            elif self.mode_num == 0 and self.level_num == 1:
                self.finished01.emit()
            elif self.mode_num == 0 and self.level_num == 2:
                self.finished02.emit()
            elif self.mode_num == 1 and self.level_num == 0:
                self.finished10.emit()
            elif self.mode_num == 1 and self.level_num == 1:
                self.finished11.emit()
            elif self.mode_num == 1 and self.level_num == 2:
                self.finished12.emit()
            elif self.mode_num == 2 and self.level_num == 0:
                self.finished20.emit()
            elif self.mode_num == 2 and self.level_num == 1:
                self.finished21.emit()
            elif self.mode_num == 2 and self.level_num == 2:
                self.finished22.emit()
        self.update()

    #当鼠标点击空白滑块周围的滑块时交换
    def mousePressEvent(self, evt):
        x, y = evt.x(), evt.y()
        j = int(x/SIZE)
        i = int(y/SIZE)
        if 0 <= i < self.box_num and 0 <= j < self.box_num:
            if self.getNum(i-1, j) == self.box_num ** 2 - 1:
                self.swap(i, j, i - 1, j)
            elif self.getNum(i + 1, j) == self.box_num ** 2 - 1:
                self.swap(i, j, i + 1, j)
            elif self.getNum(i, j - 1) == self.box_num ** 2 - 1:
                self.swap(i, j, i, j - 1)
            elif self.getNum(i, j + 1) == self.box_num ** 2 - 1:
                self.swap(i, j, i, j + 1)

    #打乱滑块，因为不能随意打乱，所以定义了三种打乱方式
    def shuffle(self):
        rand = random.randint(0,2)
        rand_list = self.shuffle_list[rand]
        index = -1
        for i in rand_list:
            img_num = []
            if self.egg:
                img = img = QImage(f'{self.mode}/{self.level}/{i}.png')
            else:
                img = QImage(f'{self.mode}/{self.level}/{i}.jpg')
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
        self.level_num = 0
        self.box_num = 3
        self.mode_num = 0
        self.shuffle_list = EASYSHUFFLE
        self.readResources()
        self.update()

    def changeModeToOrdinary(self):
        global SIZE
        SIZE = 150
        self.mode = 'Ordinary'
        self.level = 'Level 1'
        self.level_num = 0
        self.box_num = 4
        self.mode_num = 1
        self.shuffle_list = ORDINARYSHUFFLE
        self.readResources()
        self.update()

        

    def changeModeToHard(self):
        global SIZE
        SIZE = 125
        self.mode = 'Hard'
        self.level = 'Level 1'
        self.level_num = 0
        self.box_num = 5
        self.mode_num = 2
        self.shuffle_list = HARDSHUFFLE
        self.readResources()
        self.update()
   
    def changeLevelTo1(self):
        self.level = 'Level 1'
        self.level_num = 0
        self.readResources()
        self.update()


    def changeLevelTo2(self):
        self.level = 'Level 2'
        self.level_num = 1
        self.readResources()
        self.update()

        

    def changeLevelTo3(self):
        self.level = 'Level 3'
        self.level_num = 2
        self.readResources()
        self.update()

       





class TopWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.state = [[0,0,0],[0,0,0],[0,0,0]]
        self.initSignalSlot()
        self.timer.start(5000)
        self.setWindowIcon(QIcon('game.ico'))
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
        self.setFixedSize(SIZE * self.canvas.box_num + GAP,
         SIZE * self.canvas.box_num + BTNSIZE )



    def initSignalSlot(self):
        self.timer = QTimer(self)
        self.easyButton.clicked.connect(self.onEasy)
        self.ordinaryButton.clicked.connect(self.onOrdinary)
        self.hardButton.clicked.connect(self.onHard)
        self.level1Button.clicked.connect(self.onLevel1)
        self.level2Button.clicked.connect(self.onLevel2)
        self.level3Button.clicked.connect(self.onLevel3)

        self.canvas.finished00.connect(self.onFinished00)
        self.canvas.finished01.connect(self.onFinished01)
        self.canvas.finished02.connect(self.onFinished02)
        self.canvas.finished10.connect(self.onFinished10)
        self.canvas.finished11.connect(self.onFinished11)
        self.canvas.finished12.connect(self.onFinished12)
        self.canvas.finished20.connect(self.onFinished20)
        self.canvas.finished21.connect(self.onFinished21)
        self.canvas.finished22.connect(self.onFinished22)

        self.timer.timeout.connect(self.onTimer)

    def onEasy(self):
        self.canvas.changeModeToEasy()
        self.timer.start(5000)
        QMessageBox.question(self, '消息框', '5秒之后打乱图片', 
        QMessageBox.Ok)
    
    def onOrdinary(self):
        if self.state[1][0]:
            self.canvas.changeModeToOrdinary()
            self.timer.start(5000)
            QMessageBox.question(self, '消息框', '5秒之后打乱图片', 
            QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '未解锁', 
            QMessageBox.Ok)                    

    def onHard(self):
        if self.state[2][0]:
            self.canvas.changeModeToHard()
            self.timer.start(5000)
            QMessageBox.question(self, '消息框', '5秒之后打乱图片', 
            QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '未解锁', 
            QMessageBox.Ok)      

    def onLevel1(self):
        self.canvas.changeLevelTo1()
        self.timer.start(5000)
        QMessageBox.question(self, '消息框', '5秒之后打乱图片', 
        QMessageBox.Ok)        

    def onLevel2(self):
        if self.state[self.canvas.mode_num][1]:
            self.canvas.changeLevelTo2()
            self.timer.start(5000)
            QMessageBox.question(self, '消息框', '5秒之后打乱图片', 
            QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '未解锁', 
            QMessageBox.Ok)                   

    def onLevel3(self):
        if self.state[self.canvas.mode_num][2]:
            self.canvas.changeLevelTo3()
            self.timer.start(5000)
            QMessageBox.question(self, '消息框', '5秒之后打乱图片', 
            QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '未解锁', 
            QMessageBox.Ok)  
    
    def onTimer(self):
        self.canvas.shuffle()
        self.timer.stop()
    
    """ def onFinished(self):
        QMessageBox.question(self, '消息框', '祝贺，成功复原！', QMessageBox.Ok)
 """
    def onFinished00(self):
        if self.canvas.egg:
            QMessageBox.question(self, '消息框', '兄弟盟把保护打在公屏上！', QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '祝贺，成功复原！解锁下一等级！', QMessageBox.Ok)
            self.state[0][1] = 1
    
    def onFinished01(self):
        if self.canvas.egg:
            QMessageBox.question(self, '消息框', '觉得艺术的把艺术打在公屏上！', QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '祝贺，成功复原！解锁下一等级！', QMessageBox.Ok)
            self.state[0][2] = 1
    
    def onFinished02(self):
        if self.canvas.egg:
            QMessageBox.question(self, '消息框', '兄弟盟艺术需要支持！', QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '祝贺，成功复原！解锁普通模式！', QMessageBox.Ok)
            self.state[1][0] = 1
    def onFinished10(self):
        if self.canvas.egg:
            QMessageBox.question(self, '消息框', '宁看我，那我也看宁！', QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '祝贺，成功复原！解锁下一等级！', QMessageBox.Ok)
            self.state[1][1] = 1
    
    def onFinished11(self):
        if self.canvas.egg:
            QMessageBox.question(self, '消息框', '兄弟盟艺术需要支持！', QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '祝贺，成功复原！解锁下一等级！', QMessageBox.Ok)
            self.state[1][2] = 1
    
    def onFinished12(self):
        if self.canvas.egg:
            QMessageBox.question(self, '消息框', '兄弟盟把保护打在公屏上！', QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '祝贺，成功复原！解锁困难模式！', QMessageBox.Ok)
            self.state[2][0] = 1
    def onFinished20(self):
        if self.canvas.egg:
            QMessageBox.question(self, '消息框', '兄弟盟艺术需要支持！', QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '祝贺，成功复原！解锁下一等级！', QMessageBox.Ok)
            self.state[2][1] = 1
    
    def onFinished21(self):
        if self.canvas.egg:
            QMessageBox.question(self, '消息框', '兄弟盟把保护打在公屏上！', QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '祝贺，成功复原！解锁下一等级！', QMessageBox.Ok)
            self.state[2][2] = 1
    
    def onFinished22(self):
        if self.canvas.egg:
            QMessageBox.question(self, '消息框', '觉得艺术的把艺术打在公屏上！', QMessageBox.Ok)
        else:
            QMessageBox.question(self, '消息框', '你是搞黄色的吗，这么厉害 你以为结束了？游戏才刚刚开始，解锁带制作模式！', QMessageBox.Ok)
            self.canvas.egg = 1

app = QApplication(sys.argv)
w = TopWindow()
w.show()
app.exec_()
