######### CLASS TREE  ######### 
import Node

class Tree:
	def __init__(self, root, package_manager):
		self.root = root
		self.package_manager = package_manager
	def getRoot(self):
		return self.root
	def contains(self, node):
		return self.root.contains(node)
	def find(self, node):
		return self.root.find(node)
	def toString(self, tabulate):
		return self.root.buildWithChildren(tabulate)
	def buildWithChildrenToDict(self,tabulate):
		return self.root.buildWithChildrenToDict(tabulate, self.package_manager)
######### END OF CLASS #########