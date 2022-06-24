#!/usr/bin/python3

# author: Deacon Seals

# use: python3 treeCheck.py treeFilePath0 treeFilePath1 ... treeFilePathN
# use note: Bash regex filename expressions supported

import sys
import re # python regex library


def getDepth(line):
	# trying to support arbitratry node strings was a mistake
	return len(line)-len(line.lstrip("|")) # this is kinda gross but it works

'''
desc:	Returns the number of children for a node on a given line.
'''
def numChildren(depths, lineNum):
	myDepth = depths[lineNum]
	children = 0
	for line in range(lineNum+1,len(depths)):
		nodeDepth = depths[line]
		if nodeDepth == myDepth+1:
			children += 1
		elif nodeDepth <= myDepth:
			break
	return children

'''
desc:	Checks tree file at input `filepath` for a valid tree. Considers formatting errors
		that cause tree depth to increase by unreasonable amounts, the number of children
		each node has. A comment is made for each instance of an unknown node, but this 
		does not indicate an error if the node is a new sensor or operator you have added
		and documented.
'''
def checkTree(filename):
	sensors = {"G", "P", "W", "F"}
	operators = {"+":2, "-":2, "*":2, "/":2, "RAND":2}

	# identified sensor nodes
	def isSensor(value):
		numbers = value.split(".")
		return value in sensors or re.fullmatch('(-?[0-9]+(\.[0-9]*)?)',value)

	errors = []
	treeText = []

	with open(filename, 'r') as file:
		treeText = [line.rstrip() for line in file] # remove tailing space from each line
	# remove tailing blank lines from file
	for line in range(len(treeText)):
		if treeText[-(line+1)]:
			if line > 0:
				treeText = treeText[:-line]
			break
	if not treeText:
		print(filename+": [ERROR] is empty")
		return

	depths = [getDepth(line) for line in treeText]
	nodes = [line.lstrip("|") for line in treeText]
	children = [numChildren(depths,line) for line in range(len(treeText))]

	# check for invalid depth increases
	for line in range(len(treeText)-1):
		if depths[line+1]-depths[line] > 1:
			errors.append("depth increased by more than 1 between lines "+repr(line+1)+" and "+repr(line+2))
	
	# somewhat abusive way of breaking if we've already found errors
	if [print(filename+": [ERROR] "+error) for error in errors]: return

	for line in range(len(treeText)):
		node = nodes[line]
		numKids = children[line]
		if isSensor(node): # sensor
			if numKids != 0: # sensor has children but shouldn't
				errors.append("sensor node "+repr(node)+" on line "+repr(line+1)+" has "+repr(numKids)+" more children than it should")
		elif node in operators: # operators
			if numKids != operators[node]: # defined operator has incorrect number of children
				errors.append("operator node "+repr(node)+" on line "+repr(line+1)+" has "+repr(numKids)+" children but "+repr(operators[node])+" were expected")
		else: # unknown node
			print(filename+": [warning] unknown node "+repr(node)+" on line "+repr(line+1)+" has "+repr(numKids)+" children")

	# print errors or pass
	if not [print(filename+": [ERROR] "+error) for error in errors]: # still a little hack-ey
		print(filename+": PASS")
	return

def main():
	if len(sys.argv) < 2:
		print("Please pass in a world file")
	else:
		for arg in range(1,len(sys.argv)):
			checkTree(sys.argv[arg])

if __name__ == '__main__':
	main()