#!/usr/bin/python3

import argparse
from struct import unpack

main_block_size = 0x1000
registry = {}

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

	def toString(self):
		return ""           # TODO toString regHeader


class BinHeader:

	def __init__(self, buffer):
		if len(buffer) != 0x20:
			print("Неверный размер буфера BinHeader")
		sign, _, bin_size, _ = unpack("4s4pI20p", buffer)
		if sign != b'hbin':
			print("Отсутствует сигнатура рамки!")
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
		self.flag = flag                                            # флаг кодировки
		self.timestamp = timestamp                                  # временная метка
		self.shift_parent = shift_parent + main_block_size          # смещение родительского ключа
		self.count_subkey = count_subkey                            # количество подразделов
		self.shift_subkey = shift_subkey + main_block_size          # список подразделов
		self.count_value = count_value                              # количество параметров
		self.values = values + main_block_size                      # список параметров
		if self.values > 12320767 and not empty:
			pass
		self.shift_desk = shift_desk + main_block_size              # смещение дескриптора уровня защиты
		self.shift_classname = shift_classname + main_block_size    # смещение имени класса
		self.len_keyname = len_keyname                              # длина имени ключа
		self.len_classname = len_classname                          # длина имени класса
		try:
			self.name = name.decode("ascii") if flag == 0x20 else name.decode("UTF-16")
		except:
			CellNK.error_count += 1
			try:
				self.name = name.decode("ascii") if flag != 0x20 else name.decode("UTF-16")
			except:
				pass

	def set_vk_list(self, buffer):
		if self.isEmpty:
			return
		if self.count_value == 0:
			self.values = []
			return
		sv = self.values
		size = unpack("i", buffer[sv:sv+0x4])[0]
		vl_buf = buffer[sv+0x4:sv+abs(size)]
		result = []
		head = 0
		while head < len(vl_buf) and len(result) < self.count_value:
			param = unpack("I", vl_buf[head:head+0x4])[0] + main_block_size
			result.append(param)
			head += 4
		self.values = result

	def toString(self):
		return ""           # TODO toString nk


class CellVK:
	error_count = 0
	count = 0

	def __init__(self, buffer):
		if len(buffer) < 0x18:
			self.isEmpty = True
			return None                                             # TODO вернуть пустую ячейку значения
		self.isEmpty = False
		size, sign, len_valname, len_data, _, pointer, param_type, flag = unpack("i2sHH2pIIH", buffer[:0x16])
		if sign != b'vk':
			print("Отсутствует сигнатура vk!")
		deleted = False if size < 0 else True
		len_valname = len_valname if abs(size) >= 0x18 + len_valname else 0
		pattern = str(len_valname) + "s"
		name = unpack(pattern, buffer[0x18:0x18 + len_valname])[0]
		self.size = size                                            # размер ячейки
		self.sign = sign                                            # сигнатура
		self.len_valname = len_valname                              # длина имени параметра
		self.len_data = len_data                                    # длина данных
		self.value = pointer                                        # данные или указатель на них
		if self.value > 12320767 and not deleted:
			CellVK.error_count += 1
			pass
		self.type = param_type                                      # тип данных {1..11}
		self.flag = flag                                            # тип кодировки
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
			CellVK.count += 1
			return
		vs = self.value + main_block_size
		size = unpack("i", buffer[vs:vs+0x4])[0]
		if self.type == 11 and abs(size) == 8:
			value = unpack("q", buffer[vs+0x4:vs+abs(size)])[0]
		if self.isString():
			pattern = str(self.len_data) + "s"
			value = unpack(pattern, buffer[vs+0x4:vs+0x4+self.len_data])[0] if size != 0 else ""
		else:
			value = buffer[vs+0x4:vs+0x4+self.len_data]
		self.value = value

	def isString(self):
		return self.type == 1 or self.type == 2 or self.type == 6 or self.type == 7

	def toString(self):
		return ""           # TODO toString vk, test fot git rep


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
			shift, crc = unpack("II", buffer[head:head+0x8])
			shift += main_block_size
			self.subkeys.append([shift, crc])
			head += 0x8

	def get_shift(self, num):
		return self.subkeys[num][0]

	def get_crc(self, num):
		return self.subkeys[num][1]


class CellSubKeysRiLi:

	def __init__(self, buffer):
		size, sign, subkey_count  = unpack("i2sH", buffer[0x0:0x8])
		# if sign != b'ri' or sign != b'li':
		# 	print("ri or li!")
		self.size = size
		self.sign = sign
		self.count_subkey = subkey_count
		self.subkeys = []
		head = 0x8
		while head < abs(size):
			shift = unpack("I", buffer[head:head+0x4])[0]
			shift += main_block_size
			self.subkeys.append(shift)
			head += 0x4

	def get_shift(self, num):
		return self.subkeys[num]


def create_parser():
	parser = argparse.ArgumentParser(
		prog="Python Registry Unformer",
		description="",
		epilog="Created by Canis (canis.ferox@yandex.ru)"
	)
	parser.add_argument("--hive", required=True, help="Путь к файлу улью реестра ОС Windows.")
	parser.add_argument("-o", "--out", required=True, help="Имя файла для сохранения")
	parser.add_argument("-p", "--path", help="Путь для извлечения данных улья")
	return parser


def get_first_bytes(buffer, head):
	return buffer[head:head+0x6]


def what_is(buffer):
	sign, type = unpack("4s2s", buffer)
	if sign == b'hbin':
		return sign
	types = {b'vk', b'nk', b'ri', b'li', b'lf', b'lh'}
	if type in types:
		return type
	return None


def get_item(type, head, buff):
	if type == b'hbin':
		return BinHeader(buff[head:head+0x20]), 0x20
	size = unpack("i", buff[head:head+0x4])[0]
	if type == b'vk':
		res = CellVK(buff[head:head+abs(size)])
		res.set_value(buff)
		return res, abs(size)
	if type == b'nk':
		res = CellNK(buff[head:head+abs(size)])
		res.set_vk_list(buff)
		return res, abs(size)
	if type == b'ri' or type == b'li':
		res = CellSubKeysRiLi(buff[head:head+abs(size)])
		return res, abs(size)
	if type == b'lf' or type == b'lh':
		res = CellSubKeysLfLh(buff[head:head+abs(size)])
		return res, abs(size)
	return None, 1 if size == 0 else abs(size)


def umform(header, registry, path, out):
	root_sh = get_root(header, registry, path)
	if root_sh == 0:
		return
	queue = [root_sh]
	with open(out, "w") as file:
		while len(queue) > 0:
			cell_sh = queue.pop(0)
			cell = registry[cell_sh]
			file.write(cell.toString())
			queue.extend(get_subkeys(cell_sh, registry))


def get_subkeys(parent_sh, registry):
	queue = []
	parent = registry[parent_sh]
	if parent.sign == "nk":
		for sub_cell_sh in parent.shift_subkey:
			if registry[sub_cell_sh].sign == "nk":
				queue.append(sub_cell_sh)
			else:
				queue.extend(get_subkeys(sub_cell_sh, registry))
	else:
		for num in range(0, len(parent.subkeys)):
			if registry[parent.get_shift(num)].sign == "nk":
				queue.append(parent.get_shift(num))
			else:
				queue.extend(get_subkeys(parent.get_shift(num), registry))
	return queue


def get_root(header, registry, path):
	return 1        # TODO


def main(namespace):
	with open(namespace.hive, "rb") as reg:                     # считываем весь бинарный файл улья
		binary_reg = reg.read()
	reg_header = RegistryHeader(binary_reg[:0x70])              # считываем сигнатуру файла улья
	head = 0x1000                                               # смещение до первого блока
	while head < len(binary_reg) - 5:
		type = what_is(get_first_bytes(binary_reg, head))
		reg_item, head_inc = get_item(type, head, binary_reg)
		if type is not None:
			registry[head] = reg_item
		head += head_inc
	pass
	umform(reg_header, registry, namespace.path, namespace.out)
	pass


if __name__ == "__main__":
	parser = create_parser()
	namespace = parser.parse_args()
	main(namespace)
