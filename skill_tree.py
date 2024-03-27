#Binary tree

class Node(object):
    def __init__(self,value):
        self.node_value = value
        self.left = None
        self.right = None

class Tree(object):
    def __init__(self,root):
        self.root = Node(root)
        self.tree_list = []
    
    def return_tree(self):
        self.preorder_traversal(self.root)
        return self.tree_list

    def preorder_traversal(self,node):
        self.tree_list.append(node.node_value)
        if node.left is not None:
            self.preorder_traversal(node.left)
        if node.right is not None:
            self.preorder_traversal(node.right)