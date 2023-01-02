# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Klient.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ClientScreen(object):
    def setupUi(self, ClientScreen):
        if not ClientScreen.objectName():
            ClientScreen.setObjectName(u"ClientScreen")
        ClientScreen.resize(478, 338)
        self.buttonBox = QDialogButtonBox(ClientScreen)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(120, 290, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.tableView = QTableView(ClientScreen)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(10, 80, 451, 191))
        self.lineEdit = QLineEdit(ClientScreen)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 30, 91, 20))
        self.lineEdit_2 = QLineEdit(ClientScreen)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(140, 30, 41, 20))
        self.lineEdit_3 = QLineEdit(ClientScreen)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(210, 30, 41, 20))
        self.label = QLabel(ClientScreen)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(160, 10, 61, 16))
        self.label_2 = QLabel(ClientScreen)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 30, 16, 16))
        self.label_3 = QLabel(ClientScreen)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(190, 30, 16, 16))
        self.label_4 = QLabel(ClientScreen)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 10, 91, 16))
        self.label_5 = QLabel(ClientScreen)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(270, 10, 91, 16))
        self.lineEdit_4 = QLineEdit(ClientScreen)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(270, 30, 91, 20))
        self.pushButton = QPushButton(ClientScreen)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(380, 20, 75, 31))
        self.pushButton_2 = QPushButton(ClientScreen)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(20, 290, 75, 31))

        self.retranslateUi(ClientScreen)

        QMetaObject.connectSlotsByName(ClientScreen)
    # setupUi

    def retranslateUi(self, ClientScreen):
        ClientScreen.setWindowTitle(QCoreApplication.translate("ClientScreen", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("ClientScreen", u"Cooridnates", None))
        self.label_2.setText(QCoreApplication.translate("ClientScreen", u"X:", None))
        self.label_3.setText(QCoreApplication.translate("ClientScreen", u"Y:", None))
        self.label_4.setText(QCoreApplication.translate("ClientScreen", u"Demand", None))
        self.label_5.setText(QCoreApplication.translate("ClientScreen", u"Pattern", None))
        self.pushButton.setText(QCoreApplication.translate("ClientScreen", u"Add", None))
        self.pushButton_2.setText(QCoreApplication.translate("ClientScreen", u"Delete", None))
    # retranslateUi

