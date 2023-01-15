    
from multiprocessing.connection import wait
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
import itertools
from Initial import generate_initial, IIP
import pyqtgraph as pg
from SimulationSettingScreen import Ui_SimulationSettingScreen
import math
import copy
#Global vars
daysCount = 0
days = []
maxIterations = 0
minImprove  = 0
minDeviation = 0
neighborhoodSize = 0
IIPTimeLimit = 0
A=[[0,0,0,2]]
dM=[[]]
Lambda=[[]]
LambdaI=[ [0] for i in range(1000)]
akt=[[0]*10 for i in range(10)]
d=[]
x=[]
y=[]
order=[]
currentDay=0

def operate_lists(inputY, inputX):
    for y in inputY:
        if math.isclose(y[2], 1.0):
            order[y[1]-1].remove(y[0])
    for x in inputX:
        if math.isclose(x[3], 1.0):
            index = order[x[2]-1].index(x[1])
            order[x[2]-1].insert(index,x[0])


def decode_input_Y_objects(input_str_list):
    values_list = []
    for input_str in input_str_list:
        parts = str(input_str).split('_')
        try:
            values = [int(parts[1]), int(parts[2])]
        except ValueError:
            continue
        values.append(input_str.varValue)
        values_list.append(values)
    return values_list

def decode_input_X_objects(input_str_list):
    values_list = []
    for input_str in input_str_list:
        parts = str(input_str).split('_')
        try:
            values = [int(parts[1]), int(parts[2]), int(parts[3])]
        except ValueError:
            continue
        values.append(input_str.varValue)
        values_list.append(values)
    return values_list
    
def neighborhood_moves(i, j, routes):
    moves = []
    
    moves.append(('one_point', i, j))
    
    for k in routes:
        if k != i and k != j:
            moves.append(('two_point', i, j, k))
    
    for k in routes:
        if k != i and k != j:
            moves.append(('two_opt', i, j, k))
    
    for k, l in itertools.product(routes, repeat=2):
        if k != i and k != j and l != i and l != j:
            moves.append(('three_point', i, j, k, l))
    
    for k in routes:
        if k != i and k != j:
            moves.append(('or_opt', i, j, k))
    return moves

def extract_nested(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(extract_nested(item))
        else:
            result.append(item)
    return result

def get_pairs(input_list):
  
  pairs = []

  
  for i in range(len(input_list) - 1):
    pairs.append((input_list[i], input_list[i + 1]))

  
  return pairs

def perturb_solution(routes):
    routes_copy = routes.copy()
    customers = sorted(routes_copy, key=lambda x: x.demand/x.insertion_cost)
    
    customers_to_remove = customers[:int(len(customers)*0.2)]
    for customer in customers_to_remove:
        routes_copy.remove(customer)
    
    for customer in customers_to_remove:
        best_cost = float('inf')
        best_route = None
        for route in routes_copy:
            for i in range(len(route)):
                cost = 0
                if cost < best_cost:
                    best_cost = cost
                    best_route = route
                    best_index = i
        best_route.insert(best_index, customer)
    return routes_copy

def ERTR(routes, K=70, tolerance=0.1):
    
    best_solution = routes

    while True:
        
        for _ in range(K):
            
            for i, j in itertools.product(routes, repeat=2):
                
                for move in neighborhood_moves(i, j):
                    
                    savings = move
                    
                    if savings > 0 and savings <= tolerance :
                        routes = (routes, move)

        
        improved = True
        while improved:
            improved = False
            
            for i, j in itertools.product(routes, repeat=2):
                
                for move in neighborhood_moves(i, j):
                    
                    savings = move
                    
                    if savings > 0:
                        routes = (routes, move) / 2
                        improved = True

        
        if routes.count > best_solution:
            best_solution = routes
        else:
            
            routes = perturb_solution(routes)

    return best_solution

def generate_list_of_ints(input_string: str) -> list[int]:
    return [int(x) for x in input_string.split(',')]

def subsets(arr):
  arr.sort()
  result = [[]]
  for element in arr:
    result += [subset + [element] for subset in result]
  return result

def distance(point1, point2):
  x1, y1 = point1
  x2, y2 = point2
  return math.sqrt((int(x2) - int(x1))**2 + (int(y2) - int(y1))**2)

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
            
            
            
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        
        return len(self._data)

    def columnCount(self, index):
        
        
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
        self.ui.nextDay.clicked.connect(self.on_nextDay_clicked)

    def on_nextDay_clicked(self):
        global currentDay
        if currentDay < int(daysCount)-1:
            currentDay = currentDay + 1
        else:
            currentDay = 0
        self.ui.PlotWidget.clear()
        scatter = pg.ScatterPlotItem(
            size=10, brush=pg.mkBrush(30, 255, 35, 255))
        scatter.setData(x, y)
        #add magazine
        scatter.addPoints([0],[0], brush=pg.mkBrush('r'))
        self.ui.PlotWidget.addItem(scatter)
        #drawing line
        plt = pg.PlotWidget()
        pairs = get_pairs(order[currentDay])
        for i in pairs:
            if i[0]==0 or i[0]==len(A)+1:
                line=plt.plot([0,x[i[1]-1]],[0,y[i[1]-1]])
            elif i[1]==0 or i[1]==len(A)+1:
                if x[i[0]-1] < 0:
                    line=plt.plot([x[i[0]-1],0],[0,y[i[0]-1]])
                else:
                    line=plt.plot([x[i[0]-1],0],[y[i[0]-1],0])
            else:
                line=plt.plot((x[i[0]-1],x[i[1]-1]),(y[i[0]-1],y[i[1]-1]))
            self.ui.PlotWidget.addItem(line)

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
        global A, dM, LambdaI, akt, daysCount, days, x, y, order, currentDay

        #displaying shops
        for row in A:
            x.append(row[1])
            y.append(row[2])
            d.append(row[0])
        scatter = pg.ScatterPlotItem(
            size=10, brush=pg.mkBrush(30, 255, 35, 255))
        scatter.setData(x, y)
        #add magazine
        scatter.addPoints([0],[0], brush=pg.mkBrush('r'))
        self.ui.PlotWidget.addItem(scatter)
        #drawing line
        plt = pg.PlotWidget()
        LI=0;
        for row in A:
            if type(row[3]) == int:
                LambdaI[LI]=[row[3]]
            elif type(row[3]) == str:
                LambdaI[LI]=generate_list_of_ints(row[3])
            LI=LI+1
        dM = distance_matrix(A[:,[1,2]])
        S=generate_initial(Lambda, LambdaI, len(A), akt, days, d)
        stringS=[]
        for v in range(len(S)):
            for vv in range(len(S[v])):
                stringS.append(str(S[v][vv]) + "_" + str(int(S[v][vv].varValue)))

        print(stringS)
        single_element_list = [sublist in stringS for sublist in stringS]

        stringS = single_element_list

        ik=[0]*4

        for vvv in range(len(stringS)):
            xxx=stringS[vvv].split("_")
            if(int(xxx[3]) ==1):
                ik[int(xxx[1])]=int(xxx[2])
        ik[3]=2

        order=([0],[0])
        for i in range(len(A)):
            for t in days:
                if t in Lambda[ik[i]]:
                    order[t-1].append(i+1)
        for t in days:
            order[t-1].append(len(A)+1)
        pairs = get_pairs(order[0])
        for i in pairs:
            if i[0]==0 or i[0]==len(A)+1:
                line=plt.plot([0,x[i[1]-1]],[0,y[i[1]-1]])
            elif i[1]==0 or i[1]==len(A)+1:
                if x[i[0]-1] < 0:
                    line=plt.plot([x[i[0]-1],0],[y[i[0]-1]],0)
                else:
                    line=plt.plot([x[i[0]-1],0],[0,y[i[0]-1]])
            else:
                line=plt.plot((x[i[0]-1],x[i[1]-1]),(y[i[0]-1],y[i[1]-1]))
            self.ui.PlotWidget.addItem(line)
            orderA=copy.deepcopy(order)
            SS = IIP(Lambda, LambdaI, len(A), akt, days, d, ik, orderA, dM)

            decodedSSY = decode_input_Y_objects(extract_nested(SS[0]))
            decodedSSX = decode_input_X_objects(extract_nested(SS[1]))
            operate_lists(decodedSSY, decodedSSX)
            self.ui.PlotWidget.clear()
            scatter = pg.ScatterPlotItem(
                size=10, brush=pg.mkBrush(30, 255, 35, 255))
            scatter.setData(x, y)
            #add magazine
            scatter.addPoints([0],[0], brush=pg.mkBrush('r'))
            self.ui.PlotWidget.addItem(scatter)
            #drawing line
            plt = pg.PlotWidget()
            pairs = get_pairs(order[currentDay])
            for i in pairs:
                if i[0]==0 or i[0]==len(A)+1:
                    line=plt.plot([0,x[i[1]-1]],[0,y[i[1]-1]])
                elif i[1]==0 or i[1]==len(A)+1:
                    if x[i[0]-1] < 0:
                        line=plt.plot([x[i[0]-1],0],[0,y[i[0]-1]])
                    else:
                        line=plt.plot([x[i[0]-1],0],[y[i[0]-1],0])
                else:
                    line=plt.plot((x[i[0]-1],x[i[1]-1]),(y[i[0]-1],y[i[1]-1]))
                self.ui.PlotWidget.addItem(line)

    def on_Save_clicked(self):
        global daysCount, days, Lambda, akt
        daysCount = self.ui.lineEdit.text()
        self.ui.label_5.setText("Ilość dni: " + daysCount)
        days = [i+1 for i in range(int(daysCount))]
        Lambda = [subset for subset in subsets(days) if subset]
        for i in range(len(days)):
            for j in range(len(Lambda)):
                if days[i] in Lambda[j]:
                    akt[j][i]=1


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


