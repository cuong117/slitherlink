
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from ReadFile import maps5, maps7, maps10, maps15, maps20, maps30
from slitherlink import solve
from slitherlink_optimize import solve as solve_op

distance = 30


class MyApp(QtWidgets.QMainWindow):
    __maps = [maps5, maps7, maps10, maps15, maps20, maps30]
    __size = 0
    __map = 0
    __slitherlink_size = 0
    __result = dict()
    __start_draw_x = 30
    __start_draw_y = 30

    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('map/ui.ui', self)
        self.move(130, 0)
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
        self.info_clear()

    def draw_point(self, m, n):
        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.black)
        pen.setWidth(3)
        qp.setPen(pen)
        for i in range(m + 1):
            for j in range(n + 1):
                qp.drawPoint(self.__start_draw_x + i * distance, self.__start_draw_y + j * distance)
        qp.end()

    def draw_border(self, m, n):
        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.black)
        pen.setWidth(1)
        qp.setPen(pen)
        start = QPoint(self.__start_draw_x - 20, self.__start_draw_y - 20)
        up_right = QPoint(self.__start_draw_x + 20 + m * distance, self.__start_draw_y - 20)
        bottom_left = QPoint(self.__start_draw_x - 20, self.__start_draw_y + 20 + n * distance)
        bottom_right = QPoint(self.__start_draw_x + 20 + m * distance, self.__start_draw_y + 20 + n * distance)
        qp.drawLine(start, up_right)
        qp.drawLine(start, bottom_left)
        qp.drawLine(bottom_left, bottom_right)
        qp.drawLine(bottom_right, up_right)
        qp.end()

    def create_map(self, index):
        h = self.height()
        self.flag = False
        self.__map = index
        size = len(self.__maps[self.__size][self.__map])
        self.__slitherlink_size = size
        self.__start_draw_x = int((959 - (distance * size)) / 2)
        self.__start_draw_y = int((h - (distance * size)) / 2)
        self.map.setRowCount(size)
        self.map.setColumnCount(size)
        self.map.setGeometry(self.__start_draw_x, self.__start_draw_y, distance * size, distance * size)
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
                
        self.map.setStyleSheet("QTableWidget {background-color: transparent; border: none}")
        self.update()

    def solver(self):
        self.flag = True
        self.update()
        index = self.input_method.currentIndex()
        if index:
            self.__result = solve_op(self.__maps[self.__size][self.__map])
        else:
            self.__result = solve(self.__maps[self.__size][self.__map])
        self.clause.setText("Clause: " + str(self.__result['clauses']))
        self.variable.setText('Variable: ' + str(self.__result['variables']))
        self.time.setText("Time: %.3f ms" % (self.__result['time']))
        self.reload.setText(f"Reload: {self.__result['reload']}")
        
    def paintEvent(self, event):
        self.draw_point(self.__slitherlink_size, self.__slitherlink_size)
        self.draw_border(self.__slitherlink_size, self.__slitherlink_size)
        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.black)
        pen.setWidth(1)
        qp.setPen(pen)
        if self.flag:
            sol = self.__result['result']
            if type(sol) is str:
                self.result.setText(f"Result: {sol}")
                return
            pen.setWidth(1)
            qp.setPen(pen)
            m = n = self.__slitherlink_size
            for i in range(m + 1):
                for j in range(n + 1):
                    if j < n:
                        line = i * n + j + 1
                        if sol[line - 1] > 0:
                            x = self.__start_draw_x + j * distance
                            y = self.__start_draw_y + i * distance
                            qp.drawLine(x, y, x + distance, y)
                    if i < m:
                        line1 = (m + 1) * n + j * m + i + 1
                        if sol[line1 - 1] > 0:
                            x = self.__start_draw_x + j * distance
                            y = self.__start_draw_y + i * distance
                            qp.drawLine(x, y, x, y + distance)
        qp.end()

    def info_clear(self):
        self.clause.setText("Clause: ")
        self.variable.setText("Variable: ")
        self.time.setText("Time: ")
        self.reload.setText("Reload: ")


app = QApplication(sys.argv)
UIWindow = MyApp()
sys.exit(app.exec_())
