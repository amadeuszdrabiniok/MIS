# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SimulationSettingScreen.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SimulationSettingScreen(object):
    def setupUi(self, SimulationSettingScreen):
        if not SimulationSettingScreen.objectName():
            SimulationSettingScreen.setObjectName(u"SimulationSettingScreen")
        SimulationSettingScreen.resize(319, 270)
        self.buttonBox = QDialogButtonBox(SimulationSettingScreen)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(130, 225, 171, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.label_4 = QLabel(SimulationSettingScreen)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 10, 91, 16))
        self.lineEdit = QLineEdit(SimulationSettingScreen)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(20, 30, 101, 20))
        self.label_5 = QLabel(SimulationSettingScreen)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 60, 91, 16))
        self.lineEdit_2 = QLineEdit(SimulationSettingScreen)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(20, 80, 101, 20))
        self.label_6 = QLabel(SimulationSettingScreen)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 110, 91, 16))
        self.lineEdit_3 = QLineEdit(SimulationSettingScreen)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(20, 130, 101, 20))
        self.label_7 = QLabel(SimulationSettingScreen)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(20, 160, 101, 16))
        self.lineEdit_4 = QLineEdit(SimulationSettingScreen)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(20, 180, 101, 20))
        self.label_8 = QLabel(SimulationSettingScreen)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(20, 210, 91, 16))
        self.lineEdit_5 = QLineEdit(SimulationSettingScreen)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setGeometry(QRect(20, 230, 101, 20))

        self.retranslateUi(SimulationSettingScreen)

        QMetaObject.connectSlotsByName(SimulationSettingScreen)
    # setupUi

    def retranslateUi(self, SimulationSettingScreen):
        SimulationSettingScreen.setWindowTitle(QCoreApplication.translate("SimulationSettingScreen", u"Dialog", None))
        self.label_4.setText(QCoreApplication.translate("SimulationSettingScreen", u"max Iterations", None))
        self.label_5.setText(QCoreApplication.translate("SimulationSettingScreen", u"min Improve", None))
        self.label_6.setText(QCoreApplication.translate("SimulationSettingScreen", u"min Deviation", None))
        self.label_7.setText(QCoreApplication.translate("SimulationSettingScreen", u"neighborhood size", None))
        self.label_8.setText(QCoreApplication.translate("SimulationSettingScreen", u"IIP time limit", None))
    # retranslateUi

