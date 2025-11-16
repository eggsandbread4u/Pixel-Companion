import sys 
import ctypes # let's you interact with window os
from ctypes import windll, wintypes, byref
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random

# allows python to communicate with window api
class appbar(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD), 
        ("hWnd", wintypes.HWND),
        ("uEdge", wintypes.UINT), 
        ("rc", wintypes.RECT)        
    ]
# interact with taskbar and asks to get taskbar position
class grab_taskbar():
    SHAppBarMessage = ctypes.windll.shell32.SHAppBarMessage
    bar_pos = 0x00000005 
    def get_coords(self):
        appbar_data = appbar()
        # setting size for the container where taskbar pos will be stored
        appbar_data.cbSize = ctypes.sizeof(appbar)
        # requests window api to give pos and not only read our request 
        output = self.SHAppBarMessage(self.bar_pos, ctypes.byref(appbar_data))
        # return nothing if request failed
        if not output:
            return None
        # if yes we get coordinates
        rect = appbar_data.rc 
        return rect.left, rect.top, rect.right, rect.bottom
    
# main window
class image_girl(QWidget):
    def __init__(self):
        super().__init__()
        # frameless window with transparent background
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.offset = None
        self.setMouseTracking(True)
        self.dragging = False

        # girl image
        self.image = QPixmap("girl.png")
        if self.image.isNull():
            print("failed to load")   
        self.image = self.image.scaled(282, 282, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setFixedSize(self.image.width(), self.image.height())

        # for dialogue
        self.dialogue_words = ["You got this!", "Keep it up!", "Don't give up yet!",
                               "more to come!", "You can do this!", "Wow, you've made it this far",
                               "so proud of you!", "Don't lose hope!"]
        self.current_words = random.choice(self.dialogue_words)
        self.dialogue_image = QPixmap("dialogue.png")
        self.dialogue_image = self.dialogue_image.scaled(162, 162, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setFixedSize(self.image.width() + self.dialogue_image.width() + 10, self.image.height())

        self.place_on_taskbar()
    # where our girl image will be standing
    def place_on_taskbar(self):
        GETWORKAREA = 0x0030
        rect = wintypes.RECT()
        windll.user32.SystemParametersInfoW(GETWORKAREA, 0, byref(rect), 0)
        x = rect.left + 20
        y = rect.bottom - self.height() + 50
        self.move(x, y) 

    # when press left mouse dialogue changes
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.current_words = random.choice(self.dialogue_words)
            self.update()
        elif event.button() == Qt.RightButton:
            self.dragging = True
            self.offset = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.dragging = False
                               
    # draw girl image
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.image)
        # setting the dialogue image and font
        dialogue_x = self.image.width() - 100
        dialogue_y = 5
        painter.drawPixmap(dialogue_x, dialogue_y, self.dialogue_image)
        painter.setPen(Qt.black)
        font_id = QFontDatabase.addApplicationFont("PixelifySans.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.setFont(QFont(font_family, 10))
        text_rect = QRect(dialogue_x + 10, dialogue_y + 10, 
                          self.dialogue_image.width() - 30, 
                          self.dialogue_image.height() - 40)                      
        text_rect.moveTo(dialogue_x + 10, dialogue_y + 10)
        painter.drawText(text_rect, Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWordWrap, self.current_words)
                 
if __name__ == '__main__':
    figure = QApplication(sys.argv)
    window = image_girl()
    window.show()
    sys.exit(figure.exec())        
