# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QAbstractItemView, QFileDialog
from PySide2.QtCore import QFile, QAbstractTableModel, Qt
from PySide2.QtUiTools import QUiLoader
from form import Ui_Widget
from Klient import Ui_ClientScreen
from Initial import generate_initial
import pyqtgraph as pg
from SimulationSettingScreen import Ui_SimulationSettingScreen
import math

#Global vars
daysCount = 0
days = []
maxIterations = 0
minImprove  = 0
minDeviation = 0
neighborhoodSize = 0
IIPTimeLimit = 0
A=[[0,0,0,0]]
dM=[[]]
Lambda=[[]]
LambdaI=[ [0] for i in range(100)]

def generate_list_of_ints(input_string: str) -> list[int]:
    return [int(x) for x in input_string.split(',')]

def subsets(arr):
  if len(arr) == 0:
    return [[]]
  subs = subsets(arr[1:])
  return subs + [sub + [arr[0]] for sub in subs]

def distance(point1, point2):
  x1, y1 = point1
  x2, y2 = point2
  return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def distance_matrix(points):
  num_points = len(points)
  distance_matrix = np.zeros((num_points, num_points))

  for i in range(num_points):
    for j in range(num_points):
      distance_matrix[i][j] = distance(points[i], points[j])

  return distance_matrix

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = Ui_SimulationSettingScreen()
        self.layout.setupUi(self)
        self.layout.buttonBox.accepted.connect(self.OK)

    def OK(self):
        global maxIterations
        global minImprove
        global minDeviation
        global neighborhoodSize
        global IIPTimeLimit
        maxIterations = self.layout.lineEdit.text()
        minImprove = self.layout.lineEdit_2.text()
        minDeviation = self.layout.lineEdit_3.text()
        neighborhoodSize = self.layout.lineEdit_4.text()
        IIPTimeLimit = self.layout.lineEdit_5.text()
        self.close()

class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global A
        self.layout = Ui_ClientScreen()
        self.layout.setupUi(self)
        self.layout.pushButton.clicked.connect(self.on_Add_clicked)
        self.layout.pushButton_2.clicked.connect(self.on_Delete_clicked)
        self.model = TableModel(A)
        self.layout.tableView.setModel(self.model)
        self.layout.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.layout.buttonBox.accepted.connect(self.OK)
        self.layout.buttonBox.rejected.connect(self.OK)

    def OK(self):
        self.close()

    def on_Delete_clicked(self):
        global A
        indexes = self.layout.tableView.selectionModel().selectedRows()
        for index in sorted(indexes):
            A = np.delete(A, index.row(), 0)
        self.model = TableModel(A)
        self.layout.tableView.setModel(self.model)
        QApplication.processEvents()

    def on_Add_clicked(self):
        global A
        newrow=[self.layout.lineEdit.text(), self.layout.lineEdit_2.text(), self.layout.lineEdit_3.text(), self.layout.lineEdit_4.text()]
        A = np.vstack([A, newrow])
        self.model = TableModel(A)
        self.layout.tableView.setModel(self.model)
        QApplication.processEvents()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.ui.label.setText("Clients: "+str(len(A)))
        self.ui.AddClientButton.clicked.connect(self.on_AddClientButton_clicked)
        self.ui.SettingsButton.clicked.connect(self.on_SettingsButton_clicked)
        self.ui.SaveButton.clicked.connect(self.on_Save_clicked)
        self.ui.StartButton.clicked.connect(self.on_Start_clicked)
        self.ui.ImportButton.clicked.connect(self.on_Import_clicked)
        self.ui.ExportButton.clicked.connect(self.on_Export_clicked)

    def on_Export_clicked(self):
        global A
        name = QFileDialog.getSaveFileName(self, 'Save File')
        pd.DataFrame(A).to_csv(name[0], sep=';', index=False,)

    def on_Import_clicked(self):
        global A
        fileName = QFileDialog.getOpenFileName(self, 'OpenFile')
        data = pd.read_csv(fileName[0],";")
        arr=data.values
        for row in arr:
            A = np.vstack([A, row])
        self.ui.label.setText("Clients: "+str(len(A)))

    def on_Start_clicked(self):
        global A, dM, LambdaI
        x=[]
        y=[]
        #displaying shops
        for row in A:
            x.append(row[1])
            y.append(row[2])
        scatter = pg.ScatterPlotItem(
            size=10, brush=pg.mkBrush(30, 255, 35, 255))
        scatter.setData(x, y)
        #add magazine
        scatter.addPoints([0],[0], brush=pg.mkBrush('r'))
        self.ui.PlotWidget.addItem(scatter)
        #drawing line
        plt = pg.PlotWidget()
        line=plt.plot([0,1],[0,1])
        self.ui.PlotWidget.addItem(line)
        LI=1;
        for row in A:
            if type(row[3]) == int:
                LambdaI[LI]=row[3]
            elif type(row[3]) == str:
                LambdaI[LI]=generate_list_of_ints(row[3])
            LI=LI+1
        dM = distance_matrix(A[:,[1,2]])
        S=generate_initial(Lambda, LambdaI, len(A))


    def on_Save_clicked(self):
        global daysCount, days, Lambda
        daysCount = self.ui.lineEdit.text()
        days = [i+1 for i in range(int(daysCount))]
        Lambda = [subset for subset in subsets(days) if subset]


    def on_SettingsButton_clicked(self):
        self.window = SettingsWindow()
        self.window.show()

    def on_AddClientButton_clicked(self):
        self.window = ClientWindow()
        self.window.show()


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())

