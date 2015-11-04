import sys, random, numpy
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont, QFontMetrics, QPen, QPixmap, QFontDatabase
from PyQt5.QtMultimedia import QSound

SCREENWIDTH = 1280
SCREENHEIGHT = 1024
NUMWORDS = 20
MARGIN = 50

class SkyShoot(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):    

        self.playfield = Field(self)
        self.setCentralWidget(self.playfield)

        # status bar?
        
        self.playfield.start()
        
        self.resize(SCREENWIDTH, SCREENHEIGHT)
        self.center()
        self.setWindowTitle('SynoMaster SkyShoot')        
        self.show()
        

    def center(self):
        
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)
        

class Field(QFrame):
    
#    msg2Statusbar = pyqtSignal(str)
    
    Speed = 10

    def __init__(self, parent):
        super().__init__(parent)

        palette = self.palette()
        palette.setColor( palette.Window, QColor( 0, 0, 0 ) )
        self.setPalette( palette )
        self.setAutoFillBackground(True)
        self.loadWords()

        self.initField()

    def loadWords(self):

        f = open("slush.txt")
        string = f.read()
        self.entries = [0 for x in range(len(string.splitlines()))]

        for index, line in enumerate(string.splitlines()):
            self.entries[index] = line.split(',')
            for x in range(3):
                self.entries[index][x].strip()

#  first word entries[x][0] second word entries[x][1] meaning entries[x][2]


    def initField(self):     

        self.timer = QBasicTimer()
        QFontDatabase.addApplicationFont("Keystone Normal.ttf")

        self.font = QFont('Decorative', 22) # 'Keystone'
        self.metrics = QFontMetrics(self.font)
#        print(self.metrics.width(self.entries[11][2]))
#        print(self.metrics.boundingRect(self.entries[11][2]).width())
        self.topxvalues = [0 for x in range(NUMWORDS)]
#        print(self.metrics.boundingRect('sconsequemtials').width())
        
        self.topSpaceBetween = 50
        cursor = 0
        for i in range(NUMWORDS):
            self.topxvalues[i] = cursor - self.metrics.boundingRect(self.entries[i][0]).width() - self.topSpaceBetween
            cursor = self.topxvalues[i]
#            print(self.xvalues[i])
#        print(self.metrics.boundingRect(self.entries[4][1]))
#        print(self.metrics.boundingRect(self.entries[4][1]).top())
#        print(self.metrics.boundingRect(self.entries[4][1]).topLeft())
#        print(self.metrics.boundingRect(self.entries[4][1]).bottomRight())
        self.bulletLength = 100
        self.shooting = False
        self.distanceShot = 0

        # spread bottomwords out in terms of length

        self.bottomWords = [0 for x in range(NUMWORDS)]
        self.temp = [0 for x in range(NUMWORDS)]

        for i in range(NUMWORDS):
            self.bottomWords[i] = self.entries[i][1]

        self.bottomWords.sort(key=len, reverse=True)

        for i in range(int(NUMWORDS/2)):
            self.temp[i*2] = self.bottomWords[i]

        for i in range(int(NUMWORDS/2)):
            self.temp[1+i*2] = self.bottomWords[NUMWORDS-1-i]

        self.bottomWords = self.temp

        self.rowSize = int(NUMWORDS/4)
        self.bottomSpaceBetween = [0 for x in range(4)]
        for i in range(4):
            self.bottomSpaceBetween[i] = 0
            for x in range(self.rowSize):
                self.bottomSpaceBetween[i] += self.metrics.boundingRect(self.bottomWords[i * self.rowSize + x]).width()
            self.bottomSpaceBetween[i] = int((SCREENWIDTH - 2 * MARGIN - self.bottomSpaceBetween[i])/4)

        print(self.bottomSpaceBetween)

        self.bottomxvalues = [0 for x in range(NUMWORDS)]

        for i in range(4): # 4 rows
            cursor = MARGIN
            for x in range(self.rowSize):
                self.bottomxvalues[i * self.rowSize + x] = cursor
                cursor += self.metrics.boundingRect(self.bottomWords[i * self.rowSize + x]).width() + self.bottomSpaceBetween[i]

#        print(self.bottomxvalues)        

#        self.spaceBetweenBottomWords = int((SCREENWIDTH - 2 * MARGIN) / (NUMWORDS/4))
#        print(self.spaceBetweenBottomWords)
#        print(self.temp)
#        print(self.bottomWords)

#        self.shot = QSound("sound2.wav")
        self.setFocusPolicy(Qt.StrongFocus)

        self.pixmap = QPixmap("logo.png")
        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)
        self.lbl.move(int(SCREENWIDTH/2-self.pixmap.width()/2), MARGIN)
        print(self.pixmap.width())
        
    def start(self):
        
        self.clearBoard()

        self.timer.start(Field.Speed, self)

    def paintEvent(self, event):
        
        painter = QPainter(self)
#        rect = self.contentsRect()
#        painter.begin(self)

        self.drawText(event, painter)
#        painter.end()
        
        
    def drawText(self, event, painter):
      
        painter.setPen(QColor(188, 54, 23))
        painter.setFont(self.font)

        for i in range(NUMWORDS):
            if (self.topxvalues[i] > -300) and (self.topxvalues[i] < SCREENWIDTH):
                painter.drawText(self.topxvalues[i],200, self.entries[i][0]) 
            elif(self.topxvalues[i] >= SCREENWIDTH) and (self.topxvalues[i] < SCREENWIDTH * 2):
                painter.drawText(self.topxvalues[i] - SCREENWIDTH,300, self.entries[i][0]) 
            elif(self.topxvalues[i] >= SCREENWIDTH * 2) and (self.topxvalues[i] < SCREENWIDTH * 3):
                painter.drawText(self.topxvalues[i] - SCREENWIDTH * 2,400, self.entries[i][0]) 
        
        for i in range(NUMWORDS):
            if i in range(self.rowSize):
                painter.drawText(self.bottomxvalues[i], 650, self.bottomWords[i]) 
            elif i < (self.rowSize*2):
                painter.drawText(self.bottomxvalues[i], 750, self.bottomWords[i]) 
            elif i < (self.rowSize*3):
                painter.drawText(self.bottomxvalues[i], 850, self.bottomWords[i]) 
            else:
                painter.drawText(self.bottomxvalues[i], 950, self.bottomWords[i]) 

        
#        painter.setBrush(QColor(25,0,90))
#        painter.drawRect(100, 100, 400, 400)

        if self.shooting is True:
            pen = QPen(Qt.white, 2, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(SCREENWIDTH/2, 450 - self.metrics.boundingRect(self.entries[4][1]).height() - self.distanceShot, SCREENWIDTH/2, 450 - self.metrics.boundingRect(self.entries[4][1]).height() - self.distanceShot-self.bulletLength)


    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():
            for i in range(NUMWORDS):
                self.topxvalues[i] += 1
            for i in range(NUMWORDS):
                if self.topxvalues[i] >= SCREENWIDTH * 3:
                    self.topxvalues[i] = min(self.topxvalues) - self.metrics.boundingRect(self.entries[i][0]).width() - self.topSpaceBetween
            if self.shooting is True:
                self.distanceShot += 10
                if self.distanceShot > SCREENHEIGHT/2:
                    self.shooting = False
            self.update()

        
        super(Field, self).timerEvent(event)

            
    def clearBoard(self):
        
        pass

    def mousePressEvent(self, QMouseEvent):
#        if self.metrics.boundingRect(self.entries[4][1]).contains(QMouseEvent.pos()):
#        print(QMouseEvent.pos())
#        print(self.metrics.boundingRect(self.entries[4][1]))
#        print(self.metrics.boundingRect(self.entries[4][1]).center())
        if self.metrics.boundingRect(self.entries[4][1]).adjusted(SCREENWIDTH/2 - self.metrics.boundingRect(self.entries[4][1]).width()/2, 450,SCREENWIDTH/2 - self.metrics.boundingRect(self.entries[4][1]).width()/2, 450).contains(QMouseEvent.pos()):
            self.shooting = True
            self.distanceShot = 0
 #           self.shot.play()
# ["foo", "bar", "baz"].index("bar")
        return super().mousePressEvent(QMouseEvent)
        
        
if __name__ == '__main__':
    
    app = QApplication([])
    tetris = SkyShoot()    
    sys.exit(app.exec_())