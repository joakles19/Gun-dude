#Binary tree

class Node(object):
    def __init__(self,value,content):
        self.node_value = value
        self.node_content = content
        self.left = None
        self.right = None

class Tree(object):
    def __init__(self,root,content):
        self.root = Node(root,content)
        self.tree_list = []

    def insert(self,value,content):
        self.insert_recurs(value,content,self.root)
    def insert_recurs(self,value,content,node):
        if value < node.node_value:
            if node.left is None:
                node.left = Node(value,content)
            else:
                self.insert_recurs(value,content,node.left)
        else:
            if node.right is None:
                node.right = Node(value,content)
            else:
                self.insert_recurs(value,content,node.right)

    def return_tree(self):
        self.preorder_traversal_recurs(self.root)
        return self.tree_list
    def preorder_traversal_recurs(self,node):
        self.tree_list.append(node.node_content)
        if node.left is not None:
            self.preorder_traversal_recurs(node.left)
        if node.right is not None:
            self.preorder_traversal_recurs(node.right)

    def find_node(self,node):
        return self.find_node_recurs(self.root,node)
    def find_node_recurs(self,node,search):
        if search < node.node_value:
            if node.left is None:
                return None
            else:
                return self.find_node_recurs(node.left,search)
        elif search > node.node_value:
            if node.right is None:
                return None
            else:
                return self.find_node_recurs(node.right,search)
        else:
            return node
            
    def find_next_nodes(self,node):
        parent_node = self.find_node(node)
        return parent_node.left,parent_node.right
        
tree = Tree(8,"Hello")
tree.insert(1,"No")
tree.insert(2,"Po")
tree.insert(3,"Jjj")
tree.insert(4,None)
tree.insert(5,None)
tree.insert(6,None)
tree.insert(7,None)

print(tree.find_next_nodes(1))