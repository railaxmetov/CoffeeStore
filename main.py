import sqlite3

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

import sys

from addEditCoffeeForm import addEditCoffeeItem


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.coffeePrices = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.coffeePrices.setGeometry(QtCore.QRect(10, 10, 781, 491))
        self.coffeePrices.setObjectName("coffeePrices")
        self.coffeePrices.setColumnCount(0)
        self.coffeePrices.setRowCount(0)
        self.refresh = QtWidgets.QPushButton(parent=self.centralwidget)
        self.refresh.setGeometry(QtCore.QRect(680, 510, 101, 29))
        self.refresh.setObjectName("refresh")
        self.addCoffee = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addCoffee.setGeometry(QtCore.QRect(570, 510, 101, 29))
        self.addCoffee.setObjectName("addCoffee")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.refresh.setText(_translate("MainWindow", "Обновить"))
        self.addCoffee.setText(_translate("MainWindow", "Добавить"))


class CoffeePrices(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.con = sqlite3.connect('release/data/coffee.sqlite')
        self.cur = self.con.cursor()

        self.refresh.clicked.connect(self.refresh_prices)
        self.addCoffee.clicked.connect(self.add_coffee)

    def refresh_prices(self):
        res = self.cur.execute('SELECT * FROM CoffeePrices')
        headers = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый / В Зёрнах', 'Описание вкуса', 'Цена', 'Объем упаковки']
        self.coffeePrices.setColumnCount(len(headers))
        self.coffeePrices.setHorizontalHeaderLabels(headers)
        self.coffeePrices.setRowCount(0)

        for i, row in enumerate(res):
            self.coffeePrices.setRowCount(self.coffeePrices.rowCount() + 1)
            for j, item in enumerate(row):
                self.coffeePrices.setItem(i, j, QTableWidgetItem(str(item)))

        self.coffeePrices.resizeColumnsToContents()

    def add_coffee(self):
        temp_dialog = addEditCoffeeItem(self.cur)
        temp_dialog.exec()
        self.con.commit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeePrices()
    ex.show()
    sys.exit(app.exec())

