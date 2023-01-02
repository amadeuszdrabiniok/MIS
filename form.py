# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pyqtgraph as pg

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(587, 490)
        self.AddClientButton = QPushButton(Widget)
        self.AddClientButton.setObjectName(u"AddClientButton")
        self.AddClientButton.setGeometry(QRect(20, 20, 80, 22))
        self.SettingsButton = QPushButton(Widget)
        self.SettingsButton.setObjectName(u"SettingsButton")
        self.SettingsButton.setGeometry(QRect(20, 50, 80, 22))
        self.label_5 = QLabel(Widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 80, 80, 22))
        self.lineEdit = QLineEdit(Widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(20, 110, 80, 22))
        self.SaveButton = QPushButton(Widget)
        self.SaveButton.setObjectName(u"SaveButton")
        self.SaveButton.setGeometry(QRect(20, 140, 80, 22))
        self.StartButton = QPushButton(Widget)
        self.StartButton.setObjectName(u"StartButton")
        self.StartButton.setGeometry(QRect(20, 370, 80, 22))
        self.StopButton = QPushButton(Widget)
        self.StopButton.setObjectName(u"StopButton")
        self.StopButton.setGeometry(QRect(20, 400, 80, 22))
        self.ImportButton = QPushButton(Widget)
        self.ImportButton.setObjectName(u"ImportButton")
        self.ImportButton.setGeometry(QRect(130, 450, 201, 22))
        self.ExportButton = QPushButton(Widget)
        self.ExportButton.setObjectName(u"ExportButton")
        self.ExportButton.setGeometry(QRect(360, 450, 201, 22))
        self.PlotWidget = pg.PlotWidget(Widget)
        self.PlotWidget.setObjectName(u"graphicsView")
        self.PlotWidget.setGeometry(QRect(120, 10, 441, 411))
        scatter = pg.ScatterPlotItem(
            size=10, brush=pg.mkBrush(30, 255, 35, 255))
        x_data = [0]
        y_data = [0]
        scatter.setData(x_data, y_data)
        self.PlotWidget.addItem(scatter)
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 180, 47, 14))
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 330, 81, 16))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.AddClientButton.setText(QCoreApplication.translate("Widget", u"Add Client", None))
        self.SettingsButton.setText(QCoreApplication.translate("Widget", u"Settings", None))
        self.StartButton.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.StopButton.setText(QCoreApplication.translate("Widget", u"Stop", None))
        self.ImportButton.setText(QCoreApplication.translate("Widget", u"Import from Excel", None))
        self.ExportButton.setText(QCoreApplication.translate("Widget", u"Export To Excel", None))
        self.SaveButton.setText(QCoreApplication.translate("Widget", u"Save", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Clients: ", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Time: 00:00:00", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"Ilość dni:", None))
    # retranslateUi

