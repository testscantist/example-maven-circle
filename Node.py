######### CLASS NODE  ######### 
MAVEN_PACKAGE_MANAGER = "mvn"
GRADLE_PACKAGE_MANAGER = "gradle"

class Node:
	def __init__(self, data):
		self.parent = None
		self.level = 0
		self.data = data
		self.children = []

	def getData(self):
		return self.data
	def getChildren(self):
		return self.children
	def getLevel(self):
		return self.level
	def getParent(self):
		return self.parent

	def addChild(self, node):
		if(self.__class__ == node.__class__):
			node.parent = self
			node.level = self.level + 1
			self.children.append(node)

	def equals(self, other):
		if(self.__class__ == other.__class__):
			if(self.data == other.data):
				return True;
		return False
	def contains(self, other):
		found = False
		if(self.__class__ == other.__class__):
			if(self.data == other.data):
				found = True;
			else:
				for child in self.children:
					found = child.contains(other)
					if(found == True):
						break
		return found

	def find(self, other):
		foundNode = None
		if(self.__class__ == other.__class__):
			if(self.data == other.data):
				foundNode = self;
			else:
				for child in self.children:
					foundNode = child.find(other)
					if(foundNode != None):
						break
		return foundNode
	def toString(self, tabulate):
		tabs = ' '
		if(tabulate):
			for i in range(0, self.level):
				tabs += '  '
		return str(self.level) + tabs + self.data + '\n'
	def buildWithChildren(self, tabulate):
		result = self.toString(tabulate)
		for child in self.children:
			result += child.buildWithChildren(tabulate)
		return result
	
	def buildWithChildrenToDict(self, tabulate, package_manager):
		if package_manager == MAVEN_PACKAGE_MANAGER:
			version_index = 3
		if package_manager == GRADLE_PACKAGE_MANAGER:
			version_index = 2
		plain_text = self.toString(tabulate)

		plain_text_start_with_library = plain_text.rfind(' ')+1 if self.level == 0 else plain_text.rfind('- ')+2
		plain_text = plain_text[plain_text_start_with_library:]
		end_index_of_library = plain_text.find(' ') if plain_text.find(' ') > 0 else -1
		plain_text = plain_text[:end_index_of_library]
		key_values = plain_text.split(":")
		result = {
			"group_id":key_values[0],
			"artifact_id":key_values[1],
			"version":key_values[version_index],
			"level":self.level,
			"children":[]
		}
		for child in self.children:
			result["children"].append(child.buildWithChildrenToDict(tabulate,package_manager))
		return result

	def buildWithAncestors(self, tabulate):
		result = ''
		if(self.parent is not None):
			result = self.parent.buildWithAncestors(tabulate)
		return result + self.toString(tabulate)

######### END OF CLASS ######### 

def main():
	node = Node("hello world")
	print(node.getData())

if __name__ == "__main__":
	main()