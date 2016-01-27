#!/usr/bin/python3
from PyQt5 import QtWidgets

import argparse
from struct import unpack, pack
import sys
import binascii
import re
from interface import Ui_MainWindow
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
		self.mode_value.setText("Все")
		self.open_action.triggered.connect(self.open_action_func)
		self.export_a_action.triggered.connect(self.export_a_action_func)
		self.export_m_action.triggered.connect(self.export_m_action_func)
		self.value_search_action.triggered.connect(self.search_func)
		self.about.triggered.connect(self.about_func)
		self.exit_action.triggered.connect(self.exit_func)
		self.treeWidget.clicked.connect(self.tree_item_click)
		self.window.show()

	def open_action_func(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(self.window, 'Open file', '/home')
		if not fname[0]:
			return
		column = 0
		header, registry = load_hive(fname[0])
		self.registry = registry
		self.tree_root = self.add_parent(self.treeWidget.invisibleRootItem(), column, header.name, header.shift)
		queue_sh = [header.shift]
		queue_item = [self.tree_root]
		while len(queue_sh) > 0:
			cell_sh = queue_sh.pop(0)
			parent = queue_item.pop(0)
			for child_sh in get_subkeys(cell_sh, registry):
				child = get_cell(child_sh, registry)
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
		subeys = get_subkeys(shift, self.registry, set())
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
			row_num += 1

	def export_a_action_func(self):
		fname = QtWidgets.QFileDialog.getSaveFileName(self.window, 'Open file', '/home')
		selected = self.treeWidget.selectedItems()
		if len(selected) > 1:
			return
		selected = selected[0]
		shift = selected.data(0, QtCore.Qt.UserRole)
		path = get_cell(shift, self.registry).get_name(self.registry)
		root = get_root(self.registry, path)
		if root == None:
			raise "Ошибка при попытке выполнения переход от корневого раздела файла улья реестра по пути path"
		umform(self.registry[0], self.registry, path, fname)
		pass

	def export_m_action_func(self):
		pass

	def search_func(self):
		pass

	def about_func(self):
		pass

	def exit_func(self):
		pass

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
		if len(buffer) < 0x50:
			self.isEmpty = True
			return None
		self.isEmpty = False
		CellNK.count += 1
		size, sign, flag, timestamp, _, shift_parent, count_subkey, _, shift_subkey = unpack("i2sHQ4sII4sI", buffer[:0x24])
		count_value, values, shift_desk, shift_classname, _, len_keyname, len_classname = unpack("IIII20sHH", buffer[0x28:0x50])
		if sign != b'nk':
			print("отсутствует сигнатура nk!")
		empty = False if size < 0 else True
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
		if self.values > 12320767 and not empty:
			pass
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

	def to_string(self, _registry):
		result = "\r\n"
		result += "KEY \"" + self.get_name(_registry) + "\"\r\n"
		result += "Time: " + str(self.timestamp) + "\r\n"
		result += "Keys: " + str(self.count_subkey) + "\r\n"
		result += "Values: " + str(self.count_value) + "\r\n"
		result += "\r\n"
		return result

	def get_name(self, _registry):
		result = self.name
		cell = self
		while cell is not None and cell.shift_parent != _registry[0].shift:
			try:
				cell = get_cell(cell.shift_parent, _registry)
				result = cell.name + "/" + result
			except Exception:
				cell = None
		return _registry[0].name + "/" + result


class CellVK:
	# error_count = 0
	# count = 0

	def __init__(self, buffer):
		if len(buffer) < 0x18:
			self.isEmpty = True
			return None  # TODO вернуть пустую ячейку значения
		self.isEmpty = False
		size, sign, len_valname, len_data, _, pointer, param_type, flag = unpack("i2sHH2pIIH", buffer[:0x16])
		if sign != b'vk':
			print("Отсутствует сигнатура vk!")
		deleted = False if size < 0 else True
		len_valname = len_valname if abs(size) >= 0x18 + len_valname else 0
		pattern = str(len_valname) + "s"
		name = unpack(pattern, buffer[0x18:0x18 + len_valname])[0]
		self.size = size  # размер ячейки
		self.sign = sign  # сигнатура
		self.len_valname = len_valname  # длина имени параметра
		self.len_data = len_data  # длина данных
		self.value = pointer  # данные или указатель на них
		self.value_shift = pointer
		# if self.value > 12320767 and not deleted:
		# 	CellVK.error_count += 1
		# 	pass
		self.type = param_type  # тип данных {1..11}
		self.flag = flag  # тип кодировки
		try:
			self.name = name.decode("ascii") if flag == 1 else name.decode("UTF-16")
		except:
			try:
				self.name = name.decode("ascii") if flag != 1 else name.decode("UTF-16")
			except:
				pass

	def set_value(self, buffer):
		if self.isEmpty:
			return
		if self.type == 4 or self.type == 5:
			return
		if self.value > len(buffer):
			# CellVK.count += 1
			return
		if self.len_data == 4 and self.type == 1:
			self.value = pack("I", self.value).decode("ascii")
			return
		elif self.len_data < 4 and self.type == 1:
			self.value = pack("H", self.value).decode("ascii")
			return
		vs = self.value + main_block_size
		size = unpack("i", buffer[vs:vs + 0x4])[0]
		if self.type == 11 and abs(size) == 8:
			value = unpack("q", buffer[vs + 0x4:vs + abs(size)])[0]
		if self.is_string():
			pattern = str(self.len_data) + "s"
			value = unpack(pattern, buffer[vs + 0x4:vs + 0x4 + self.len_data])[0] if size != 0 else ""
		else:
			value = buffer[vs + 0x4:vs + 0x4 + self.len_data]
		self.value = value

	def is_string(self):
		return self.type == 1 or self.type == 2 or self.type == 6 or self.type == 7

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
			data = "0x" + str(hex(self.value))[2:].zfill(16)
		elif self.type == 1 or self.type == 2 or self.type == 7:
			if isinstance(self.value, str):
				return self.value
			else:
				data = self.value.decode("ascii") if len(self.value) != 0 else ""
		else:
			data = binascii.b2a_hex(self.value).decode("ascii")
			data = re.sub(r'(..)', r'\1 ', data)
		return str(data)

	def to_string(self):
		result = "VALUE \"" + self.name + "\"" + "\r\n"
		result += "Size: " + str(self.get_data_size()) + " bytes\r\n"
		result += "Type: " + self.get_type() + "\r\n"
		result += "Data: " + self.get_data() + "\r\n"
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


def umform(reg_header, _registry, path, out):
	root_sh = get_root(_registry, path)
	if root_sh == 0:
		return None
	filled = set()
	errors = set()
	queue = [root_sh]
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
			file.write(cell.to_string(_registry))
			for i in range(0, len(cell.values)):
				cell_vk = get_cell(cell.values[i], _registry)
				file.write(cell_vk.to_string())
			temp = get_subkeys(cell_sh, _registry)
			temp.extend(queue)
			queue = temp
	pass


def get_cell(shift, _registry):
	return _registry[shift]


def get_subkeys(parent_sh, _registry, marked=set()):
	queue = []
	if parent_sh in marked:
		return queue
	else:
		marked.add(parent_sh)
	parent = get_cell(parent_sh, _registry)
	if parent.sign == b'nk':
		try:
			cell_list = get_cell(parent.shift_subkey, _registry)
		except KeyError:
			return queue
		for i in range(0, len(cell_list.subkeys)):
			try:
				if get_cell(cell_list.get_shift(i), _registry).sign == b'nk':
					queue.append(cell_list.get_shift(i))
				else:
					queue.extend(get_subkeys(cell_list.get_shift(i), _registry, marked))
			except KeyError:
				pass
	elif parent.sign == b'lf' or parent.sign == b'lh' or parent.sign == b'ri' or parent.sign == b'li':
		for i in range(0, len(parent.subkeys)):
			try:
				if get_cell(parent.get_shift(i), _registry).sign == b'nk':
					queue.append(parent.get_shift(i))
				else:
					queue.extend(get_subkeys(parent.get_shift(i), _registry, marked))
			except KeyError:
				pass
	return queue


def get_root(_registry, path):
	path_sp = path.split("/")
	if path_sp[0] == '':
		path_sp.pop(0)
	if _registry[0].name != path_sp.pop(0):
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