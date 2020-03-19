class Node:
    def __init__(self, name, value=0, parent=None):
        self.Name = name
        self.value = value
        self.parent = parent
        self.children = []    # list

    def Child_node(self, child):
        self.children.append(child)