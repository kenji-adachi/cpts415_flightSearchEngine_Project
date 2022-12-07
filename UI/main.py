import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

qtCreatorFile = "mainwindow.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class flightMainwindow(QMainWindow):
    def __init__(self):
        super(flightMainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.button1.clicked.connect(self.updateText)

    def updateText(self):
        print("pushed")
        self.ui.label1.setText(self.ui.insertedTextBox.text())
        self.ui.insertedTextBox.clear()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = flightMainwindow()
    window.show()
    sys.exit(app.exec_())