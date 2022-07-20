import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QWidget, QGridLayout, QMenu
from PySide6.QtGui import Qt
from PySide6.QtCore import QCoreApplication
import sys
from PIL import Image, ImageQt
from dataclasses import dataclass, field

tr = QCoreApplication.translate


@dataclass
class Data:
  currentDIr: str = "."
  index: int = 0
  images: list[str] = field(default_factory=list)
  img: Image = None

  def openDir(self):
    flist = os.listdir(self.currentDIr)
    self.images = list(filter(self.isImage, flist))
    self.index = 0

  def isImage(self, fname):
    return os.path.splitext(fname)[1].lower() in [
        ".jpg", ".png", ".jpeg", ".webp"
    ]


class App(QMainWindow):

  def __init__(self):
    super(App, self).__init__()
    self.data = Data()
    self.init_gui()

  def init_gui(self):
    self.setWindowTitle("Image Tagger")
    self.resize(600, 400)
    self.mainWidget = QWidget()
    self.mainWidget.setStyleSheet("margin: 0px; padding: 0px;")
    self.mainLayout = QGridLayout()
    self.mainLayout.setSpacing(0)
    self.mainLayout.setContentsMargins(0, 0, 0, 0)
    self.mainWidget.setLayout(self.mainLayout)
    self.mainLayout.setColumnStretch(0, 8)
    self.mainLayout.setColumnStretch(1, 2)
    self.mainLayout.setColumnMinimumWidth(0, 400)
    self.mainLayout.setColumnMinimumWidth(1, 200)

    self.imageLabel = QLabel("Test")
    self.imageLabel.setAlignment(Qt.AlignCenter)
    self.imageLabel.setStyleSheet("background-color: blue")
    self.mainLayout.addWidget(self.imageLabel, 0, 0)

    self.testLabel = QLabel("Test")
    self.testLabel.setStyleSheet("background-color: red")
    self.testLabel.setAlignment(Qt.AlignCenter)
    self.mainLayout.addWidget(self.testLabel, 0, 1)


    self.fileMenu = QMenu("File")
    self.fileMenu.addAction("Open", self.open_file)
    self.fileMenu.addAction("Exit", self.exit)
    self.menuBar().addMenu(self.fileMenu)

    self.setCentralWidget(self.mainWidget)

  def open_file(self):
    print("Open dir")
    testLa = QLabel("Test")
    testLa.setStyleSheet("background-color: yellow")
    self.mainLayout.addWidget(testLa, 0, 2)

  def exit(self):
    print("Exit")
    QCoreApplication.quit()


if __name__ == "__main__":
  app = QApplication(sys.argv)
  w = App()
  w.show()
  sys.exit(app.exec())
