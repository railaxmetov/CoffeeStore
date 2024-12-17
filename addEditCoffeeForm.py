import sqlite3

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.Name = QtWidgets.QLineEdit(parent=Dialog)
        self.Name.setGeometry(QtCore.QRect(0, 10, 391, 28))
        self.Name.setInputMask("")
        self.Name.setText("")
        self.Name.setObjectName("Name")
        self.Grade = QtWidgets.QLineEdit(parent=Dialog)
        self.Grade.setGeometry(QtCore.QRect(0, 40, 391, 28))
        self.Grade.setObjectName("Grade")
        self.Status = QtWidgets.QLineEdit(parent=Dialog)
        self.Status.setGeometry(QtCore.QRect(0, 70, 391, 28))
        self.Status.setObjectName("Status")
        self.Disc = QtWidgets.QLineEdit(parent=Dialog)
        self.Disc.setGeometry(QtCore.QRect(0, 100, 391, 28))
        self.Disc.setObjectName("Disc")
        self.Price = QtWidgets.QLineEdit(parent=Dialog)
        self.Price.setGeometry(QtCore.QRect(0, 130, 391, 28))
        self.Price.setObjectName("Price")
        self.Volume = QtWidgets.QLineEdit(parent=Dialog)
        self.Volume.setGeometry(QtCore.QRect(0, 160, 391, 28))
        self.Volume.setObjectName("Volume")
        self.addDBItem = QtWidgets.QPushButton(parent=Dialog)
        self.addDBItem.setGeometry(QtCore.QRect(300, 260, 91, 29))
        self.addDBItem.setObjectName("addDBItem")
        self.changeDBItem = QtWidgets.QPushButton(parent=Dialog)
        self.changeDBItem.setGeometry(QtCore.QRect(200, 260, 91, 29))
        self.changeDBItem.setObjectName("changeDBItem")
        self.deleteDBItem = QtWidgets.QPushButton(parent=Dialog)
        self.deleteDBItem.setGeometry(QtCore.QRect(100, 260, 91, 29))
        self.deleteDBItem.setObjectName("deleteDBItem")
        self.errorLabel = QtWidgets.QLabel(parent=Dialog)
        self.errorLabel.setGeometry(QtCore.QRect(0, 190, 391, 21))
        self.errorLabel.setText("")
        self.errorLabel.setObjectName("errorLabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Name.setPlaceholderText(_translate("Dialog", "Название сорта"))
        self.Grade.setPlaceholderText(_translate("Dialog", "Степень обжарки"))
        self.Status.setPlaceholderText(_translate("Dialog", "Молотый / В Зёрнах"))
        self.Disc.setPlaceholderText(_translate("Dialog", "Описание вкуса"))
        self.Price.setPlaceholderText(_translate("Dialog", "Цена"))
        self.Volume.setPlaceholderText(_translate("Dialog", "Объем упаковки"))
        self.addDBItem.setText(_translate("Dialog", "Добавить"))
        self.changeDBItem.setText(_translate("Dialog", "Изменить"))
        self.deleteDBItem.setText(_translate("Dialog", "Удалить"))



class addEditCoffeeItem(QDialog, Ui_Dialog):
    def __init__(self, db_cur: sqlite3.Cursor):
        super().__init__()
        self.setupUi(self)
        self.initUi(db_cur)

    def initUi(self, db_cur: sqlite3.Cursor):
        self.addDBItem.clicked.connect(self.addDB)
        self.changeDBItem.clicked.connect(self.changeDB)
        self.deleteDBItem.clicked.connect(self.deleteDB)
        self.db_cur = db_cur

    def addDB(self):
        error_massage = []
        if self.Name.text() == '':
            error_massage.append('Нет названия')
        if self.Name.text() in [i[0] for i in self.db_cur.execute('SELECT Name FROM CoffeePrices').fetchall()]:
            error_massage.append('Данная позиция уже есть')
        if self.Price.text().isalpha():
            error_massage.append('Некоректная цена')
        if self.Volume.text().isalpha():
            error_massage.append('Некоректный объем')
        if error_massage:
            self.errorLabel.setText(' + '.join(error_massage))
        else:
            self.db_cur.execute('INSERT INTO CoffeePrices (Name, Grade, Status, Desc, Price, Volume) VALUES (?, ?, ?, ?, ?, ?)',
                                (self.Name.text(), self.Grade.text(), self.Status.text(), self.Disc.text(), self.Price.text(), self.Volume.text()))
            self.close()

    def changeDB(self):
        error_massage = []
        if self.Name.text() not in [i[0] for i in self.db_cur.execute('SELECT Name FROM CoffeePrices').fetchall()]:
            print(self.db_cur.execute('SELECT Name FROM CoffeePrices').fetchall())
            error_massage.append('Нет такого названия в таблице')
        if self.Price.text().isalpha():
            error_massage.append('Некоректная цена')
        if self.Volume.text().isalpha():
            error_massage.append('Некоректный объем')
        if error_massage:
            self.errorLabel.setText(' + '.join(error_massage))
        else:
            self.db_cur.execute('UPDATE CoffeePrices SET Grade=?, Status=?, Desc=?, Price=?, Volume=? WHERE Name=?',
                                (self.Grade.text(), self.Status.text(), self.Disc.text(), self.Price.text(), self.Volume.text(), self.Name.text()))
            self.close()

    def deleteDB(self):
        error_massage = []
        if self.Name.text() not in [i[0] for i in self.db_cur.execute('SELECT Name FROM CoffeePrices').fetchall()]:
            print(self.db_cur.execute('SELECT Name FROM CoffeePrices').fetchall())
            error_massage.append('Нет такого названия в таблице')
        if error_massage:
            self.errorLabel.setText(' + '.join(error_massage))
        else:
            self.db_cur.execute('DELETE FROM CoffeePrices WHERE Name=?',
                                (self.Name.text(),))
            self.close()


