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

from PyQt6 import QtWidgets
from ultralytics import YOLO
from PyQt6.QtCore import pyqtSlot, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QDialog, QColorDialog, QFileDialog
from PyQt6.uic import loadUi
from ObjectDetection.Detector import Detector
from MyThread import MyThread

class Ui_OutputDialog(QDialog):

    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("outputwindow.ui", self)
        self.image = None

        self.video_address = ''
        self.pause = False

        self.my_thread=MyThread()
        self.my_thread.start()
        self.my_thread.mysignal.connect(self.displayImage)

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

        # self.slider.valueChanged.connect(self.on_slider_changed)

    def runDetection(self):
        if self.pause:
            self.my_thread.play_pause=False
            self.playButton.setText("Play")
        else:
            if self.useWebCum.isChecked() == False and self.video_address == '':
                self.currentVideo.setText("Please!!! Choose your video")
                return

            if self.useWebCum.isChecked():
                self.my_thread.capture = cv2.VideoCapture(0)
            else:
                if not self.my_thread.capture: self.my_thread.capture = cv2.VideoCapture(self.video_address)

            self.playButton.setText("Pause")
            self.my_thread.play_pause=True
        self.pause = not self.pause


    def displayImage(self, outImage):
        self.imgLabel.setPixmap(QPixmap(outImage))
        self.imgLabel.setScaledContents(True)

    def chooseOnClick(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', filter="Video Files (*.mp4)")
        self.video_address = fname[0]
        self.currentVideo.setText(fname[0])
        self.my_thread.capture = cv2.VideoCapture(self.video_address)
        self.frame_count = int(self.my_thread.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.slider.setRange(0,self.frame_count)

# ПОПРАВИТЬ
    def on_slider_changed(self, value):
        # перемотка видео к нужному кадру
        if self.my_thread.capture:
            self.my_thread.capture.set(cv2.CAP_PROP_POS_FRAMES, value)

    def camOnClick(self):
        if self.useWebCum.isChecked():
            self.currentVideo.setText("Using webcam...")
        else:
            self.currentVideo.setText("Choose your video")

    @pyqtSlot()
    def openColorDialogPose(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.my_thread.detector.bgrPose = (color.blue(),
                                     color.green(),
                                     color.red())

    @pyqtSlot()
    def openColorDialogWeapon(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.my_thread.detector.bgrWeapon = (color.blue(),
                                       color.green(),
                                       color.red())

    def changeWeaponConf(self):
        self.my_thread.detector.weapon_conf = self.weaponConfSlider.value() / 100
        self.my_thread.detector.weapon_iou = self.weaponIOUSlider.value() / 100
        self.my_thread.detector.pose_conf = self.poseConfSlider.value() / 100

    def changeWeaponThickness(self):
        self.my_thread.detector.weapon_thickness = self.weaponThickness.value() / 20

    def changePoseThickness(self):
        self.my_thread.detector.pose_thickness = self.poseThickness.value() / 20


    def closeEvent(self, e):
        result = QtWidgets.QMessageBox.question(self, "Подтверждение закрытия окна",
                                                "Вы действительно хотите закрыть окно?",
                                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                                                QtWidgets.QMessageBox.StandardButton.No)
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.hide()  # Скрываем окно
            self.my_thread.running = False  # Изменяем флаг выполнения
            self.my_thread.wait(5000)  # Даем время, чтобы закончить
            e.accept()
            QtWidgets.QWidget.closeEvent(self, e)
        else:
            e.ignore()