# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created: Sun Jan 24 23:46:48 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

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
        spacerItem1 = QtWidgets.QSpacerItem(40, 16, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
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
        spacerItem3 = QtWidgets.QSpacerItem(40, 16, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
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
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
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
        self.export_2.addAction(self.export_a_action)
        self.export_2.addAction(self.export_m_action)
        self.file.addAction(self.open_action)
        self.file.addAction(self.save_action)
        self.file.addAction(self.export_2.menuAction())
        self.file.addAction(self.exit_action)
        self.search.addAction(self.value_search_action)
        self.view_mode.addAction(self.view_deleted)
        self.view_mode.addAction(self.view_nondeleted)
        self.view_mode.addAction(self.view_all)
        self.view.addAction(self.view_mode.menuAction())
        self.help.addAction(self.about)
        self.menubar.addAction(self.file.menuAction())
        self.menubar.addAction(self.search.menuAction())
        self.menubar.addAction(self.view.menuAction())
        self.menubar.addAction(self.help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
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
        self.file.setTitle(_translate("MainWindow", "Файл"))
        self.export_2.setTitle(_translate("MainWindow", "Экспорт"))
        self.search.setTitle(_translate("MainWindow", "Поиск"))
        self.view.setTitle(_translate("MainWindow", "Вид"))
        self.view_mode.setTitle(_translate("MainWindow", "Режим отображения"))
        self.help.setTitle(_translate("MainWindow", "Помощь"))
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

