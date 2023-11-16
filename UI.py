# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 150, 1280, 720))
        self.label.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"border-style:solid;\n"
"border-width:5px;\n"
"border-color: rgb(255, 255, 255);\n"
"")
        self.label.setText("")
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 160, 900))
        self.widget.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.widget.setObjectName("widget")
        self.pushButton_fg = QtWidgets.QPushButton(self.widget)
        self.pushButton_fg.setGeometry(QtCore.QRect(30, 350, 100, 50))
        self.pushButton_fg.setStyleSheet("background-color: rgb(64, 158, 255);\n"
"border-radius: 20px;\n"
"font-size: 16px;\n"
"linr-height: 20px;\n"
"color: rgb(255, 255, 255);")
        self.pushButton_fg.setObjectName("pushButton_fg")
        self.pushButton_bg = QtWidgets.QPushButton(self.widget)
        self.pushButton_bg.setGeometry(QtCore.QRect(30, 500, 100, 50))
        self.pushButton_bg.setStyleSheet("background-color: rgb(64, 158, 255);\n"
"border-radius: 20px;\n"
"font-size: 16px;\n"
"linr-height: 20px;\n"
"color: rgb(255, 255, 255);")
        self.pushButton_bg.setObjectName("pushButton_bg")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(30, 200, 100, 50))
        self.pushButton.setStyleSheet("background-color: rgb(64, 158, 255);\n"
"border-radius: 20px;\n"
"font-size: 16px;\n"
"linr-height: 20px;\n"
"color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.label_fps = QtWidgets.QLabel(self.widget)
        self.label_fps.setGeometry(QtCore.QRect(20, 30, 100, 50))
        self.label_fps.setStyleSheet("\n"
"border-radius: 20px;\n"
"font-size: 30px;\n"
"font:bold;\n"
"linr-height: 20px;\n"
"color: rgb(255, 255, 255);")
        self.label_fps.setAlignment(QtCore.Qt.AlignCenter)
        self.label_fps.setObjectName("label_fps")
        self.pushButton_export = QtWidgets.QPushButton(self.widget)
        self.pushButton_export.setGeometry(QtCore.QRect(30, 650, 100, 50))
        self.pushButton_export.setStyleSheet("background-color: rgb(64, 158, 255);\n"
"border-radius: 20px;\n"
"font-size: 16px;\n"
"linr-height: 20px;\n"
"color: rgb(255, 255, 255);")
        self.pushButton_export.setObjectName("pushButton_export")
        self.pushButton_stop = QtWidgets.QPushButton(self.widget)
        self.pushButton_stop.setGeometry(QtCore.QRect(30, 800, 100, 50))
        self.pushButton_stop.setStyleSheet("\n"
"border-radius: 20px;\n"
"font-size: 30px;\n"
"font:bold;\n"
"linr-height: 20px;\n"
"color: rgb(255, 255, 255);")
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.widget_2.setStyleSheet("background-image: url(:/UI/main.png);")
        self.widget_2.setObjectName("widget_2")
        self.widget_slider = QtWidgets.QWidget(self.centralwidget)
        self.widget_slider.setGeometry(QtCore.QRect(250, 840, 1260, 20))
        self.widget_slider.setStyleSheet("")
        self.widget_slider.setObjectName("widget_slider")
        self.horizontalSlider = QtWidgets.QSlider(self.widget_slider)
        self.horizontalSlider.setGeometry(QtCore.QRect(0, 0, 1260, 20))
        self.horizontalSlider.setStyleSheet("  QSlider::groove:horizontal {         \n"
"  background: red;       \n"
"position: absolute; \n"
"left: 4px; \n"
"right: 4px;     }   \n"
"QSlider::handle:horizontal {           \n"
"background: rgb(255, 170, 0);         \n"
"margin: 0 -20px; }     \n"
"QSlider::add-page:horizontal {         background: rgb(232, 235, 241);     }     \n"
"QSlider::sub-page:horizontal {         background: rgb(35, 173, 229);     }")
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.widget_2.raise_()
        self.label.raise_()
        self.widget.raise_()
        self.widget_slider.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_fg.setText(_translate("MainWindow", "选择前景视频"))
        self.pushButton_bg.setText(_translate("MainWindow", "选择背景视频"))
        self.pushButton.setText(_translate("MainWindow", "开始"))
        self.label_fps.setText(_translate("MainWindow", "fps"))
        self.pushButton_export.setText(_translate("MainWindow", "导出"))
        self.pushButton_stop.setText(_translate("MainWindow", "关闭"))
import UI_rc
