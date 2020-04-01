import numpy as np
import time

 
class GameTree:

    def __init__(self, **kwargs):
        self.levels = kwargs.get('levels', 3) - 1
        self.childs = kwargs.get('childs', 2)
        self.n_nodes = self.childs ** (self.levels) + 1
        self.tree = {}

        self.t1 = 0
        self.t2 = 0
        self.t3 = 0
        self.t4 = 0

    def create_tree(self):
        # instantiate root node
        self.tree[0] = {'children':[]}
        c = 1
        for level in range(self.levels + 1):
            if level == 0:
                self.tree[0] = {'children':[*range(1, 1 + self.childs)]}
            else:
                t = time.time()
                n_low_current = sum(self.childs**i for i in range(0, level))
                n_high_current = n_low_current + self.childs ** level
                self.t1 += time.time() - t

                t = time.time()
                n_low_next = sum(self.childs**i for i in range(0, (level+1)))
                n_high_next = n_low_next + self.childs ** (level+1)
                self.t2 += time.time() - t

                t = time.time()
                all_children = np.array([*range(n_low_next, n_high_next)])
                children = np.split(all_children, len(all_children)/self.childs)
                self.t3 += time.time() - t

                t = time.time()
                for node, cs in zip(range(n_low_current, n_high_current), children):
                    self.tree[node] = {'children': cs.tolist()}
                self.t4 += time.time() - t
                c +=1

    def ddd(self):
        self.create_tree()

G = GameTree(levels=3, childs=4)
G.levels
G.create_tree()

