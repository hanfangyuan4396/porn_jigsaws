import sys
import random
from PyQt4.QtGui import *
from PyQt4.QtCore import *

 #滑块的间隔和每个滑块的大小
# GAP = 2
SIZE = 170
mode = 'init'
#定义一个滑块窗口的类
class BlockWindow(QWidget):

    #在类的层面定义变量，作为信号
    finished = pyqtSignal()

    #初始化窗口，data列表，窗口最小尺寸
    def __init__(self, parent = None):
        super().__init__(parent)
        self.readResources()
        self.setMinimumSize(SIZE * 4, SIZE * 4)

    #重写函数，画界面
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawMe(qp)
        qp.end()


    #定义判断是否完成函数，返回在正确位置滑块的数目
    def isFinished(self):
        counter = 0
        for i in range(15):
            if self.data[i][1] == i:
                counter += 1
        return counter

    def readResources(self):
        self.data = []
        for i in range(16):
            img_num = []
            img = QImage(f'{i}.jpg')
            img_num.append(img)
            img_num.append(i)
            self.data.append(img_num)
            

    #画出滑块界面



    def drawMe(self, qp):
        pen = QPen(Qt.white, 1, Qt.SolidLine)
        brush = QBrush(QColor('white'))
        qp.setPen(pen)
        qp.setBrush(brush)
        for i in range(4):
            for j in range(4):
                ix = i * 4 + j
                if self.data[ix][1] != 15:
                    x = SIZE * j
                    y = SIZE * i 
                    qp.drawRect(x, y, SIZE, SIZE)
                    img_scaled = self.data[ix][0].scaled(SIZE, SIZE, Qt.KeepAspectRatio)
                    qp.drawImage(x, y, img_scaled)


    #读出所在滑块的数字
    def getNum(self, i, j):
        if 0 <= i < 4 and 0 <= j < 4:
            ix = i * 4 + j
            return self.data[ix][1]
        else:
            return -1

    #定义交换函数，交换两个滑块 
    def swap(self, i, j, m, n):
        ix1 = i * 4 + j
        ix2 = m * 4 + n
        tmp = self.data[ix1][0]
        self.data[ix1][0] = self.data[ix2][0]
        self.data[ix2][0] = tmp
        tmp = self.data[ix1][1]
        self.data[ix1][1] = self.data[ix2][1]
        self.data[ix2][1] = tmp
        if self.isFinished() == 15:
            self.finished.emit()
        self.update()

    #当鼠标点击空白滑块周围的滑块时交换
    def mousePressEvent(self, evt):
        x, y = evt.x(), evt.y()
        j = int(x/SIZE)
        i = int(y/SIZE)
        if 0 <= i < 4 and 0 <= j < 4:
            if self.getNum(i-1, j) == 15:
                self.swap(i, j, i - 1, j)
            elif self.getNum(i + 1, j) == 15:
                self.swap(i, j, i + 1, j)
            elif self.getNum(i, j - 1) == 15:
                self.swap(i, j, i, j - 1)
            elif self.getNum(i, j + 1) == 15:
                self.swap(i, j, i, j + 1)

    #打乱滑块，因为不能随意打乱，所以定义了三种打乱方式
    def shuffle(self):
        rand = random.randint(1,3)
        if rand == 1:
            shuffle_list = [1,7,5,4,6,0,10,2,8,13,3,11,9,14,12,15]
            index = -1
            for i in shuffle_list:
                img_num = []
                img = QImage(f'{i}.jpg')
                img_num.append(img)
                img_num.append(i)
                index = index + 1
                self.data[index] = img_num
        elif rand == 2:
            shuffle_list = [4,1,3,11,0,2,6,9,8,13,5,14,7,10,13,15]
            index = -1
            for i in shuffle_list:
                img_num = []
                img = QImage(f'{i}.jpg')
                img_num.append(img)
                img_num.append(i)
                index = index + 1
                self.data[index] = img_num

        elif rand == 3:
            shuffle_list = [12,1,2,9,6,0,7,4,14,8,5,3,13,10,11,15]
            index = -1
            for i in shuffle_list:
                img_num = []
                img = QImage(f'{i}.jpg')
                img_num.append(img)
                img_num.append(i)
                index = index + 1
                self.data[index] = img_num

        self.update()

#定义一个顶层窗口的类，包括滑块窗口的画布和一个按钮
class TopWindow(QWidget):

    #初始化界面，槽函数
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initSingalSlot()
        self.setWindowTitle('滑块')

    #初始化界面
    def initUI(self):
        vLayout = QVBoxLayout()
        self.canvas = BlockWindow(self)
        self.shuffleButton = QPushButton('shuffle', self)

        vLayout.addWidget(self.canvas, stretch = 1)
        vLayout.addWidget(self.shuffleButton)

        self.setLayout(vLayout)

    #槽函数，点击按钮时打乱，成功复原时弹出消息框
    def initSingalSlot(self):
        self.shuffleButton.clicked.connect(self.onShuffle)
        self.canvas.finished.connect(self.onFinished)

    def onShuffle(self, evt):
        self.canvas.shuffle()

    def onFinished(self):
        QMessageBox.question(self, '消息框', '祝贺，成功复原！', QMessageBox.Ok)
    
class initWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        vLayout = QVBoxLayout()
        self.easyButton = QPushButton('easy', self)
        self.ordinaryButton = QPushButton('ordinary',self)
        self.hardButton = QPushButton('hard', self)
        vLayout.addWidget(self.easyButton)
        vLayout.addWidget(self.ordinaryButton)
        vLayout.addWidget(self.hardButton)
        self.setLayout(vLayout)
        self.setMinimumSize(SIZE * 2, SIZE * 2)


class easyWindow(QWidget):
    finished = pyqtSignal()

    #初始化窗口，data列表，窗口最小尺寸
    def __init__(self, parent = None):
        super().__init__(parent)
        self.readResources()
        self.setMinimumSize(SIZE * 4, SIZE * 4)

    #重写函数，画界面
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawMe(qp)
        qp.end()


    #定义判断是否完成函数，返回在正确位置滑块的数目
    def isFinished(self):
        counter = 0
        for i in range(15):
            if self.data[i][1] == i:
                counter += 1
        return counter

    def readResources(self):
        self.data = []
        for i in range(16):
            img_num = []
            img = QImage(f'{i}.jpg')
            img_num.append(img)
            img_num.append(i)
            self.data.append(img_num)
            

    #画出滑块界面



    def drawMe(self, qp):
        pen = QPen(Qt.white, 1, Qt.SolidLine)
        brush = QBrush(QColor('white'))
        qp.setPen(pen)
        qp.setBrush(brush)
        for i in range(4):
            for j in range(4):
                ix = i * 4 + j
                if self.data[ix][1] != 15:
                    x = SIZE * j
                    y = SIZE * i 
                    qp.drawRect(x, y, SIZE, SIZE)
                    img_scaled = self.data[ix][0].scaled(SIZE, SIZE, Qt.KeepAspectRatio)
                    qp.drawImage(x, y, img_scaled)


    #读出所在滑块的数字
    def getNum(self, i, j):
        if 0 <= i < 4 and 0 <= j < 4:
            ix = i * 4 + j
            return self.data[ix][1]
        else:
            return -1

    #定义交换函数，交换两个滑块 
    def swap(self, i, j, m, n):
        ix1 = i * 4 + j
        ix2 = m * 4 + n
        tmp = self.data[ix1][0]
        self.data[ix1][0] = self.data[ix2][0]
        self.data[ix2][0] = tmp
        tmp = self.data[ix1][1]
        self.data[ix1][1] = self.data[ix2][1]
        self.data[ix2][1] = tmp
        if self.isFinished() == 15:
            self.finished.emit()
        self.update()

    #当鼠标点击空白滑块周围的滑块时交换
    def mousePressEvent(self, evt):
        x, y = evt.x(), evt.y()
        j = int(x/SIZE)
        i = int(y/SIZE)
        if 0 <= i < 4 and 0 <= j < 4:
            if self.getNum(i-1, j) == 15:
                self.swap(i, j, i - 1, j)
            elif self.getNum(i + 1, j) == 15:
                self.swap(i, j, i + 1, j)
            elif self.getNum(i, j - 1) == 15:
                self.swap(i, j, i, j - 1)
            elif self.getNum(i, j + 1) == 15:
                self.swap(i, j, i, j + 1)

    #打乱滑块，因为不能随意打乱，所以定义了三种打乱方式
    def shuffle(self):
        rand = random.randint(1,3)
        if rand == 1:
            shuffle_list = [1,7,5,4,6,0,10,2,8,13,3,11,9,14,12,15]
            index = -1
            for i in shuffle_list:
                img_num = []
                img = QImage(f'{i}.jpg')
                img_num.append(img)
                img_num.append(i)
                index = index + 1
                self.data[index] = img_num
        elif rand == 2:
            shuffle_list = [4,1,3,11,0,2,6,9,8,13,5,14,7,10,13,15]
            index = -1
            for i in shuffle_list:
                img_num = []
                img = QImage(f'{i}.jpg')
                img_num.append(img)
                img_num.append(i)
                index = index + 1
                self.data[index] = img_num

        elif rand == 3:
            shuffle_list = [12,1,2,9,6,0,7,4,14,8,5,3,13,10,11,15]
            index = -1
            for i in shuffle_list:
                img_num = []
                img = QImage(f'{i}.jpg')
                img_num.append(img)
                img_num.append(i)
                index = index + 1
                self.data[index] = img_num

        self.update()    



class TopWindow_v2(QWidget):
    
    #初始化界面，槽函数
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initSingalSlot()
        self.setWindowTitle('beautifulgame')
    #初始化界面
    def initUI(self):

        if mode == 'init':
            vLayout = QVBoxLayout()
            self.canvas = initWindow(self)
            vLayout.addWidget(self.canvas)
            self.setLayout(vLayout)
            

        elif mode == 'easy':
            vLayout = QVBoxLayout()
            self.canvas = easyWindow(self)
            vLayout.addWidget(self.canvas)
            self.setLayout(vLayout)
            

        elif mode == 'ordinary':
            vLayout = QVBoxLayout()
            self.canvas = ordinaryWindow(self)
            vLayout.addWidget(self.canvas)
            self.setLayout(vLayout)

        elif mode == 'hard':
            vLayout = QVBoxLayout()
            self.canvas = hardWindow(self)
            vLayout.addWidget(self.canvas)
            self.setLayout(vLayout)            



    #槽函数，点击按钮时打乱，成功复原时弹出消息框
    def initSingalSlot(self):
        print(mode)
        if mode == 'init':
            self.canvas.easyButton.clicked.connect(self.onEasy)
    
    def onEasy(self):
        global mode
        mode = 'easy'
        self.update()













app = QApplication(sys.argv)
w = TopWindow_v2()
w.show()
app.exec_()
