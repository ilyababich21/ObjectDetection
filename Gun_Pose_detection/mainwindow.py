import sys
from pathlib import Path

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.uic import loadUi

# import resource
# from model import Model
from out_window import Ui_OutputDialog


class Ui_Dialog(QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        loadUi("mainwindow.ui", self)
        self.label.setPixmap(QPixmap("logo.png"))
        self.runButton.clicked.connect(self.runSlot)
        print(Path(__file__).resolve().parent.parent)
        self._new_window = None
        self.Videocapture_ = None

    @pyqtSlot()
    def runSlot(self):
        """
        Called when the user presses the Run button
        """
        print("Clicked Run")

        ui.hide()  # hide the main window
        self.outputWindow_()  # Create and open new output window

    def outputWindow_(self):
        """
        Created new window for vidual output of the video in GUI
        """
        self._new_window = Ui_OutputDialog()
        self._new_window.show()
        # self._new_window.startVideo(self.Videocapture_)
        print("Video Played")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec())
