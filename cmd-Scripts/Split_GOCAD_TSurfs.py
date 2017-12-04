"""
Created on 04.11.2013

@author: Stephan Donndorf

Split an exported TSurf-File with multiple features in separated files with a single features stored in
"""

import os
import sys

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Wrong number of arguments. Usage: Split_PLine.py <InputFile.ts>! Canceling...")
		sys.exit(1)

	inputFile = os.path.normpath(sys.argv[1])

	if not os.path.exists("out"):
		os.makedirs("out")

	mainDict = {}
	lineList = []
	name = ""
	first = True

	infile = open(inputFile, "r")

	if infile.closed:
		print("Could not open the input file! Canceling...")
		sys.exit(1)

	for line in infile:
		line = line.rstrip()
		if first:
			if line == "GOCAD TSurf 1":
				first = False
				lineList.append(line)
			continue
		else:
			if line == "GOCAD TSurf 1":
				if name == "":
					print("Could not store object, name is not defined!")
					lineList = []
					name = ""
					continue
				mainDict[name] = lineList
				lineList = []
				name = ""
		lineList.append(line)
		splitLine = line.split(": ")
		if (len(splitLine) > 1) and (splitLine[0].strip() == "name"):
			name = splitLine[1].strip()
			print("Found name: %s" % (splitLine[1],))
			print(line)

	if name == "":
		print("Could not store object, name is not defined!")
	else:
		mainDict[name] = lineList
	infile.close()

	# save objects
	for key in mainDict:
		outfile = open("out/" + key + ".ts", "w")
		for line in mainDict[key]:
			outfile.write(line + "\n")
		outfile.close()
