# try to make a somewhat useful code for alpha- beta algorithm

class Alpha_Beta:
    def __init__(self,tree):
        self.tree=tree     # incorporate game tree
        self.              # refer to root node
        self.current_node=  # current Game node
        self.sucessors=[]   # list of possible child nodes

    def alpha_beta_search (self,node):
        # zunächst einen Minimax-Algorithmus
        # suche maximalen Wert und dessen Knoten
        # update -> move
        # suche anschließend minimalen Wert usw.
        # backpropagation und Aktualisieren von alpha und beta

        max_val=self.max_value(node)
        max_node= self.get_max_node(node)

    def max_value (self,node):
        pass
        #wenn der Knoten ein leave ist gib eigenen Wert wieder
        # wenn nicht gib den maximalen Wert seiner child nodes wieder

    def get_max_node(self,node):
        child_node=self.get_child_node(node)

    def get_child_node(self,node):
        pass
        #Funktion die alle child nodes ermittelt