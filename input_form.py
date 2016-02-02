# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input_form.ui'
#
# Created: Mon Feb  1 06:25:06 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 250)
        Form.setMinimumSize(QtCore.QSize(600, 250))
        Form.setMaximumSize(QtCore.QSize(800, 250))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.info_label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.info_label.setFont(font)
        self.info_label.setWordWrap(True)
        self.info_label.setObjectName("info_label")
        self.verticalLayout.addWidget(self.info_label)
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.type = QtWidgets.QLabel(Form)
        self.type.setMinimumSize(QtCore.QSize(120, 0))
        self.type.setMaximumSize(QtCore.QSize(120, 16777215))
        self.type.setObjectName("type")
        self.horizontalLayout_4.addWidget(self.type)
        self.type_value = QtWidgets.QLineEdit(Form)
        self.type_value.setEnabled(False)
        self.type_value.setObjectName("type_value")
        self.horizontalLayout_4.addWidget(self.type_value)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.old_name = QtWidgets.QLabel(Form)
        self.old_name.setMinimumSize(QtCore.QSize(120, 0))
        self.old_name.setObjectName("old_name")
        self.horizontalLayout_3.addWidget(self.old_name)
        self.old_value = QtWidgets.QLineEdit(Form)
        self.old_value.setEnabled(False)
        self.old_value.setText("")
        self.old_value.setObjectName("old_value")
        self.horizontalLayout_3.addWidget(self.old_value)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.new_name = QtWidgets.QLabel(Form)
        self.new_name.setMinimumSize(QtCore.QSize(120, 0))
        self.new_name.setObjectName("new_name")
        self.horizontalLayout_2.addWidget(self.new_name)
        self.new_value = QtWidgets.QLineEdit(Form)
        self.new_value.setObjectName("new_value")
        self.horizontalLayout_2.addWidget(self.new_value)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 24, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.accept_button = QtWidgets.QPushButton(Form)
        self.accept_button.setMinimumSize(QtCore.QSize(180, 0))
        self.accept_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.accept_button.setObjectName("accept_button")
        self.horizontalLayout.addWidget(self.accept_button)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Изменение параметра"))
        self.info_label.setText(_translate("Form", "Изменение значения и имени параметра возможно только в пределах выделенной для его хранения (в файле улье) памяти."))
        self.type.setText(_translate("Form", "Тип параметра"))
        self.old_name.setText(_translate("Form", "Старое значение"))
        self.new_name.setText(_translate("Form", "Новое значение"))
        self.accept_button.setText(_translate("Form", "Применить"))

