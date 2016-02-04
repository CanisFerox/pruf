#!/usr/bin/python3

import argparse
from struct import unpack, pack
import binascii
from datetime import datetime, timedelta
import re

main_block_size = 0x1000


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

	def add_child(self, shift, parent_sh, _registry):
		if not shift in get_subkeys(parent_sh, _registry):
			if self.count_subkey == 0:
				try:
					get_cell(self.shift_subkey, _registry)
				except:
					return
					# _registry[-1 * self.shift] = CellSubKeysRiLi(pack("i2sH", -8, b"li", 0))
					# self.shift_subkey = -1 * self.shift
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
		if get_cell(_registry[0].shift, _registry) != self:
			result = self.name
		else:
			return _registry[0].name
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

	def get_data(self, is_machine):
		if self.type == 4 or self.type == 5:
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


def create_parser():
	_parser = argparse.ArgumentParser(
		prog="Python Registry Unformer",
		description="Программа производит преобразование указанной ветви бинарного файла улья реестра Windows в текстовый вид.",
		epilog="Created by Canis (canis.ferox@yandex.ru)"
	)
	_parser.add_argument("--hive", required=True, help="Путь к файлу улью реестра ОС Windows.")
	_parser.add_argument("-o", "--out", required=True, help="Имя файла для сохранения")
	_parser.add_argument("-p", "--path", help="Путь для извлечения данных улья")
	_parser.add_argument("-m", "--mode", required=True, choices=["M", "A"],
	                     help="Формат преобразованного файла, M - человекочитаемый формат, A - формат для последующей машинной обработки.")
	return _parser


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
	with open(out, "a+") as file:
		file.close()
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
		if hive_name_part.replace("\0", "") != path_sp.pop(0):
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
	return name == cell.name


def restore_deleted_keys(reg):
	count = 0
	for shift in reg.keys():
		if shift == 0 or shift == "changed":
			continue
		cell = get_cell(shift, reg)
		if cell.sign == b'nk' and cell.is_deleted():
			cell.name = "[DELETED] " + cell.name
			try:
				if get_cell(cell.shift_parent, reg).sign != b"nk":
					continue
			except:
				continue
			get_cell(cell.shift_parent, reg).add_child(shift, cell.shift_parent, reg)
			set_parent_hdc(cell.shift_parent, reg)
	return reg


def set_parent_hdc(shift, reg):
	cell = get_cell(shift, reg)
	cell.have_deleted = True
	if cell.sign != b"nk":
		return
	if cell.shift_parent == reg[0].shift:
		cell = get_cell(reg[0].shift, reg)
		cell.have_deleted = True
		return
	set_parent_hdc(cell.shift_parent, reg)


def main(ns):
	registry = {}
	with open(ns.hive, "rb") as reg:  # считываем весь бинарный файл улья
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
	registry = restore_deleted_keys(registry)
	umform(reg_header, registry, ns.path, ns.out, ns.mode == "A")
	pass


if __name__ == "__main__":
	parser = create_parser()
	namespace = parser.parse_args()
	main(namespace)
