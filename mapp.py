import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QWidget, QGridLayout, QMenu, QLineEdit, QVBoxLayout, QCheckBox
from PySide6.QtGui import Qt, QShowEvent, QKeyEvent, QResizeEvent, QCloseEvent, QPixmap
from PySide6.QtCore import QCoreApplication, Signal, Slot, QObject
import sys
from PIL import Image, ImageQt
from dataclasses import dataclass, field

tr = QCoreApplication.translate


class Data(QObject):
  currentDir: str = "."
  index: int = 0
  images: list[str] = []
  img: Image = None
  imgUpdateSig = Signal()
  tagsChanged = Signal()
  tags: list[str] = []

  def init(self):
    self.open_dir()

  def open_dir(self):
    flist = os.listdir(self.currentDir)
    self.images = list(filter(self.isImage, flist))
    self.index = 0
    self.img = self.getImg(True)
    self.imgUpdateSig.emit()

  def append_tag(self, tag):
    self.tags.append(tag)
    self.tagsChanged.emit()

  def next(self):
    if len(self.images) <= 0:
      return
    self.index = (self.index + 1) % len(self.images)
    self.img = self.getImg(True)
    self.imgUpdateSig.emit()

  def pre(self):
    if len(self.images) <= 0:
      return
    self.index = (self.index - 1) % len(self.images)
    self.img = self.getImg(True)
    self.imgUpdateSig.emit()

  def getImg(self, update=False) -> QPixmap:
    if len(self.images) > 0 and update:
      self.img = Image.open(
          os.path.join(self.currentDir, self.images[self.index]))
      self.img = ImageQt.toqpixmap(self.img)
    return self.img

  def isImage(self, fname):
    return os.path.splitext(fname)[1].lower() in [
        ".jpg", ".png", ".jpeg", ".webp"
    ]


class App(QMainWindow):
  ctx: str = "MainMenu"

  def __init__(self):
    super(App, self).__init__()
    self.data = Data()
    self.data.init()
    self.init_gui()

  def tr(self, txt):
    return tr(self.ctx, txt)

  def init_gui(self):
    self.setWindowTitle(self.tr("Image Tagger"))
    self.resize(600, 400)
    self.mainWidget = QWidget()
    self.mainWidget.setStyleSheet("margin: 0px; padding: 0px;")
    self.mainLayout = QGridLayout()
    self.mainLayout.setSpacing(0)
    self.mainLayout.setContentsMargins(0, 0, 0, 0)
    self.mainWidget.setLayout(self.mainLayout)
    self.mainLayout.setColumnStretch(0, 9)
    self.mainLayout.setColumnStretch(1, 1)
    self.mainLayout.setColumnMinimumWidth(0, 350)
    self.mainLayout.setColumnMinimumWidth(1, 150)
    self.mainLayout.setRowMinimumHeight(0, 400)

    # Image Label
    self.imageLabel = QLabel()
    self.imageLabel.setAlignment(Qt.AlignCenter)
    self.imageLabel.setMinimumSize(100, 100)
    self.mainLayout.addWidget(self.imageLabel, 0, 0)

    # Sidebar
    self.sideBar = QWidget()
    self.sideBarLayout = QVBoxLayout()
    self.sideBarLayout.setAlignment(Qt.AlignTop)
    self.sideBar.setLayout(self.sideBarLayout)
    # tagEdit
    self.tagEdit = QLineEdit()
    self.tagEdit.returnPressed.connect(self.tagEditReturnPressed)
    self.tagEdit.setPlaceholderText(self.tr("Enter tag"))
    self.sideBarLayout.addWidget(self.tagEdit)
    # tagList
    self.tagList = QWidget()
    self.tagListLayout = QVBoxLayout()
    self.tagListItems: list[QWidget] = []
    self.tagListLayout.setAlignment(Qt.AlignTop)
    self.tagList.setLayout(self.tagListLayout)
    self.updateTags()
    self.sideBarLayout.addWidget(self.tagList)

    self.mainLayout.addWidget(self.sideBar, 0, 1)

    self.fileMenu = QMenu(self.tr("File"))
    self.fileMenu.addAction(self.tr("Open"), self.open_file)
    self.fileMenu.addAction(self.tr("File"), self.exit)
    self.menuBar().addMenu(self.fileMenu)

    # signals
    self.data.imgUpdateSig.connect(lambda: self.updateImg())
    self.data.tagsChanged.connect(lambda: self.updateTags())

    self.setCentralWidget(self.mainWidget)

  def open_file(self):
    dir = QFileDialog.getExistingDirectory(self, self.tr("Open Directory"))
    if not dir:
      return
    self.data.currentDir = dir
    self.data.open_dir()

  def closeEvent(self, event: QCloseEvent) -> None:
    return super().closeEvent(event)

  def exit(self):
    QCoreApplication.quit()

  def tagEditReturnPressed(self):
    tag = self.tagEdit.text()
    if tag:
      self.data.append_tag(tag)
    self.tagEdit.setText("")

  def showEvent(self, event: QShowEvent) -> None:
    super().showEvent(event)
    self.updateImg(True)

  def keyPressEvent(self, event: QKeyEvent) -> None:
    super().keyPressEvent(event)
    key = event.key()
    if key == Qt.Key_Right:
      self.data.next()
    elif key == Qt.Key_Left:
      self.data.pre()

  def resizeEvent(self, event: QResizeEvent) -> None:
    super().resizeEvent(event)
    self.updateImg()

  def updateImg(self, update=False):
    img = self.data.getImg(update)
    size = self.imageLabel.size()
    img = img.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    self.imageLabel.setPixmap(img)

  def updateTags(self):
    tags = self.data.tags
    for item in self.tagListItems:
      self.tagListLayout.removeWidget(item)
    self.tagListItems.clear()
    for tag in tags:
      item = QCheckBox(tag)
      # item.setAlignment(Qt.AlignCenter)
      item.setMinimumSize(100, 20)
      self.tagListLayout.addWidget(item)
      self.tagListItems.append(item)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  w = App()
  w.show()
  sys.exit(app.exec())
