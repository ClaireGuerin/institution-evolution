import os 

def getPathToFile(filename, dirname=""):
	f = '{0}/{1}'.format(dirname,filename)
	return "{0}/{1}".format(os.getcwd(), f)
	
def searchFile(fileToRead, string):
	with open(fileToRead) as f:
		if string in f.read():
			assert True
		else:
			assert False, "{0} not provided in {1}".format(string, fileToRead)		
	
def extractColumnFromFile(fileToRead, col, datatype):
	with open(fileToRead) as f:
		return [datatype(line.split(',')[col]) for line in f.readlines()]