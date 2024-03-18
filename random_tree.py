import random
import numpy as np

class TreeNode:
    def __init__(self, data, label):
        self.data = data
        self.children = []
        self.label = label

    def add_child(self, child):
        self.children.append(child)

class Tree:
    def __init__(self, root_data, contour):
        self.root = TreeNode(root_data, 0)
        self.edges = []
        self.contour = contour
        self.corners = []
        self.nodes = []

    def print_tree(self, node, level=0):
        if node is None:
            return
        print("  " * level + str(node.data) + " -> label: " + str(node.label))
        for child in node.children:
            self.print_tree(child, level + 1)

    def find_parent(self, node_data, current_node=None, parent=None):
        if current_node is None:
            current_node = self.root

        if current_node.data == node_data:
            return parent

        for child in current_node.children:
            found_parent = self.find_parent(node_data, child, current_node)
            if found_parent != -1:
                return found_parent

        return -1

def prefix_sum(arr):
    ct = 0
    prefix_arr = []
    for x in arr:
        ct += x
        prefix_arr.append(ct)
    return prefix_arr

def random_contour(n):
    """
    n is the number of edges of the tree
    """
    k = 2 * n + 1
    arr = [i for i in range(k)]
    arr = np.array(arr)
    np.random.shuffle(arr)
    first_n_elem = arr[:n]
    walk = [-1 for i in range(k)]
    for i in range(k):
        if i in first_n_elem:
            walk[i] = 1
    walk_from_root = [0] + walk
    walk = np.array(walk)
    contour = prefix_sum(walk_from_root)
    contour = np.array(contour)
    min_position = np.argmin(contour)
    walk = np.roll(walk, -min_position)
    contour = prefix_sum(walk)
    contour = [0] + contour
    return contour[:-1]

def contour_to_tree(contour):
    print(contour)
    #steps = [1, -1, -1, -1, -1, 0, -1, 0, -1]
    #tmp = 0
    ct = 0
    tree = Tree(str(ct), contour)
    tree.nodes.append(tree.root)
    curr_node = tree.root 
    ct += 1
    for i in range(1, len(contour)):
        if contour[i] > contour[i - 1]:
            step = random.choice([-1, 0, 1])
            label = curr_node.label + step
            #label = curr_node.label + steps[tmp]
            #tmp += 1
            new_node = TreeNode(str(ct), label)      
            curr_node.add_child(new_node)
            # tree.edges.append((curr_node.data, new_node.data))
            tree.edges.append((curr_node, new_node))
            tree.corners.append(curr_node)
            tree.nodes.append(new_node)
            curr_node = tree.nodes[-1]
            ct += 1
        else:
            parent_node = tree.find_parent(curr_node.data)
            # tree.edges.append((curr_node.data, parent_node.data))
            tree.edges.append((curr_node, parent_node))
            tree.corners.append(curr_node)
            curr_node = parent_node
    tree.print_tree(tree.root)
    return tree

    

    

if __name__ == "__main__":
    # tree = Tree("Root")
    # child1 = TreeNode("Child 1")
    # child2 = TreeNode("Child 2")
    # child3 = TreeNode("Child 3")
    # tree.root.add_child(child1)
    # tree.root.add_child(child2)
    # child2.add_child(child3)
    # par = tree.find_parent(tree.root.data)
    # print(par)
    # tree.print_tree(tree.root) 
    n = 10000
    contour = random_contour(n)
    tree = contour_to_tree(contour)
    
    #print(len(contour))