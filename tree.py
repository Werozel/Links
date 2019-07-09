
class Node:

    def __init__(self, data, parent=None):
        self.children = []
        self.data = data
        self.parent = parent

    def insert(self, node):
        self.children.append(node)