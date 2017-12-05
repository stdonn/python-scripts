#!/usr/bin/env python

import os
import sys


class TextColors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


class ObjectData:
	def __init__(self):
		self.startLine = ""
		self.ID_dict = {}

	def __init__(self, startLine):
		self.startLine = startLine
		self.ID_dict = {}

	def parseObjectData(self, start_ID):
		node = start_ID
		parseTree = dict()  # dictionary stores last node according tree depth
		valueList = list()  # stores all found node values
		T = 0  # path depth equivalent to recursion depth
		parseTree[T] = node
		valueList.append(node)
		while T >= 0:
			found = False
			for elem in (self.ID_dict[node][3], self.ID_dict[node][4], self.ID_dict[node][5]):
				if (elem in valueList) or (elem == 0):
					continue
				T += 1
				found = True
				node = elem
				parseTree[T] = node  # current element in path depth
				valueList.append(node)
				break  # stop for-loop and restart while-loop with new node element
			if not found:
				T -= 1
				if T >= 0:  # list index out of range exception if T < 0
					node = parseTree[T]  # go back to last tree node and search for a new path
			if T > len(self.ID_dict.keys()):
				print(TextColors.BOLD + TextColors.FAIL + "Reached maximum iteration depth {} - ITERATION ERROR".format(len(self.ID_dict.keys())) + TextColors.ENDC)
				print("Iteration depth: {}".format(T))
		return valueList

	def parseObjectDataRecursive(self, ID, result):
		(ID1, ID2, ID3) = (self.ID_dict[ID][3], self.ID_dict[ID][4], self.ID_dict[ID][5])
		if (ID1 != 0) and (ID1 not in result):
			result.append(ID1)
			self.parseObjectDataRecursive(ID1, result)

		if (ID2 != 0) and (ID2 not in result):
			result.append(ID2)
			self.parseObjectDataRecursive(ID2, result)

		if (ID3 != 0) and (ID3 not in result):
			result.append(ID3)
			self.parseObjectDataRecursive(ID3, result)


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print(TextColors.FAIL + "Wrong number of arguments! Canceling..." + TextColors.ENDC)
		print(TextColors.FAIL + "Usage: Split_SURPAC_DTM.py <input DTM> <output DTM>" + TextColors.ENDC)
		sys.exit(0)

	Objects = list()
	inFileName = os.path.normpath(sys.argv[1])
	outFileName = os.path.normpath(sys.argv[2])

	print("\nStart reading inputFile...")
	inFile = open(inFileName, 'r')

	startLines = list()
	startLines.append(inFile.readline().rstrip())
	startLines.append(inFile.readline().rstrip())

	inFile.readline()  # ignore first "OBJECT ..." line
	objData = ObjectData(inFile.readline().rstrip())

	foundEnd = False
	for line in inFile:
		line = line.rstrip()
		if line == "END":  # EOF
			Objects.append(objData)
			foundEnd = True
			break

		line = line.split(',')

		if (line[0]) == "OBJECT":
			Objects.append(objData)
			objData = ObjectData(inFile.readline().rstrip())
			continue

		objData.ID_dict[int(line[0])] = [int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6])]

	if not foundEnd:
		Objects.append(objData)
		print(TextColors.WARNING + TextColors.BOLD + "WARNING: abrupt file ending!" + TextColors.ENDC)

	inFile.close()
	print("Finished reading inputFile")

	print("\nFound {} objects in {}".format(len(Objects), inFileName))
	newObjects = list()
	count = 1
	for obj in Objects:
		print("Parsing object {} of {}".format(count, len(Objects)))
		print("Maximum iteration depth: {}".format(len(obj.ID_dict.keys())))
		count += 1

		while len(obj.ID_dict) > 0:
			key = list(obj.ID_dict.keys())[0]
			results = obj.parseObjectData(key)
			# print("{} - {}".format(len(results), results))
			newObj = ObjectData(obj.startLine)
			# print("{} - {}".format(key, results))
			# print(list(obj.ID_dict.keys()))
			for i in results:
				newObj.ID_dict[i] = obj.ID_dict.pop(i)
			newObjects.append(newObj)

	print(TextColors.OKGREEN + "New Objects: {}".format(len(newObjects)) + TextColors.ENDC)
	# for obj in newObjects:
	# 	print("-------------------------------------------------------\nStartline:\t{}".format(obj.startLine))
	# 	text=""
	# 	for key in obj.ID_dict:
	# 		print("{}".format(obj.ID_dict[key]))
	# 		text += "{} - ".format(key)
	# 	text = text[:-2]
	# 	print("Object keys:\t{}\nStartline:\t{}".format(text, obj.startLine))
	# 	print("Object with {} Elements: {}".format(len(obj.ID_dict), obj.startLine))

	print("Start exporting objects...")

	outFile = open(outFileName, 'w', encoding="utf-8", newline='\r\n')  # newline representation for windows usage!
	for line in startLines:
		outFile.write("{}\n".format(line))

	# outFile.writelines(startLines)
	count = 10
	for obj in newObjects:
		# obj = ObjectData()
		outFile.write("OBJECT, {},\n".format(count))
		count += 1
		outFile.write("{}\n".format(obj.startLine))
		keys = list(obj.ID_dict.keys())
		keys.sort()
		# print("keys: {}\n".format(keys))
		# print("{}\n".format(keys))
		for key in keys:
			outFile.write("{}".format(key))
			for i in obj.ID_dict[key]:
				outFile.write(", {}".format(i))
			outFile.write(",\n")

	outFile.write("END\n")
	outFile.close()

	print("Finished exporting objects...")
