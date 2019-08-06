class FileManipulation(object):
			
	def getPathToFile(self,filename):
		return "{0}/{1}".format(os.getcwd(), filename)
	
	def extractColumnFromFile(self, fileToRead, col, datatype):
		with open(fileToRead) as f:
			return [datatype(line.split(',')[col]) for line in f.readlines()]