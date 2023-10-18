import cv2
from PyQt6 import QtCore
from PyQt6.QtGui import QImage
from ObjectDetection.Detector import Detector


class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(QImage)
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.running = False  # Флаг выполнения
        self.detector = Detector()
        self.capture = None
        self.play_pause=False
        self.image = cv2.imread("D:\PythonProjects\YOLO888\media\work.PNG")


    def run(self):
        self.running = True
        while self.running:   # Проверяем значение флага
            if self.play_pause:
                # print(self.play_pause)
                ret, self.image = self.capture.read()
                self.returnImage(self.image)
            else:
                self.image = cv2.imread("D:\PythonProjects\YOLO888\media\work6.PNG")
                self.returnImage(self.image)

                self.sleep(1)

    def returnImage(self, image):
        try:
            image = self.detector.weapon_detect(image)
        except Exception as e:
            print(e)
        qformat = QImage.Format.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format.Format_RGBA8888
            else:
                qformat = QImage.Format.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        self.mysignal.emit(outImage)
