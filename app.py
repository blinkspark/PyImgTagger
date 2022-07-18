import sys, os
from PySide6 import QtCore, QtWidgets, QtGui, QtQuick
from ImageViewer import Ui_MainWindow


class App(QtWidgets.QMainWindow):

    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.imageLabel.setMinimumSize(1, 1)
        self.ui.actionOpen.triggered.connect(self.openFolderDialog)
        self.currentFolder = "."
        self.imgIndex = 0

        self.openFolder(self.currentFolder)

    def openFolder(self, folder: str):
        files = os.listdir(folder)
        self.files = list(filter(self.isImage, files))
        self.picName = self.files[self.imgIndex]
        self.pixmap = QtGui.QPixmap(os.path.join(folder, self.picName))
        self.updateAll()

    def isImage(self, fname: str):
        return os.path.splitext(fname)[1].lower() in [
            ".jpg", '.jpeg', '.png', '.webp'
        ]

    def openFolderDialog(self) -> None:
        targetDir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Open Directory", "")
        if targetDir:
            self.currentFolder = targetDir
            self.openFolder(self.currentFolder)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        key = event.key()
        if QtGui.Qt.Key_Left == key:
            self.imgIndex = (self.imgIndex - 1) % len(self.files)
            self.pixmap = QtGui.QPixmap(
                os.path.join(self.currentFolder, self.files[self.imgIndex]))
            self.updateAll()
        elif QtGui.Qt.Key_Right == key:
            self.imgIndex = (self.imgIndex + 1) % len(self.files)
            self.pixmap = QtGui.QPixmap(
                os.path.join(self.currentFolder, self.files[self.imgIndex]))
            self.updateAll()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        print(event.size())
        self.updateImg()
        super().resizeEvent(event)

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        self.updateImg()
        super().showEvent(event)

    def updateImg(self) -> None:
        pixmap = self.pixmap.scaled(self.ui.imageLabel.size(),
                                    QtCore.Qt.KeepAspectRatio,
                                    QtCore.Qt.SmoothTransformation)
        self.ui.imageLabel.setPixmap(pixmap)

    def updateStatusBar(self) -> None:
        self.ui.statusbar.showMessage(
            self.files[self.imgIndex] +
            f' ({self.imgIndex + 1}/{len(self.files)})')

    def updateAll(self) -> None:
        self.updateStatusBar()
        self.updateImg()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()

    sys.exit(app.exec())