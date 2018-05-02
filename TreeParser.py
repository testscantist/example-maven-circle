class TreeParser:
	def __init__(self, data, rootName, starting_line, ending_line):
		self.data = data
		self.rootName = rootName
		self.starting_line = starting_line
		self.ending_line = ending_line

	def parse(self):
		treeStart = self.starting_line
		treeEnd = self.ending_line

		with open(self.data) as f:
			content = f.read()

		print('inside TreeParser')
		print('content: ')
		print(content)
		print('treestart:')
		print(treeStart)
		
		rawTree = str.split(content, treeStart+'\n', 1)[1]
		print(rawTree)
		rawTree = str.split(rawTree, '\n' + treeEnd, 1)[0]
		print(rawTree)
		nodeList = str.split(rawTree, '\n')
		print('nodeList: ')
		print(nodeList)

		return nodeList

def main():
	jarName = "[INFO] com.mcmoe:com.mcmoe.jsikulifut13:jar:0.0.1-SNAPSHOT"
	dataFile = "zdependencies.txt"
	nodeList = TreeParser(dataFile, jarName, jarName, 
	"[INFO] ------------------------------------------------------------------------",).parse()
	for rawNode in nodeList:
		print(rawNode)


if __name__ == '__main__':
	main()