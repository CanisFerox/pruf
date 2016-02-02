#!/usr/bin/python3
from PyQt5 import QtWidgets

import argparse
from struct import unpack, pack
import sys
import binascii
import re
from interface import Ui_MainWindow
from search import Ui_Form
import input_form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem, QTableWidgetItem
from datetime import datetime, timedelta

main_block_size = 0x1000
registry = {}


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
		self.tableWidget.hideColumn(4)
		self.window.show()

	def open_action_func(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(self.window, 'Open file', '/home')
		if not fname[0]:
			return
		header, _reg = load_hive(fname[0])
		_reg = restore_deleted_keys(_reg)
		self.registry = _reg
		self.tree_root = self.add_parent(self.treeWidget.invisibleRootItem(), 0, header.name, header.shift)
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
		# удаление строк таблицы с конца, т.к. при удалении первой строки таблица перестраивается
		for i in reversed(range(0, self.tableWidget.rowCount())):
			self.tableWidget.removeRow(i)
		row_num = 0
		for value_sh in cell.values:
			try:
				value_cell = get_cell(value_sh, self.registry)
			except KeyError:
				continue
			self.tableWidget.insertRow(row_num)
			self.tableWidget.setItem(row_num, 0, QTableWidgetItem(value_cell.name))
			self.tableWidget.setItem(row_num, 1, QTableWidgetItem(value_cell.get_type()))
			self.tableWidget.setItem(row_num, 2, QTableWidgetItem(str(value_cell.get_data_size())))
			self.tableWidget.setItem(row_num, 3, QTableWidgetItem(value_cell.get_data()))
			self.tableWidget.setItem(row_num, 4, QTableWidgetItem(str(value_sh)))
			row_num += 1

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
			raise Exception("Ошибка при попытке выполнения переход от корневого раздела файла улья реестра по пути {}".format(path))
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
			raise Exception("Ошибка при попытке выполнения переход от корневого раздела файла улья реестра по пути {}".format(path))
		umform(self.registry[0], self.registry, path, fname, False)
		pass

	def search_func(self):
		self.search_window = Search(self)

	def about_func(self):
		pass

	def exit_func(self):
		sys.exit()

	def show_only_deleted(self):
		if self.tree_root is None:
			return
		self.treeWidget.clear()
		self.tree_root = self.add_parent(self.treeWidget.invisibleRootItem(), 0, self.registry[0].name, self.registry[0].shift)
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
		self.tree_root = self.add_parent(self.treeWidget.invisibleRootItem(), 0, self.registry[0].name, self.registry[0].shift)
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
		self.tree_root = self.add_parent(self.treeWidget.invisibleRootItem(), 0, self.registry[0].name, self.registry[0].shift)
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
		self.input_form = InputForm(self.registry, shift, True)

	def change_value_func(self):
		if self.tableWidget.currentItem() is None:
			return
		row = self.tableWidget.currentItem().row()
		shift = self.tableWidget.item(row, 4).text()
		self.input_form = InputForm(self.registry, shift, False)


class Search(Ui_Form):

	def __init__(self, parent):
		Ui_Form.__init__(self)
		self.window = QtWidgets.QDialog()
		self.parent = parent
		self.setupUi(self.window)
		self.seach_button.clicked.connect(self.search_func)
		self.clear_button.clicked.connect(self.clear_func)
		self.window.show()

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
						row_num = self.add_search_row("Раздел: '{}'".format(child.name), child.get_name(registry), row_num)
				if vk_name_enabled or vk_value_enabled:
					for i in range(0, len(child.values)):
						cell_vk = get_cell(child.values[i], registry)
						if (vk_name_enabled and search_str.lower() in str(cell_vk.name).replace("\0", "").lower()) \
								or (vk_value_enabled and search_str.lower() in str(cell_vk.get_data()).replace("\0", "").lower()):
							row_num = self.add_search_row("Параметр: '{}'".format(cell_vk.name), child.get_name(registry), row_num)
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


class InputForm(input_form.Ui_Form):

	def __init__(self, reg, shift, isName):
		input_form.Ui_Form.__init__(self)
		self.window = QtWidgets.QDialog()
		self.setupUi(self.window)
		self.accept_button.clicked.connect(self.accept_function)
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

	def accept_function(self):
		value = self.new_value.text()
		self.shift = int(self.shift)
		cell = get_cell(self.shift, self.reg)
		if self.isName:
			if abs(cell.size) < len(value) + 0x19:
				self.raise_exception("Слишком длинное имя! Максимум {} байтов!", abs(cell.size) - 0x18)
				return
			value = bytes(value, "ascii")
		elif cell.is_string():
			value = value.replace("\\0", "\0") + "\0"
			if cell.value_size < len(value):
				self.raise_exception("Слишком длинное значение! Максимум {} байтов!", cell.value_size - 1)
				return
			value = bytes(value, "ascii")
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
		prop = "name" if self.isName else "value"
		if "changed" not in self.reg.keys():
			self.reg["changed"] = {}
		if self.shift not in self.reg["changed"].keys():
			self.reg["changed"][self.shift] = {}
		self.reg["changed"][self.shift][prop] = value
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

	def __init__(self, buffer):
		self.sign = None
		if len(buffer) < 0x50:
			self.isEmpty = True
			return None
		self.isEmpty = False
		CellNK.count += 1
		size, sign, flag, timestamp, _, shift_parent, count_subkey, _, shift_subkey = unpack("i2sHQ4sII4sI", buffer[:0x24])
		count_value, values, shift_desk, shift_classname, _, len_keyname, len_classname = unpack("IIII20sHH", buffer[0x28:0x50])
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

	def add_child(self, shift, parent_sh, _registry):
		if not shift in get_subkeys(parent_sh, _registry):
			get_cell(self.shift_subkey, _registry).add_child(shift)

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
		result = "\r\n"
		if is_machine:
			result += "KEY \"{}\"\r\n".format(self.get_name(_registry).replace("\0", ""))
			result += "Time: {}\r\n".format(str(self.timestamp))
			result += "Keys: {}\r\n".format(str(self.count_subkey))
			result += "Values: {}\r\n".format(str(self.count_value))
		else:
			result += "<<<<< Раздел: \"{}\" >>>>>\r\n".format(self.get_name(_registry).replace("\0", ""))
			result += "Временная метка: {}\r\n".format(str(datetime(1601, 1, 1) + timedelta(microseconds=self.timestamp / 10)))
			result += "Всего подразделов: {}\r\n".format(str(self.count_subkey))
			result += "Всего параметров: {}\r\n".format(str(self.count_value))
		result += "\r\n"
		return result

	def get_name(self, _registry):
		result = self.name
		cell = self
		while cell is not None and cell.shift_parent != _registry[0].shift:
			try:
				cell = get_cell(cell.shift_parent, _registry)
				result = cell.name + "\\" + result
			except Exception:
				cell = None
		return _registry[0].name + "\\" + result


class CellVK:
	# error_count = 0
	# count = 0

	def __init__(self, buffer):
		self.sign = None
		if len(buffer) < 0x18:
			self.isEmpty = True
			return None  # TODO вернуть пустую ячейку значения
		self.isEmpty = False
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
			if self.type == 1:
				self.value = self.value.decode("ascii")
				return
			return
		else:
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
		return value_type[self.type]

	def get_data_size(self):
		if self.type == 4 or self.type == 5:
			size = 4
		elif self.type == 11:
			size = 8
		else:
			size = len(self.value)
		return size

	def get_data(self):
		if self.type == 4 or self.type == 5:
			data = "0x" + str(hex(self.value))[2:].zfill(8)
		elif self.type == 11:
			if isinstance(self.value, bytes):
				data = unpack("Q", self.value)[0]
			else:
				data = self.value
			data = "0x" + str(hex(data))[2:].zfill(16)
		elif self.type == 1 or self.type == 2 or self.type == 7:
			if isinstance(self.value, str):
				return self.value.replace("\0", "")
			else:
				try:
					data = self.value.decode("ascii").replace("\0", "") if len(self.value) > 0 else ""
				except UnicodeDecodeError:
					try:
						data = self.value.decode("UTF-16").replace("\0", "") if len(self.value) > 0 else ""
					except:
						data = str(self.value)
		else:
			data = binascii.b2a_hex(self.value).decode("ascii")
			data = re.sub(r'(..)', r'\1 ', data)
		return data

	def to_string(self, is_machine):
		if is_machine:
			result = "VALUE \"{}\"\r\n".format(self.name)
			result += "Size: {} bytes\r\n".format(str(self.get_data_size()))
			result += "Type: {}\r\n".format(self.get_type())
			result += "Data: \"{}\"\r\n".format(self.get_data())
		else:
			result = "Имя параметра: \"{}\"\r\n".format(self.name)
			result += "Тип: \"{}\"\r\n".format(self.get_type())
			result += "Данные: \"{}\"\r\n".format(self.get_data())
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
		res = CellVK(buff[head:head + abs(size)])
		res.set_value(buff)
		return res, abs(size)
	if cell_type == b'nk':
		res = CellNK(buff[head:head + abs(size)])
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
	if root_sh == 0:
		return None
	filled = set()
	errors = set()
	queue = [root_sh]
	with open(out, "a+") as file:
		file.close()
	with open(out, "w") as file:
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
				cell_vk = get_cell(cell.values[i], _registry)
				file.write(cell_vk.to_string(is_machine))
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


def get_root(_registry, path):
	path_sp = path.split("\\")
	if path_sp[0] == '':
		path_sp.pop(0)
	for hive_name_part in _registry[0].name.split("\\"):
		if hive_name_part != path_sp.pop(0):
			return None
	if len(path_sp) == 0:
		return _registry[0].shift
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
	for shift in reg.keys():
		if shift == 0 or shift == "changed":
			continue
		cell = get_cell(shift, reg)
		if cell.sign == b'nk' and cell.is_deleted():
			cell.name = "[DELETED] " + cell.name
			get_cell(cell.shift_parent, reg).add_child(shift, cell.shift_parent, reg)
			set_parent_hdc(cell.shift_parent, reg)
	return reg

def set_parent_hdc(shift, reg):
	cell = get_cell(shift, reg)
	cell.have_deleted = True
	if cell.shift_parent == reg[0].shift:
		cell = get_cell(reg[0].shift, reg)
		cell.have_deleted = True
		return
	set_parent_hdc(cell.shift_parent, reg)


############## END ##############

def load_hive(hive):
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


################################  INTERFACE  ##################################
