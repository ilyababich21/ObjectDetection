# Modified by Augmented Startups & Geeky Bee
# October 2020
# Facial Recognition Attendence GUI
# Full Course - https://augmentedstartups.info/yolov4release
# *-
import time
from pathlib import Path

import cv2
import numpy as np
import datetime
import os
from ultralytics import YOLO
from PyQt6.QtCore import pyqtSlot, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QDialog, QColorDialog, QFileDialog
from PyQt6.uic import loadUi
from ObjectDetection.Detector import Detector


class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("outputwindow.ui", self)
        self.image = None
        self.detector = Detector()
        self.capture = None
        self.video_address = ''
        self.pause = False

        self.timer = QTimer(self)  # Create Timer
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function

        self.colorButtonPose.clicked.connect(self.openColorDialogPose)
        self.colorButtonWeapon.clicked.connect(self.openColorDialogWeapon)

        self.weaponConfSlider.valueChanged.connect(self.changeWeaponConf)
        self.poseConfSlider.valueChanged.connect(self.changeWeaponConf)
        self.weaponIOUSlider.valueChanged.connect(self.changeWeaponConf)
        self.weaponThickness.valueChanged.connect(self.changeWeaponThickness)
        self.poseThickness.valueChanged.connect(self.changePoseThickness)

        self.useWebCum.toggled.connect(self.camOnClick)
        self.ChooseButton.clicked.connect(self.chooseOnClick)

        self.playButton.clicked.connect(self.runDetection)

    def chooseOnClick(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', filter="Video Files (*.mp4)")
        self.video_address = fname[0]
        self.currentVideo.setText(fname[0])
        self.capture = cv2.VideoCapture(self.video_address)

    def camOnClick(self):
        if self.useWebCum.isChecked():
            self.currentVideo.setText("Using webcam...")
        else:
            self.currentVideo.setText("Choose your video")

    @pyqtSlot()
    def openColorDialogPose(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.detector.bgrPose = (color.blue(),
                                     color.green(),
                                     color.red())

    @pyqtSlot()
    def openColorDialogWeapon(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.detector.bgrWeapon = (color.blue(),
                                       color.green(),
                                       color.red())

    def changeWeaponConf(self):
        self.detector.weapon_conf = self.weaponConfSlider.value() / 100
        self.detector.weapon_iou = self.weaponIOUSlider.value() / 100
        self.detector.pose_conf = self.poseConfSlider.value() / 100

    def changeWeaponThickness(self):
        self.detector.weapon_thickness = self.weaponThickness.value() / 20

    def changePoseThickness(self):
        self.detector.pose_thickness = self.poseThickness.value() / 20

    def runDetection(self):
        if self.pause:
            self.timer.stop()
            self.playButton.setText("Play")
        else:
            if self.useWebCum.isChecked() == False and self.video_address == '':
                self.currentVideo.setText("Please!!! Choose your video")
                return

            if self.useWebCum.isChecked():
                self.capture = cv2.VideoCapture(0)
            else:
                if not self.capture: self.capture = cv2.VideoCapture(self.video_address)

            self.playButton.setText("Pause")
            self.timer.start(50)
        self.pause = not self.pause

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, 1)

    def displayImage(self, image, window=1):
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

        if window == 1:
            self.imgLabel.setPixmap(QPixmap(outImage))
            self.imgLabel.setScaledContents(True)
