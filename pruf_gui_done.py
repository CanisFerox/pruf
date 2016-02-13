#!/usr/bin/python3
from PyQt5 import QtWidgets

import argparse
from struct import unpack, pack
import sys
import binascii
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem, QTableWidgetItem
from datetime import datetime, timedelta

main_block_size = 0x1000
registry = {}


################ CHANGE VALUE ################

class UI_Input(object):
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
		self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_5.setObjectName("horizontalLayout_5")
		self.error_label = QtWidgets.QLabel(Form)
		self.error_label.setMinimumSize(QtCore.QSize(500, 0))
		self.error_label.setText("")
		self.error_label.setObjectName("error_label")
		self.horizontalLayout_5.addWidget(self.error_label)
		spacerItem1 = QtWidgets.QSpacerItem(20, 24, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.horizontalLayout_5.addItem(spacerItem1)
		self.verticalLayout.addLayout(self.horizontalLayout_5)
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem2)
		self.accept_button = QtWidgets.QPushButton(Form)
		self.accept_button.setMinimumSize(QtCore.QSize(150, 0))
		self.accept_button.setMaximumSize(QtCore.QSize(150, 27))
		self.accept_button.setObjectName("accept_button")
		self.horizontalLayout.addWidget(self.accept_button)
		self.exit_button = QtWidgets.QPushButton(Form)
		self.exit_button.setMinimumSize(QtCore.QSize(150, 27))
		self.exit_button.setMaximumSize(QtCore.QSize(150, 27))
		self.exit_button.setObjectName("exit_button")
		self.horizontalLayout.addWidget(self.exit_button)
		spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem3)
		self.verticalLayout.addLayout(self.horizontalLayout)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "Изменение параметра"))
		self.info_label.setText(_translate("Form",
		                                   "Изменение значения и имени параметра возможно только в пределах выделенной для его хранения (в файле улье) памяти."))
		self.type.setText(_translate("Form", "Тип параметра"))
		self.old_name.setText(_translate("Form", "Старое значение"))
		self.new_name.setText(_translate("Form", "Новое значение"))
		self.accept_button.setText(_translate("Form", "Применить"))
		self.exit_button.setText(_translate("Form", "Отмена"))


########### MAIN WINDOW #############

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(984, 643)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.centralwidget)
		self.horizontalLayout_7.setObjectName("horizontalLayout_7")
		self.splitter = QtWidgets.QSplitter(self.centralwidget)
		self.splitter.setOrientation(QtCore.Qt.Horizontal)
		self.splitter.setObjectName("splitter")
		self.treeWidget = QtWidgets.QTreeWidget(self.splitter)
		self.treeWidget.setEnabled(True)
		self.treeWidget.setProperty("showDropIndicator", True)
		self.treeWidget.setRootIsDecorated(True)
		self.treeWidget.setItemsExpandable(True)
		self.treeWidget.setHeaderHidden(True)
		self.treeWidget.setObjectName("treeWidget")
		self.treeWidget.headerItem().setText(0, "1")
		self.treeWidget.header().setVisible(False)
		self.layoutWidget = QtWidgets.QWidget(self.splitter)
		self.layoutWidget.setObjectName("layoutWidget")
		self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
		self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_6.setObjectName("horizontalLayout_6")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout()
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		spacerItem = QtWidgets.QSpacerItem(48, 16, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem)
		self.nk_count = QtWidgets.QLabel(self.layoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.nk_count.sizePolicy().hasHeightForWidth())
		self.nk_count.setSizePolicy(sizePolicy)
		self.nk_count.setObjectName("nk_count")
		self.horizontalLayout_2.addWidget(self.nk_count)
		self.nk_value = QtWidgets.QLabel(self.layoutWidget)
		self.nk_value.setMinimumSize(QtCore.QSize(100, 0))
		self.nk_value.setText("")
		self.nk_value.setObjectName("nk_value")
		self.horizontalLayout_2.addWidget(self.nk_value)
		spacerItem1 = QtWidgets.QSpacerItem(40, 16, QtWidgets.QSizePolicy.MinimumExpanding,
		                                    QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem1)
		self.verticalLayout_2.addLayout(self.horizontalLayout_2)
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		spacerItem2 = QtWidgets.QSpacerItem(56, 16, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_3.addItem(spacerItem2)
		self.vk_count = QtWidgets.QLabel(self.layoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vk_count.sizePolicy().hasHeightForWidth())
		self.vk_count.setSizePolicy(sizePolicy)
		self.vk_count.setObjectName("vk_count")
		self.horizontalLayout_3.addWidget(self.vk_count)
		self.vk_value = QtWidgets.QLabel(self.layoutWidget)
		self.vk_value.setMinimumSize(QtCore.QSize(100, 0))
		self.vk_value.setText("")
		self.vk_value.setObjectName("vk_value")
		self.horizontalLayout_3.addWidget(self.vk_value)
		spacerItem3 = QtWidgets.QSpacerItem(40, 16, QtWidgets.QSizePolicy.MinimumExpanding,
		                                    QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_3.addItem(spacerItem3)
		self.verticalLayout_2.addLayout(self.horizontalLayout_3)
		self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_4.setObjectName("horizontalLayout_4")
		spacerItem4 = QtWidgets.QSpacerItem(23, 16, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_4.addItem(spacerItem4)
		self.timestamp = QtWidgets.QLabel(self.layoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.timestamp.sizePolicy().hasHeightForWidth())
		self.timestamp.setSizePolicy(sizePolicy)
		self.timestamp.setAutoFillBackground(False)
		self.timestamp.setScaledContents(False)
		self.timestamp.setWordWrap(False)
		self.timestamp.setObjectName("timestamp")
		self.horizontalLayout_4.addWidget(self.timestamp)
		self.timestamp_value = QtWidgets.QLabel(self.layoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.timestamp_value.sizePolicy().hasHeightForWidth())
		self.timestamp_value.setSizePolicy(sizePolicy)
		self.timestamp_value.setMinimumSize(QtCore.QSize(220, 0))
		self.timestamp_value.setText("")
		self.timestamp_value.setObjectName("timestamp_value")
		self.horizontalLayout_4.addWidget(self.timestamp_value)
		self.verticalLayout_2.addLayout(self.horizontalLayout_4)
		self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_5.setObjectName("horizontalLayout_5")
		spacerItem5 = QtWidgets.QSpacerItem(13, 16, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_5.addItem(spacerItem5)
		self.cell_shift = QtWidgets.QLabel(self.layoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.cell_shift.sizePolicy().hasHeightForWidth())
		self.cell_shift.setSizePolicy(sizePolicy)
		self.cell_shift.setObjectName("cell_shift")
		self.horizontalLayout_5.addWidget(self.cell_shift)
		self.cell_shift_value = QtWidgets.QLabel(self.layoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.cell_shift_value.sizePolicy().hasHeightForWidth())
		self.cell_shift_value.setSizePolicy(sizePolicy)
		self.cell_shift_value.setMinimumSize(QtCore.QSize(220, 0))
		self.cell_shift_value.setText("")
		self.cell_shift_value.setObjectName("cell_shift_value")
		self.horizontalLayout_5.addWidget(self.cell_shift_value)
		self.verticalLayout_2.addLayout(self.horizontalLayout_5)
		self.horizontalLayout_6.addLayout(self.verticalLayout_2)
		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setObjectName("verticalLayout")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.mode = QtWidgets.QLabel(self.layoutWidget)
		self.mode.setObjectName("mode")
		self.horizontalLayout.addWidget(self.mode)
		self.mode_value = QtWidgets.QLabel(self.layoutWidget)
		self.mode_value.setMinimumSize(QtCore.QSize(75, 0))
		self.mode_value.setText("")
		self.mode_value.setObjectName("mode_value")
		self.horizontalLayout.addWidget(self.mode_value)
		self.verticalLayout.addLayout(self.horizontalLayout)
		spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem6)
		self.horizontalLayout_6.addLayout(self.verticalLayout)
		self.verticalLayout_3.addLayout(self.horizontalLayout_6)
		self.tableWidget = QtWidgets.QTableWidget(self.layoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
		self.tableWidget.setSizePolicy(sizePolicy)
		self.tableWidget.setAcceptDrops(False)
		self.tableWidget.setAutoFillBackground(False)
		self.tableWidget.setShowGrid(False)
		self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
		self.tableWidget.setWordWrap(False)
		self.tableWidget.setObjectName("tableWidget")
		self.tableWidget.setColumnCount(5)
		self.tableWidget.setRowCount(0)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(4, item)
		self.tableWidget.horizontalHeader().setVisible(True)
		self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
		self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
		self.tableWidget.horizontalHeader().setStretchLastSection(True)
		self.tableWidget.verticalHeader().setVisible(False)
		self.verticalLayout_3.addWidget(self.tableWidget)
		self.verticalLayout_3.setStretch(0, 1)
		self.verticalLayout_3.setStretch(1, 1000)
		self.horizontalLayout_7.addWidget(self.splitter)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 984, 24))
		self.menubar.setDefaultUp(False)
		self.menubar.setNativeMenuBar(False)
		self.menubar.setObjectName("menubar")
		self.file = QtWidgets.QMenu(self.menubar)
		self.file.setObjectName("file")
		self.export_2 = QtWidgets.QMenu(self.file)
		self.export_2.setObjectName("export_2")
		self.search = QtWidgets.QMenu(self.menubar)
		self.search.setObjectName("search")
		self.view = QtWidgets.QMenu(self.menubar)
		self.view.setObjectName("view")
		self.view_mode = QtWidgets.QMenu(self.view)
		self.view_mode.setObjectName("view_mode")
		self.help = QtWidgets.QMenu(self.menubar)
		self.help.setObjectName("help")
		self.menu = QtWidgets.QMenu(self.menubar)
		self.menu.setObjectName("menu")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.action1 = QtWidgets.QAction(MainWindow)
		self.action1.setObjectName("action1")
		self.action2 = QtWidgets.QAction(MainWindow)
		self.action2.setObjectName("action2")
		self.open_action = QtWidgets.QAction(MainWindow)
		self.open_action.setObjectName("open_action")
		self.exit_action = QtWidgets.QAction(MainWindow)
		self.exit_action.setObjectName("exit_action")
		self.view_deleted = QtWidgets.QAction(MainWindow)
		self.view_deleted.setObjectName("view_deleted")
		self.view_nondeleted = QtWidgets.QAction(MainWindow)
		self.view_nondeleted.setObjectName("view_nondeleted")
		self.view_all = QtWidgets.QAction(MainWindow)
		self.view_all.setObjectName("view_all")
		self.about = QtWidgets.QAction(MainWindow)
		self.about.setObjectName("about")
		self.export_a_action = QtWidgets.QAction(MainWindow)
		self.export_a_action.setObjectName("export_a_action")
		self.export_m_action = QtWidgets.QAction(MainWindow)
		self.export_m_action.setObjectName("export_m_action")
		self.search_action = QtWidgets.QAction(MainWindow)
		self.search_action.setObjectName("search_action")
		self.save_action = QtWidgets.QAction(MainWindow)
		self.save_action.setObjectName("save_action")
		self.value_search_action = QtWidgets.QAction(MainWindow)
		self.value_search_action.setObjectName("value_search_action")
		self.change_value = QtWidgets.QAction(MainWindow)
		self.change_value.setObjectName("change_value")
		self.change_name = QtWidgets.QAction(MainWindow)
		self.change_name.setObjectName("change_name")
		self.renew_action = QtWidgets.QAction(MainWindow)
		self.renew_action.setObjectName("renew_action")
		self.export_2.addAction(self.export_a_action)
		self.export_2.addAction(self.export_m_action)
		self.file.addAction(self.open_action)
		self.file.addAction(self.save_action)
		self.file.addAction(self.renew_action)
		self.file.addAction(self.export_2.menuAction())
		self.file.addAction(self.exit_action)
		self.search.addAction(self.value_search_action)
		self.view_mode.addAction(self.view_deleted)
		self.view_mode.addAction(self.view_nondeleted)
		self.view_mode.addAction(self.view_all)
		self.view.addAction(self.view_mode.menuAction())
		self.help.addAction(self.about)
		self.menu.addAction(self.change_value)
		self.menu.addAction(self.change_name)
		self.menubar.addAction(self.file.menuAction())
		self.menubar.addAction(self.menu.menuAction())
		self.menubar.addAction(self.search.menuAction())
		self.menubar.addAction(self.view.menuAction())
		self.menubar.addAction(self.help.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "PRUF GUI"))
		self.nk_count.setText(_translate("MainWindow", "Подразделов:"))
		self.vk_count.setText(_translate("MainWindow", "Параметров:"))
		self.timestamp.setText(_translate("MainWindow", "Временная метка:"))
		self.cell_shift.setText(_translate("MainWindow", "Смещение в файле:"))
		self.mode.setText(_translate("MainWindow", "Режим:"))
		self.tableWidget.setSortingEnabled(False)
		item = self.tableWidget.horizontalHeaderItem(0)
		item.setText(_translate("MainWindow", "Имя"))
		item = self.tableWidget.horizontalHeaderItem(1)
		item.setText(_translate("MainWindow", "Тип"))
		item = self.tableWidget.horizontalHeaderItem(2)
		item.setText(_translate("MainWindow", "Размер"))
		item = self.tableWidget.horizontalHeaderItem(3)
		item.setText(_translate("MainWindow", "Значение"))
		item = self.tableWidget.horizontalHeaderItem(4)
		item.setText(_translate("MainWindow", "Смещение"))
		self.file.setTitle(_translate("MainWindow", "Файл"))
		self.export_2.setTitle(_translate("MainWindow", "Экспорт"))
		self.search.setTitle(_translate("MainWindow", "Поиск"))
		self.view.setTitle(_translate("MainWindow", "Вид"))
		self.view_mode.setTitle(_translate("MainWindow", "Режим отображения"))
		self.help.setTitle(_translate("MainWindow", "Помощь"))
		self.menu.setTitle(_translate("MainWindow", "Правка"))
		self.action1.setText(_translate("MainWindow", "1"))
		self.action2.setText(_translate("MainWindow", "2"))
		self.open_action.setText(_translate("MainWindow", "Открыть"))
		self.exit_action.setText(_translate("MainWindow", "Выход"))
		self.view_deleted.setText(_translate("MainWindow", "Только удаленные"))
		self.view_nondeleted.setText(_translate("MainWindow", "Только неудаленные"))
		self.view_all.setText(_translate("MainWindow", "Все"))
		self.about.setText(_translate("MainWindow", "О программе"))
		self.export_a_action.setText(_translate("MainWindow", "Формат -a (машинный)"))
		self.export_m_action.setText(_translate("MainWindow", "Формат -m (визуальный)"))
		self.search_action.setText(_translate("MainWindow", "Поиск"))
		self.save_action.setText(_translate("MainWindow", "Сохранить"))
		self.value_search_action.setText(_translate("MainWindow", "Поиск..."))
		self.change_value.setText(_translate("MainWindow", "Изменить значение параметра"))
		self.change_name.setText(_translate("MainWindow", "Изменить имя параметра"))
		self.renew_action.setText(_translate("MainWindow", "Обновить"))


####### SEARCH ########

class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.setWindowModality(QtCore.Qt.WindowModal)
		Form.resize(640, 480)
		Form.setMinimumSize(QtCore.QSize(640, 480))
		self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout()
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.search_input = QtWidgets.QLineEdit(Form)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.search_input.sizePolicy().hasHeightForWidth())
		self.search_input.setSizePolicy(sizePolicy)
		self.search_input.setText("")
		self.search_input.setClearButtonEnabled(True)
		self.search_input.setObjectName("search_input")
		self.horizontalLayout.addWidget(self.search_input)
		self.seach_button = QtWidgets.QPushButton(Form)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.seach_button.sizePolicy().hasHeightForWidth())
		self.seach_button.setSizePolicy(sizePolicy)
		self.seach_button.setObjectName("seach_button")
		self.horizontalLayout.addWidget(self.seach_button)
		self.clear_button = QtWidgets.QPushButton(Form)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.clear_button.sizePolicy().hasHeightForWidth())
		self.clear_button.setSizePolicy(sizePolicy)
		self.clear_button.setObjectName("clear_button")
		self.horizontalLayout.addWidget(self.clear_button)
		self.verticalLayout_2.addLayout(self.horizontalLayout)
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.status_label = QtWidgets.QLabel(Form)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
		self.status_label.setSizePolicy(sizePolicy)
		self.status_label.setText("")
		self.status_label.setObjectName("status_label")
		self.horizontalLayout_2.addWidget(self.status_label)
		self.exit_button = QtWidgets.QPushButton(Form)
		self.exit_button.setMinimumSize(QtCore.QSize(85, 27))
		self.exit_button.setMaximumSize(QtCore.QSize(85, 27))
		self.exit_button.setObjectName("exit_button")
		self.horizontalLayout_2.addWidget(self.exit_button)
		self.verticalLayout_2.addLayout(self.horizontalLayout_2)
		self.horizontalLayout_3.addLayout(self.verticalLayout_2)
		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setObjectName("verticalLayout")
		self.checkBox = QtWidgets.QCheckBox(Form)
		self.checkBox.setChecked(True)
		self.checkBox.setObjectName("checkBox")
		self.verticalLayout.addWidget(self.checkBox)
		self.checkBox_2 = QtWidgets.QCheckBox(Form)
		self.checkBox_2.setChecked(True)
		self.checkBox_2.setObjectName("checkBox_2")
		self.verticalLayout.addWidget(self.checkBox_2)
		self.checkBox_3 = QtWidgets.QCheckBox(Form)
		self.checkBox_3.setChecked(True)
		self.checkBox_3.setObjectName("checkBox_3")
		self.verticalLayout.addWidget(self.checkBox_3)
		self.horizontalLayout_3.addLayout(self.verticalLayout)
		self.verticalLayout_3.addLayout(self.horizontalLayout_3)
		self.search_table = QtWidgets.QTableWidget(Form)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(100)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.search_table.sizePolicy().hasHeightForWidth())
		self.search_table.setSizePolicy(sizePolicy)
		self.search_table.setShowGrid(True)
		self.search_table.setWordWrap(False)
		self.search_table.setObjectName("search_table")
		self.search_table.setColumnCount(2)
		self.search_table.setRowCount(0)
		item = QtWidgets.QTableWidgetItem()
		self.search_table.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.search_table.setHorizontalHeaderItem(1, item)
		self.search_table.horizontalHeader().setVisible(True)
		self.search_table.horizontalHeader().setCascadingSectionResizes(False)
		self.search_table.horizontalHeader().setDefaultSectionSize(200)
		self.search_table.horizontalHeader().setHighlightSections(True)
		self.search_table.horizontalHeader().setMinimumSectionSize(100)
		self.search_table.horizontalHeader().setSortIndicatorShown(False)
		self.search_table.horizontalHeader().setStretchLastSection(True)
		self.search_table.verticalHeader().setVisible(False)
		self.verticalLayout_3.addWidget(self.search_table)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "Поиск"))
		self.seach_button.setText(_translate("Form", "Поиск"))
		self.clear_button.setText(_translate("Form", "Очистить"))
		self.exit_button.setText(_translate("Form", "Отмена"))
		self.checkBox.setText(_translate("Form", "В именах разделов"))
		self.checkBox_2.setText(_translate("Form", "В именах параметров"))
		self.checkBox_3.setText(_translate("Form", "В значениях параметров"))
		item = self.search_table.horizontalHeaderItem(0)
		item.setText(_translate("Form", "Где найдено"))
		item = self.search_table.horizontalHeaderItem(1)
		item.setText(_translate("Form", "Полный путь"))


class AboutUI(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(500, 150)
		Form.setMinimumSize(QtCore.QSize(500, 150))
		Form.setMaximumSize(QtCore.QSize(500, 150))
		Form.setWindowFilePath("")
		self.verticalLayout = QtWidgets.QVBoxLayout(Form)
		self.verticalLayout.setObjectName("verticalLayout")
		spacerItem = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem)
		self.label = QtWidgets.QLabel(Form)
		self.label.setObjectName("label")
		self.verticalLayout.addWidget(self.label)
		self.label_2 = QtWidgets.QLabel(Form)
		self.label_2.setObjectName("label_2")
		self.verticalLayout.addWidget(self.label_2)
		self.label_3 = QtWidgets.QLabel(Form)
		self.label_3.setObjectName("label_3")
		self.verticalLayout.addWidget(self.label_3)
		spacerItem1 = QtWidgets.QSpacerItem(20, 14, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem1)
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem2)
		self.exit_button = QtWidgets.QPushButton(Form)
		self.exit_button.setMaximumSize(QtCore.QSize(85, 30))
		self.exit_button.setObjectName("exit_button")
		self.horizontalLayout.addWidget(self.exit_button)
		spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem3)
		self.verticalLayout.addLayout(self.horizontalLayout)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "О программе"))
		self.label.setText(_translate("Form", "Python Registry Umformer (PRUF) GUI, ver 1.0"))
		self.label_2.setText(_translate("Form", "Шалакин Родион Геннадьевич, 2016"))
		self.label_3.setText(_translate("Form", "Научный руководитель: Бакланов Валентин Викторович"))
		self.exit_button.setText(_translate("Form", "Ok"))


################################  END INTERFACE  ##################################

class mainForm(Ui_MainWindow):
	def __init__(self):
		Ui_MainWindow.__init__(self)
		self.window = QtWidgets.QMainWindow()
		self.setupUi(self.window)
		self.registry = None
		self.tree_root = None
		self.search_window = None
		self.mode_value.setText("Все")
		self.open_action.triggered.connect(self.open_action_func)
		self.export_a_action.triggered.connect(self.export_a_action_func)
		self.export_m_action.triggered.connect(self.export_m_action_func)
		self.value_search_action.triggered.connect(self.search_func)
		self.about.triggered.connect(self.about_func)
		self.exit_action.triggered.connect(self.exit_func)
		self.treeWidget.clicked.connect(self.tree_item_click)
		self.view_all.triggered.connect(self.show_all)
		self.change_name.triggered.connect(self.change_name_func)
		self.change_value.triggered.connect(self.change_value_func)
		self.view_deleted.triggered.connect(self.show_only_deleted)
		self.view_nondeleted.triggered.connect(self.show_not_deleted)
		self.save_action.triggered.connect(self.save_changes_function)
		self.renew_action.triggered.connect(self.reload_function)
		self.tableWidget.hideColumn(4)
		self.fname = None
		self.window.show()

	def save_changes_function(self):
		if self.registry is None:
			return
		if "changed" not in self.registry.keys():
			return
		if self.registry["changed"].keys() == 0:
			return
		with open(self.fname, "rb+") as file:
			for key in self.registry["changed"].keys():
				if "name" in self.registry["changed"][key].keys():
					file.seek(key + 0x18, 0)
					a = file.write(self.registry["changed"][key]["name"])
					file.seek(key + 0x6, 0)
					a = file.write(pack("H", len(self.registry["changed"][key]["name"])))
					file.seek(key + 0x14, 0)
					a = file.write(pack("H", 1))
				if "value" in self.registry["changed"][key].keys():
					cell = get_cell(key, self.registry)
					file.seek(key + 0x8)
					type = self.registry["changed"][key]["type"]
					if type == 0 or type == 1 or type == 2 or type == 3 or type == 6 or type == 7 \
							or type == 8 or type == 9 or type == 10:
						a = file.write(pack("H", len(self.registry["changed"][key]["value"])))
					if cell.extended:
						file.seek(cell.value_shift + main_block_size + 0x4, 0)
					else:
						file.seek(key + 0x0C, 0)
					a = file.write(self.registry["changed"][key]["value"])
			file.close()

	def reload_function(self):
		if self.fname is None:
			return
		header, _reg = load_hive(self.fname)
		_reg = restore_deleted_keys(_reg)
		self.registry = _reg
		self.clear_table()
		self.treeWidget.collapseAll()

	def open_action_func(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(self.window, 'Open file', '/home')
		if not fname[0]:
			return
		self.fname = fname[0]
		self.clear_table()
		self.draw_tree()

	def draw_tree(self):
		if self.fname is None:
			return
		if self.treeWidget is not None:
			self.treeWidget.clear()
		header, _reg = load_hive(self.fname)
		_reg = restore_deleted_keys(_reg)
		self.registry = _reg
		name_arr = header.name.replace("\0", "").split("\\")
		if name_arr[len(name_arr) - 1] == "":
			name_arr.pop()
		name = name_arr[len(name_arr) - 1]
		self.tree_root = self.add_parent(self.treeWidget.invisibleRootItem(), 0, name,
		                                 header.shift)
		queue_sh = [header.shift]
		queue_item = [self.tree_root]
		while len(queue_sh) > 0:
			cell_sh = queue_sh.pop(0)
			parent = queue_item.pop(0)
			for child_sh in get_subkeys(cell_sh, _reg):
				child = get_cell(child_sh, _reg)
				node = self.add_child(parent, child.name, child_sh)
				queue_sh.append(child_sh)
				queue_item.append(node)

	def add_parent(self, parent, column, title, data):
		item = QTreeWidgetItem(parent, [title])
		item.setData(column, QtCore.Qt.UserRole, data)
		item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
		# item.setExpanded(True)
		return item

	def add_child(self, parent, name, data):
		item = QTreeWidgetItem(parent, [name])
		item.setData(0, QtCore.Qt.UserRole, data)  # тут надо добвлять смещение
		# item.setCheckState(0, QtCore.Qt.Unchecked)
		return item

	def tree_item_click(self):
		selected = self.treeWidget.selectedItems()
		if len(selected) > 1:
			return
		selected = selected[0]
		shift = selected.data(0, QtCore.Qt.UserRole)
		cell = get_cell(shift, self.registry)
		subeys = get_subkeys(shift, self.registry)
		self.nk_value.setText(str(len(subeys)))
		self.nk_value.repaint()
		self.vk_value.setText(str(cell.count_value))
		self.vk_value.repaint()
		self.timestamp_value.setText(str(datetime(1601, 1, 1) + timedelta(microseconds=cell.timestamp / 10)))
		self.timestamp.repaint()
		self.cell_shift_value.setText(str(shift))
		self.cell_shift_value.repaint()
		self.clear_table()
		row_num = 0
		for value_sh in cell.values:
			try:
				value_cell = get_cell(value_sh, self.registry)
				if value_cell.sign != b"vk":
					continue
			except KeyError:
				continue
			self.tableWidget.insertRow(row_num)
			self.tableWidget.setItem(row_num, 0, QTableWidgetItem(value_cell.name))
			self.tableWidget.setItem(row_num, 1, QTableWidgetItem(value_cell.get_type()))
			self.tableWidget.setItem(row_num, 2, QTableWidgetItem(str(value_cell.get_data_size())))
			self.tableWidget.setItem(row_num, 3, QTableWidgetItem(value_cell.get_data()))
			self.tableWidget.setItem(row_num, 4, QTableWidgetItem(str(value_sh)))
			row_num += 1

	def clear_table(self):
		# удаление строк таблицы с конца, т.к. при удалении первой строки таблица перестраивается
		for i in reversed(range(0, self.tableWidget.rowCount())):
			self.tableWidget.removeRow(i)

	def export_a_action_func(self):
		fname = QtWidgets.QFileDialog.getSaveFileName(self.window, 'Open file', '/home')
		fname = str(fname[0])
		selected = self.treeWidget.selectedItems()
		if len(selected) > 1:
			return
		selected = selected[0]
		shift = selected.data(0, QtCore.Qt.UserRole)
		path = get_cell(shift, self.registry).get_name(self.registry)
		root = get_root(self.registry, path)
		if root == None:
			raise Exception(
				"Ошибка при попытке выполнения переход от корневого раздела файла улья реестра по пути {}".format(path))
		umform(self.registry[0], self.registry, path, fname, True)
		pass

	def export_m_action_func(self):
		fname = QtWidgets.QFileDialog.getSaveFileName(self.window, 'Open file', '/home')
		fname = str(fname[0])
		selected = self.treeWidget.selectedItems()
		if len(selected) > 1:
			return
		selected = selected[0]
		shift = selected.data(0, QtCore.Qt.UserRole)
		path = get_cell(shift, self.registry).get_name(self.registry)
		root = get_root(self.registry, path)
		if root == None:
			raise Exception(
				"Ошибка при попытке выполнения переход от корневого раздела файла улья реестра по пути {}".format(path))
		umform(self.registry[0], self.registry, path, fname, False)
		pass

	def search_func(self):
		self.search_window = Search(self)

	def about_func(self):
		self.about_form = AboutForm()

	def exit_func(self):
		sys.exit()

	def show_only_deleted(self):
		if self.tree_root is None:
			return
		self.treeWidget.clear()
		self.clear_table()
		name_arr = self.registry[0].name.replace("\0", "").split("\\")
		if name_arr[len(name_arr) - 1] == "":
			name_arr.pop()
		name = name_arr[len(name_arr) - 1]
		self.tree_root = self.add_parent(self.treeWidget.invisibleRootItem(), 0, name,
		                                 self.registry[0].shift)
		queue_sh = [self.registry[0].shift]
		queue_item = [self.tree_root]
		while len(queue_sh) > 0:
			cell_sh = queue_sh.pop(0)
			parent = queue_item.pop(0)
			for child_sh in get_subkeys(cell_sh, self.registry):
				child = get_cell(child_sh, self.registry)
				if child.is_deleted() or child.have_deleted_child():
					node = self.add_child(parent, child.name, child_sh)
					queue_sh.append(child_sh)
					queue_item.append(node)
		self.mode_value.setText("Удаленные")

	def show_all(self):
		if self.tree_root is None:
			return
		self.treeWidget.clear()
		self.clear_table()
		name_arr = self.registry[0].name.replace("\0", "").split("\\")
		if name_arr[len(name_arr) - 1] == "":
			name_arr.pop()
		name = name_arr[len(name_arr) - 1]
		self.tree_root = self.add_parent(self.treeWidget.invisibleRootItem(), 0, name,
		                                 self.registry[0].shift)
		queue_sh = [self.registry[0].shift]
		queue_item = [self.tree_root]
		while len(queue_sh) > 0:
			cell_sh = queue_sh.pop(0)
			parent = queue_item.pop(0)
			for child_sh in get_subkeys(cell_sh, self.registry):
				child = get_cell(child_sh, self.registry)
				node = self.add_child(parent, child.name, child_sh)
				queue_sh.append(child_sh)
				queue_item.append(node)
		self.mode_value.setText("Все")

	def show_not_deleted(self):
		if self.tree_root is None:
			return
		self.treeWidget.clear()
		self.clear_table()
		name_arr = self.registry[0].name.replace("\0", "").split("\\")
		if name_arr[len(name_arr) - 1] == "":
			name_arr.pop()
		name = name_arr[len(name_arr) - 1]
		self.tree_root = self.add_parent(self.treeWidget.invisibleRootItem(), 0, name,
		                                 self.registry[0].shift)
		queue_sh = [self.registry[0].shift]
		queue_item = [self.tree_root]
		while len(queue_sh) > 0:
			cell_sh = queue_sh.pop(0)
			parent = queue_item.pop(0)
			for child_sh in get_subkeys(cell_sh, self.registry):
				child = get_cell(child_sh, self.registry)
				if not child.is_deleted():
					node = self.add_child(parent, child.name, child_sh)
					queue_sh.append(child_sh)
					queue_item.append(node)
		self.mode_value.setText("Не удаленные")

	def change_name_func(self):
		if self.tableWidget.currentItem() is None:
			return
		row = self.tableWidget.currentItem().row()
		shift = self.tableWidget.item(row, 4).text()
		self.input_form = InputForm(self, self.registry, shift, True)

	def change_value_func(self):
		if self.tableWidget.currentItem() is None:
			return
		row = self.tableWidget.currentItem().row()
		shift = self.tableWidget.item(row, 4).text()
		self.input_form = InputForm(self, self.registry, shift, False)


class Search(Ui_Form):
	def __init__(self, parent):
		Ui_Form.__init__(self)
		self.window = QtWidgets.QDialog()
		self.parent = parent
		self.setupUi(self.window)
		self.seach_button.clicked.connect(self.search_func)
		self.clear_button.clicked.connect(self.clear_func)
		self.exit_button.clicked.connect(self.close_function)
		self.window.show()

	def close_function(self):
		self.window.close()

	def search_func(self):
		nk_name_enabled = self.checkBox.isChecked()
		vk_name_enabled = self.checkBox_2.isChecked()
		vk_value_enabled = self.checkBox_3.isChecked()
		search_str = self.search_input.text()
		registry = self.parent.registry
		if registry is None:
			return
		for i in reversed(range(0, self.search_table.rowCount())):
			self.search_table.removeRow(i)
		queue_sh = [registry[0].shift]
		row_num = 0
		marked = set()
		find = set()
		find.add(registry[0].shift)
		self.status_label.setText("Выполняется поиск...")
		self.status_label.repaint()
		while len(queue_sh) > 0:
			cell_sh = queue_sh.pop(0)
			for child_sh in get_subkeys(cell_sh, registry):
				if child_sh in find:
					continue
				else:
					find.add(child_sh)
				child = get_cell(child_sh, registry)
				queue_sh.append(child_sh)
				if nk_name_enabled:
					if search_str.lower() in str(child.name).replace("\0", "").lower():
						row_num = self.add_search_row("Раздел: '{}'".format(child.name), child.get_name(registry),
						                              row_num)
				if vk_name_enabled or vk_value_enabled:
					for i in range(0, len(child.values)):
						try:
							cell_vk = get_cell(child.values[i], registry)
							if cell_vk.sign != b"vk":
								continue
						except:
							continue
						if (vk_name_enabled and search_str.lower() in str(cell_vk.name).replace("\0", "").lower()) \
								or (vk_value_enabled and search_str.lower() in str(cell_vk.get_data()).replace("\0",
								                                                                               "").lower()):
							row_num = self.add_search_row("Параметр: '{}'".format(cell_vk.name),
							                              child.get_name(registry), row_num)
		self.search_table.repaint()
		self.status_label.setText("Найдено {} значений.".format(row_num))
		pass

	def add_search_row(self, name, path, row_num):
		self.search_table.insertRow(row_num)
		self.search_table.setItem(row_num, 0, QTableWidgetItem(name))
		self.search_table.setItem(row_num, 1, QTableWidgetItem(path.replace("\0", "")))
		return row_num + 1

	def clear_func(self):
		self.status_label.setText("Результаты очищены.")
		for i in reversed(range(0, self.search_table.rowCount())):
			self.search_table.removeRow(i)
			self.search_table.repaint()

	def exit_func(self):
		print("!!!")


class AboutForm(AboutUI):
	def __init__(self):
		AboutUI.__init__(self)
		self.window = QtWidgets.QDialog()
		self.setupUi(self.window)
		self.exit_button.clicked.connect(self.close_func)
		self.window.show()

	def close_func(self):
		self.window.close()


class InputForm(UI_Input):
	def __init__(self, parent, reg, shift, isName):
		UI_Input.__init__(self)
		self.parent = parent
		self.window = QtWidgets.QDialog()
		self.setupUi(self.window)
		self.accept_button.clicked.connect(self.accept_function)
		self.exit_button.clicked.connect(self.close_func)
		self.shift = int(shift)
		self.reg = reg
		self.isName = isName
		self.cell = get_cell(self.shift, self.reg)
		if isName:
			self.type_value.setText("REG_SZ")
			self.old_value.setText(self.cell.name)
		else:
			self.type_value.setText(self.cell.get_type())
			self.old_value.setText(self.cell.get_data())
		self.window.show()

	def close_func(self):
		self.window.close()

	def accept_function(self):
		value = self.new_value.text()
		self.shift = int(self.shift)
		cell = get_cell(self.shift, self.reg)
		if self.isName:
			if abs(cell.size) < len(value) + 0x19:
				self.raise_exception("Слишком длинное имя! Максимум {} байтов!", abs(cell.size) - 0x19)
				return
			value = bytes(value, "ascii")
		elif cell.is_string():
			value = value.replace("\\0", "\0") + "\0"
			if cell.value_size / 2 - 1 < len(value):
				self.raise_exception("Слишком длинное значение! Максимум {} символов!", int(cell.value_size / 2 - 2))
				return
			value = bytes(value, "UTF-16LE")
		elif cell.is_number():
			hex_form = "0x" in value
			if (cell.type == 4 or cell.type == 5) and hex_form:
				if len(value) <= 10:
					try:
						value = binascii.a2b_hex(value.replace("0x", "").zfill(8))
						value = bytearray(value)
						value.reverse()
						value = bytes(value)
					except:
						self.raise_exception("Некорректное шестнадцатеричное значение")
						return
				else:
					self.raise_exception("Значение выходит за допустимый диапазон {}", cell.get_type())
					return
			elif (cell.type == 4 or cell.type == 5) and not hex_form:
				try:
					value = int(value)
					if value > 0xFFFFFFFF:
						self.raise_exception("Значение выходит за допустимый диапазон {}", cell.get_type())
						return
					value = pack("I", value)
				except:
					self.raise_exception("Некорректное десятичное значение")
					return
			elif cell.type == 11 and hex_form:
				if len(value) <= 18:
					try:
						value = binascii.a2b_hex(value.replace("0x", "").zfill(16))
						value = bytearray(value)
						value.reverse()
						value = bytes(value)
					except:
						self.raise_exception("Некорректное шестнадцатеричное значение")
						return
				else:
					self.raise_exception("Значение выходит за допустимый диапазон {}", cell.get_type())
					return
			elif cell.type == 11 and not hex_form:
				try:
					value = int(value)
					if value > 0xFFFFFFFFFFFFFFFF:
						self.raise_exception("Значение выходит за допустимый диапазон {}", cell.get_type())
						return
					value = pack("Q", value)
				except:
					self.raise_exception("Некорректное десятичное значение")
					return
		else:
			value = value.replace(" ", "")
			if cell.value_size * 2 < len(value):
				self.raise_exception("Слишком длинное значение! Максимум {} байтов!", cell.value_size)
				return
			try:
				value = binascii.a2b_hex(value)
			except:
				self.raise_exception("Некорректное шестнадцатеричное значение")
				return
		property = "name" if self.isName else "value"
		if "changed" not in self.reg.keys():
			self.reg["changed"] = {}
		if self.shift not in self.reg["changed"].keys():
			self.reg["changed"][self.shift] = {}
		self.reg["changed"][self.shift][property] = value
		self.reg["changed"][self.shift]["type"] = cell.type
		if self.isName:
			self.reg[self.shift].name = value.decode("ascii")
		else:
			self.reg[self.shift].value = value
		self.window.close()

	def raise_exception(self, mask, data=""):
		self.error_label.setText(mask.format(data))


############## BEGIN ##############

class RegistryHeader:
	def __init__(self, buffer):
		if len(buffer) != 0x70:
			print("Неверный размер буфера")
		sign, _, timestamp, _, shift, _, name = unpack("4s8pQ16pI8p64s", buffer)
		if sign != b"regf":
			print("Отсутствует сигнатура файла улья")
			exit()
		self.timestamp = timestamp
		self.shift = shift + main_block_size
		self.name = name.decode("UTF-16")

	def to_string(self):
		result = "Hive Header" + "\r\n"
		result += "Timestamp: " + self.timestamp + "\r\n"
		result += "\r\n"
		return result


class BinHeader:
	def __init__(self, buffer):
		if len(buffer) != 0x20:
			print("Неверный размер буфера BinHeader")
		sign, _, bin_size, _ = unpack("4s4pI20p", buffer)
		if sign != b'hbin':
			print("Отсутствует сигнатура рамки!")
		self.sign = sign
		self.bin_size = bin_size


class CellNK:
	error_count = 0
	count = 0

	def __init__(self, buffer, shift):
		self.sign = None
		self.shift = shift
		if len(buffer) < 0x50:
			self.isEmpty = True
			return None
		self.isEmpty = False
		CellNK.count += 1
		size, sign, flag, timestamp, _, shift_parent, count_subkey, _, shift_subkey = unpack("i2sHQ4sII4sI",
		                                                                                     buffer[:0x24])
		count_value, values, shift_desk, shift_classname, _, len_keyname, len_classname = unpack("IIII20sHH",
		                                                                                         buffer[0x28:0x50])
		if sign != b'nk':
			print("отсутствует сигнатура nk!")
		self.deleted = False if size < 0 else True
		self.have_deleted = False
		len_keyname = len_keyname if abs(size) >= 0x50 + len_keyname else 0
		pattern = str(len_keyname) + "s"
		name = unpack(pattern, buffer[0x50:0x50 + len_keyname])[0]
		self.size = size
		self.sign = sign
		self.flag = flag  # флаг кодировки
		self.timestamp = timestamp  # временная метка
		self.shift_parent = shift_parent + main_block_size  # смещение родительского ключа
		self.count_subkey = count_subkey  # количество подразделов
		self.shift_subkey = shift_subkey + main_block_size  # список подразделов
		self.count_value = count_value  # количество параметров
		self.values = values + main_block_size  # список параметров
		self.shift_desk = shift_desk + main_block_size  # смещение дескриптора уровня защиты
		self.shift_classname = shift_classname + main_block_size  # смещение имени класса
		self.len_keyname = len_keyname  # длина имени ключа
		self.len_classname = len_classname  # длина имени класса
		try:
			self.name = name.decode("ascii") if flag == 0x20 else name.decode("UTF-8")
		except:
			CellNK.error_count += 1
			try:
				self.name = name.decode("ascii") if flag != 0x20 else name.decode("UTF-8")
			except:
				pass

	def is_deleted(self):
		return self.deleted

	def have_deleted_child(self):
		return self.have_deleted

	def add_child(self, shift, parent_sh, _registry, restored):
		database = _registry if get_cell(parent_sh, _registry).shift_subkey > 0 else restored
		if not shift in get_subkeys_for_restore(parent_sh, _registry, restored):
			if self.count_subkey == 0:
				try:
					get_cell(self.shift_subkey, _registry).add_child(shift)
				except:
					restored[-1 * self.shift] = CellSubKeysRiLi(pack("i2sH", -8, b"li", 0))
					self.shift_subkey = -1 * self.shift
					get_cell(-1 * self.shift, restored).add_child(shift)
					self.count_subkey += 1
			else:
				get_cell(self.shift_subkey, database).add_child(shift)
		else:
			pass

	def set_vk_list(self, buffer):
		if self.isEmpty:
			return
		if self.count_value == 0:
			self.values = []
			return
		sv = self.values
		size = unpack("i", buffer[sv:sv + 0x4])[0]
		vl_buf = buffer[sv + 0x4:sv + abs(size)]
		result = []
		head = 0
		while head < len(vl_buf) and len(result) < self.count_value:
			param = unpack("I", vl_buf[head:head + 0x4])[0] + main_block_size
			result.append(param)
			head += 4
		self.values = result

	def to_string(self, _registry, is_machine):
		subkeys_count = len(get_subkeys(self.shift, _registry))
		result = "\r\n"
		if is_machine:
			result += "KEY \"{}\"\r\n".format(self.get_name(_registry).replace("\0", ""))
			result += "Time: {}, {}\r\n".format(str(self.timestamp),
			                                    str(datetime(1601, 1, 1) + timedelta(microseconds=self.timestamp / 10)))
			result += "Keys: {}\r\n".format(str(subkeys_count))
			result += "Values: {}\r\n".format(str(self.count_value))
		else:
			result += "<<<<< Раздел: \"{}\" >>>>>\r\n".format(self.get_name(_registry).replace("\0", ""))
			result += "Временная метка: {}\r\n".format(
				str(datetime(1601, 1, 1) + timedelta(microseconds=self.timestamp / 10)))
			result += "Всего подразделов: {}\r\n".format(str(subkeys_count))
			result += "Всего параметров: {}\r\n".format(str(self.count_value))
		result += "\r\n"
		return result

	def get_name(self, _registry):
		name_arr = _registry[0].name.replace("\0", "").split("\\")
		if name_arr[len(name_arr) - 1] == "":
			name_arr.pop()
		name = name_arr[len(name_arr) - 1]
		if get_cell(_registry[0].shift, _registry) != self:
			result = self.name
		else:
			return name
		cell = self
		while cell is not None and cell.shift_parent != _registry[0].shift:
			try:
				cell = get_cell(cell.shift_parent, _registry)
				result = cell.name + "\\" + result
			except Exception:
				cell = None
		return name + "\\" + result


class CellVK:
	# error_count = 0
	# count = 0

	def __init__(self, buffer, shift):
		self.sign = None
		self.shift = shift
		if len(buffer) < 0x18:
			self.isEmpty = True
			return None  # TODO вернуть пустую ячейку значения
		self.isEmpty = False
		self.extended = False
		size, sign, len_valname, len_data, _, pointer, param_type, flag = unpack("i2sHH2pIIH", buffer[:0x16])
		if sign != b'vk':
			print("Отсутствует сигнатура vk!")
		self.deleted = False if size < 0 else True
		len_valname = len_valname if abs(size) >= 0x18 + len_valname else 0
		pattern = str(len_valname) + "s"
		name = unpack(pattern, buffer[0x18:0x18 + len_valname])[0]
		self.size = size  # размер ячейки
		self.sign = sign  # сигнатура
		self.len_valname = len_valname  # длина имени параметра
		self.len_data = len_data  # длина данных
		self.value = pointer  # данные или указатель на них
		self.value_shift = pointer
		self.type = param_type  # тип данных {1..11}
		self.flag = flag  # тип кодировки
		self.isCorrect = True
		try:
			self.name = name.decode("ascii") if flag == 1 else name.decode("UTF-16")
		except:
			try:
				self.name = name.decode("ascii") if flag != 1 else name.decode("UTF-16")
			except:
				pass

	def is_deleted(self):
		return self.deleted

	def have_deleted_child(self):
		return False

	def set_value(self, buffer):
		if self.isEmpty:
			return
		elif self.type == 4 or self.type == 5:
			self.value_size = 4
			return
		elif self.len_data <= 4:
			self.value_size = 4
			self.value = pack("I", self.value)
			# if self.type == 1:
			# 	self.value = self.value.decode("ascii")
			# 	return
			return
		else:
			self.extended = True
			vs = self.value + main_block_size
			size = unpack("i", buffer[vs:vs + 0x4])[0]
			self.value_size = abs(size)
		if self.type == 11:
			value = unpack("q", buffer[vs + 0x4:vs + 0x4 + 0x8])[0]
		if self.is_string():
			pattern = str(self.len_data) + "s"
			value = unpack(pattern, buffer[vs + 0x4:vs + 0x4 + self.len_data])[0] if size != 0 else ""
		elif self.value < len(buffer):
			value = buffer[vs + 0x4:vs + 0x4 + self.len_data]
		else:
			self.isCorrect = False
			return
		self.value = value

	def is_string(self):
		return self.type == 1 or self.type == 2 or self.type == 6 or self.type == 7

	def is_number(self):
		return self.type == 4 or self.type == 5 or self.type == 11

	def get_type(self):
		value_type = ["REG_NONE", "REG_SZ", "REG_EXPAND_SZ", "REG_BINARY", "REG_DWORD", "REG_DWORD_BIG_ENDIAN",
		              "REG_LINK", "REG_MULTI_SZ", "REG_RESOURCE_LIST", "REG_FULL_RESOURCE_DESCRIPTION",
		              "REG_RESOURCE_REQUIREMENTS_LIST", "REG_QWORD"]
		if self.type > 11:
			return "Error type:{}".format(self.type)
		return value_type[self.type]

	def get_data_size(self):
		if self.type == 4 or self.type == 5:
			size = 4
		elif self.type == 11:
			size = 8
		else:
			size = len(self.value)
		return size

	def get_data(self, is_machine=True):
		if self.type == 4 or self.type == 5:
			if isinstance(self.value, bytes):
				self.value = unpack("I", self.value)[0]
			data = "0x" + str(hex(self.value))[2:].zfill(8)
		elif self.type == 11:
			if isinstance(self.value, bytes):
				data = unpack("Q", self.value)[0]
			else:
				data = self.value
			data = "0x" + str(hex(data))[2:].zfill(16)
		elif self.type == 1 or self.type == 2 or self.type == 7:
			pattern = "" if self.type == 1 else ","
			if isinstance(self.value, str):
				return self.value.replace("\0\0", pattern).replace("\0", "")
			else:
				try:
					data = self.value.decode("UTF-16le").replace("\0\0", pattern).replace("\0", "") if len(
						self.value) > 0 else ""
				except UnicodeDecodeError:
					try:
						data = self.value.decode("UTF-16").replace("\0\0", pattern) if len(self.value) > 0 else ""
					except:
						data = str(self.value)
		else:
			if is_machine:
				data = binascii.b2a_hex(self.value).decode("ascii")
				data = re.sub(r'(..)', r'\1 ', data)
			else:
				str_num = 0
				data = "\n"
				for i in range(0, int(len(self.value) / 0x10) + 1):
					data += str(hex(str_num).replace("x", "")).zfill(8) + " | "
					last = (i + 1) * 0x10 if (i + 1) * 0x10 < len(self.value) else len(self.value)
					data += re.sub(r'(....)', r'\1 ',
					               binascii.b2a_hex(self.value[i * 0x10: last]).decode("ascii").ljust(32))
					data += "| "
					try:
						res = ""
						temp = self.value[i * 0x10: last]
						for i in bytes(temp):
							res += chr(i) if i <= 128 and i != 0 else "."
					except:
						res = ""
					data += res
					data += "\r\n"
					str_num += 0x10
		return data

	def to_string(self, is_machine):
		if is_machine:
			result = "VALUE \"{}\"\r\n".format(self.name)
			result += "Size: {} bytes\r\n".format(str(self.get_data_size()))
			result += "Type: {}\r\n".format(self.get_type())
			result += "Data: \"{}\"\r\n".format(self.get_data(is_machine))
		else:
			result = "Имя параметра: \"{}\"\r\n".format(self.name)
			result += "Тип: \"{}\"\r\n".format(self.get_type())
			result += "Данные: \"{}\"\r\n".format(self.get_data(is_machine))
		result += "\r\n"
		return result


class CellSubKeysLfLh:
	def __init__(self, buffer):
		size, sign, subkey_count = unpack("i2sH", buffer[0x0:0x8])
		# if sign != b'lf' or sign != b'lh':
		# 	print("lf or lh!")
		self.size = size
		self.sign = sign
		self.count_subkey = subkey_count
		self.subkeys = []
		head = 0x8
		while head < abs(size):
			shift, crc = unpack("II", buffer[head:head + 0x8])
			shift += main_block_size
			self.subkeys.append([shift, crc])
			head += 0x8

	def get_shift(self, num):
		return self.subkeys[num][0]

	def get_crc(self, num):
		return self.subkeys[num][1]

	def add_child(self, shift):
		if len(self.subkeys) == self.count_subkey:
			self.subkeys.append([shift, 0])
		else:
			self.subkeys[self.count_subkey] = [shift, 0]
		self.count_subkey += 1


class CellSubKeysRiLi:
	def __init__(self, buffer):
		size, sign, subkey_count = unpack("i2sH", buffer[0x0:0x8])
		# if sign != b'ri' or sign != b'li':
		# 	print("ri or li!")
		self.size = size
		self.sign = sign
		self.count_subkey = subkey_count
		self.subkeys = []
		head = 0x8
		while head < abs(size):
			shift = unpack("I", buffer[head:head + 0x4])[0]
			shift += main_block_size
			self.subkeys.append(shift)
			head += 0x4

	def get_shift(self, num):
		return self.subkeys[num]

	def get_crc(self, num):
		return 0

	def add_child(self, shift):
		if len(self.subkeys) == self.count_subkey:
			self.subkeys.append(shift)
		else:
			self.subkeys[self.count_subkey] = shift
		self.count_subkey += 1


# def create_parser():
# 	_parser = argparse.ArgumentParser(
# 		prog="Python Registry Unformer",
# 		description="",
# 		epilog="Created by Canis (canis.ferox@yandex.ru)"
# 	)
# 	_parser.add_argument("--hive", required=True, help="Путь к файлу улью реестра ОС Windows.")
# 	_parser.add_argument("-o", "--out", required=True, help="Имя файла для сохранения")
# 	_parser.add_argument("-p", "--path", help="Путь для извлечения данных улья")
# 	return _parser


def get_first_bytes(buffer, head):
	return buffer[head:head + 0x6]


def what_is(buffer):
	sign, _type = unpack("4s2s", buffer)
	if sign == b'hbin':
		return sign
	types = {b'vk', b'nk', b'ri', b'li', b'lf', b'lh'}
	if _type in types:
		return _type
	return None


def get_item(cell_type, head, buff):
	if cell_type == b'hbin':
		return BinHeader(buff[head:head + 0x20]), 0x20
	size = unpack("i", buff[head:head + 0x4])[0]
	if cell_type == b'vk':
		res = CellVK(buff[head:head + abs(size)], head)
		res.set_value(buff)
		return res, abs(size)
	if cell_type == b'nk':
		res = CellNK(buff[head:head + abs(size)], head)
		res.set_vk_list(buff)
		return res, abs(size)
	if cell_type == b'ri' or cell_type == b'li':
		res = CellSubKeysRiLi(buff[head:head + abs(size)])
		return res, abs(size)
	if cell_type == b'lf' or cell_type == b'lh':
		res = CellSubKeysLfLh(buff[head:head + abs(size)])
		return res, abs(size)
	return None, 1 if size == 0 else abs(size)


def umform(reg_header, _registry, path, out, is_machine):
	root_sh = get_root(_registry, path)
	if root_sh is None:
		print("Не существует указанного пути '{}'".format(path))
		return
	filled = set()
	errors = set()
	queue = [root_sh]
	try:
		with open(out, "a+") as file:
			file.close()
	except:
		print("У вас недостаточно прав для записи по пути {}".format(out))
		return
	with open(out, "w", encoding="UTF-16") as file:
		while len(queue) > 0:
			cell_sh = queue.pop(0)
			if cell_sh in filled:
				errors.add(cell_sh)
				continue
			else:
				filled.add(cell_sh)
			CellNK.count -= 1
			cell = get_cell(cell_sh, _registry)
			file.write(cell.to_string(_registry, is_machine))
			for i in range(0, len(cell.values)):
				try:
					cell_vk = get_cell(cell.values[i], _registry)
					file.write(cell_vk.to_string(is_machine))
				except:
					continue
			temp = get_subkeys(cell_sh, _registry)
			temp.extend(queue)
			queue = temp
	pass


def get_cell(shift, _registry):
	return _registry[shift]


def get_subkeys(parent_sh, _registry):
	queue = []

	parent = get_cell(parent_sh, _registry)
	if parent.sign == b'nk':
		try:
			cell_list = get_cell(parent.shift_subkey, _registry)
		except KeyError:
			return queue
		for i in range(0, cell_list.count_subkey):
			try:
				if get_cell(cell_list.get_shift(i), _registry).sign == b'nk':
					queue.append(cell_list.get_shift(i))
				else:
					queue.extend(get_subkeys(cell_list.get_shift(i), _registry))
			except KeyError:
				pass
	elif parent.sign == b'lf' or parent.sign == b'lh' or parent.sign == b'ri' or parent.sign == b'li':
		for i in range(0, parent.count_subkey):
			try:
				if get_cell(parent.get_shift(i), _registry).sign == b'nk':
					queue.append(parent.get_shift(i))
				else:
					queue.extend(get_subkeys(parent.get_shift(i), _registry))
			except KeyError:
				pass
	return queue


def get_subkeys_for_restore(parent_sh, reg, res):
	queue = []
	parent = get_cell(parent_sh, reg)
	if parent.sign == b'nk':
		try:
			if parent.shift_subkey > 0:
				cell_list = get_cell(parent.shift_subkey, reg)
			else:
				cell_list = get_cell(parent.shift_subkey, res)
		except KeyError:
			return queue
		for i in range(0, cell_list.count_subkey):
			try:
				if get_cell(cell_list.get_shift(i), reg).sign == b'nk':
					queue.append(cell_list.get_shift(i))
				else:
					queue.extend(get_subkeys_for_restore(cell_list.get_shift(i), reg, res))
			except KeyError:
				pass
	elif parent.sign == b'lf' or parent.sign == b'lh' or parent.sign == b'ri' or parent.sign == b'li':
		for i in range(0, parent.count_subkey):
			try:
				if get_cell(parent.get_shift(i), reg).sign == b'nk':
					queue.append(parent.get_shift(i))
				else:
					queue.extend(get_subkeys_for_restore(parent.get_shift(i), reg, res))
			except KeyError:
				pass
	return queue


def get_root(_registry, path):
	path_sp = path.split("\\")
	if path_sp[0] == '':
		path_sp.pop(0)
	name_arr = _registry[0].name.replace("\0", "").split("\\")
	if name_arr[len(name_arr) - 1] == "":
		name_arr.pop()
	reg_name = name_arr[len(name_arr) - 1]
	if reg_name != path_sp.pop(0):
		return None
	if len(path_sp) == 0:
		return _registry[0].shift
	if "CMI-CreateHive{" in path_sp[0]:
		path_sp.pop(0)
	queue = get_subkeys(_registry[0].shift, _registry)
	cell_sh = None
	while len(queue) > 0 and len(path_sp) > 0:
		cell_name = path_sp[0]
		cell_sh = queue.pop(0)
		cell = get_cell(cell_sh, _registry)
		if has_name(cell, cell_name):
			path_sp.pop(0)
			queue = get_subkeys(cell_sh, _registry)
	return None if len(path_sp) > 0 else cell_sh


def has_name(cell, name):
	# ns_1 = {'HKEY_CURRENT_USER', 'HKCU'}
	# ns_2 = {'HKEY_USERS', 'HKU'}
	# ns_3 = {'HKEY_LOCAL_MACHINE', 'HKLM'}
	# ns_4 = {'HKEY_CLASSES_ROOT', 'HKCR'}
	# ns_5 = {'HKEY_CURRENT_CONFIG'}
	# if cell.name in ns_1 and name in ns_1:
	# 	return True
	# if cell.name in ns_2 and name in ns_2:
	# 	return True
	# if cell.name in ns_3 and name in ns_3:
	# 	return True
	# if cell.name in ns_4 and name in ns_4:
	# 	return True
	# if cell.name in ns_5 and name in ns_5:
	# 	return True
	return name == cell.name


def restore_deleted_keys(reg):
	count = 0
	count_all = 0
	restored = {}
	root_cell = get_cell(reg[0].shift, reg)
	try:
		for shift in reg.keys():
			if shift == 0 or shift == "changed":
				continue
			cell = get_cell(shift, reg)
			if cell.sign == b'nk' and cell.is_deleted():
				count_all += 1
				if root_cell.timestamp < cell.timestamp:
					continue
				try:
					if get_cell(cell.shift_parent, reg).sign != b"nk":
						continue
				except:
					continue
				get_cell(cell.shift_parent, reg).add_child(shift, cell.shift_parent, reg, restored)
				set_parent_hdc(cell.shift_parent, reg)
				cell.name = "[DELETED] " + cell.name
				count += 1
	except:
		print("Во время восстановления удаленных ключей произошла ошибка, удаленные ключи отображаться не будут")
		return reg
	# print("{} - {}".format(count_all, count))
	reg.update(restored)
	return reg


def set_parent_hdc(shift, reg):
	try:
		cell = get_cell(shift, reg)
	except:
		return
	cell.have_deleted = True
	if cell.sign != b"nk":
		return
	if cell.shift_parent == reg[0].shift:
		cell = get_cell(reg[0].shift, reg)
		cell.have_deleted = True
		return
	set_parent_hdc(cell.shift_parent, reg)


############## END ##############

def load_hive(hive):
	registry = {}
	with open(hive, "rb") as reg:  # считываем весь бинарный файл улья
		binary_reg = reg.read()
	reg_header = RegistryHeader(binary_reg[:0x70])  # считываем сигнатуру файла улья
	registry[0] = reg_header
	head = 0x1000  # смещение до первого блока
	while head < len(binary_reg) - 5:
		cell_type = what_is(get_first_bytes(binary_reg, head))
		reg_item, head_inc = get_item(cell_type, head, binary_reg)
		if cell_type is not None:
			registry[head] = reg_item
		head += head_inc
	return reg_header, registry


def main():
	# with open(ns.hive, "rb") as reg:  # считываем весь бинарный файл улья
	# 	binary_reg = reg.read()
	# reg_header = RegistryHeader(binary_reg[:0x70])  # считываем сигнатуру файла улья
	# head = 0x1000  # смещение до первого блока
	# while head < len(binary_reg) - 5:
	# 	cell_type = what_is(get_first_bytes(binary_reg, head))
	# 	reg_item, head_inc = get_item(cell_type, head, binary_reg)
	# 	if cell_type is not None:
	# 		registry[head] = reg_item
	# 	head += head_inc
	# umform(reg_header, registry, ns.path, ns.out)
	app = QtWidgets.QApplication(sys.argv)
	form = mainForm()
	sys.exit(app.exec_())
	pass


if __name__ == "__main__":
	# parser = create_parser()
	# namespace = parser.parse_args()
	# main(namespace)
	main()
