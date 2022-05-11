import time

from slitherlink import solve
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from ReadFile import maps5, maps7, maps10, maps15, maps20, maps30

distance = 30


class MyApp(QtWidgets.QMainWindow):
    __maps = [maps5, maps7, maps10, maps15, maps20, maps30]
    __size = 0
    __map = 0
    __slitherlink_size = 0
    __result = dict()

    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('map/ui.ui', self)
        self.flag = False
        self.setWindowTitle("Slitherlink")
        
        self.input_size.currentIndexChanged.connect(self.create_combobox)
        self.input_map.currentIndexChanged.connect(self.create_map)
        self.solveButton.clicked.connect(self.solver)
        self.create_map(0)
        self.create_combobox(0)
        self.show()

    def create_combobox(self, index):
        self.flag = False
        self.__size = index
        self.input_map.clear()
        length = len(self.__maps[self.__size])
        for i in range(length):
            self.input_map.addItem(str(i + 1))


    def draw_point(self, m, n):
        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.black)
        pen.setWidth(3)
        qp.setPen(pen)
        for i in range(m + 1):
            for j in range(n + 1):
                qp.drawPoint(20 + i * distance, 20 + j * distance)
        qp.end()

    def create_map(self, index):
        self.flag = False
        self.__map = index
        size = len(self.__maps[self.__size][self.__map])
        self.__slitherlink_size = size
        self.map.setRowCount(size)
        self.map.setColumnCount(size)
        self.map.resize(size*distance, size*distance)
        self.map.setGeometry(0, 0, distance * (size + 1), distance * (size + 1))
        self.map.resizeColumnsToContents()
        self.map.verticalHeader().setVisible(False)
        self.map.horizontalHeader().setVisible(False)
        for i in range(size):
            for j in range(size):
                item = self.__maps[self.__size][self.__map][i][j]
                if item != -1:
                    item = str(item)
                else:
                    item = ""
                item = QtWidgets.QTableWidgetItem(item)
                self.map.setItem(i, j, item)
                self.map.item(i, j).setTextAlignment(Qt.AlignCenter)
                
        self.map.setStyleSheet("QTableWidget {background-color: transparent; padding: 10px}")
        self.update()

    def solver(self):
        self.flag = True
        self.update()
        self.__result = solve(self.__maps[self.__size][self.__map])
        self.clause.setText("Clause: " + str(self.__result['clauses']))
        self.variable.setText('Variable: ' + str(self.__result['variables']))
        self.time.setText("Time: %.5f s" % (self.__result['time']))
        self.reload.setText(f"Reload: {self.__result['reload']}")

    def paintEvent(self, event):
        self.draw_point(self.__slitherlink_size, self.__slitherlink_size)
        if self.flag:
            sol = self.__result['result']
            if type(sol) is str:
                self.result.setText(f"Result: {sol}")
                return
            qp = QPainter()
            qp.begin(self)
            pen = QPen(Qt.black)
            pen.setWidth(1)
            qp.setPen(pen)
            m = n = self.__slitherlink_size
            for i in range(m + 1):
                for j in range(n + 1):
                    if j < n:
                        line = i * n + j + 1
                        if sol[line - 1] > 0:
                            x = 20 + j * distance
                            y = 20 + i * distance
                            qp.drawLine(x, y, x + distance, y)
                    if i < m:
                        line1 = (m + 1) * n + j * m + i + 1
                        if sol[line1 - 1] > 0:
                            x = 20 + j * distance
                            y = 20 + i * distance
                            qp.drawLine(x, y, x, y + distance)
            qp.end()


app = QApplication(sys.argv)
UIWindow = MyApp()
sys.exit(app.exec_())
