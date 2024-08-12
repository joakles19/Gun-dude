#Hash table
class HashTable():

    def __init__(self):
        self.size = 1000
        self.table = [[] for i in range(1000)] 

    def get_hash(self,key):
        sum = 0
        if key != None:
            for letter in key:
                sum += ord(letter)
        return sum
    
    def add(self,key,item):
        hashcode = self.get_hash(key)
        if hashcode >= self.size:
            self.size *= 2
        self.table[hashcode].append(item)
   
    def get(self,key):
        hashcode = self.get_hash(key)
        if len(self.table[hashcode]) == 1:
            return self.table[hashcode][0]
        else:
            return self.table[hashcode]
        
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
        parent = self.find_node(node)
        if parent.left is not None:
            left = parent.left
        else: left = None
        if parent.right is not None:
            right = parent.right
        else: right = None
        return left,right

#Sorting algorithm
def quick_sort(list):
    if len(list) < 2:
        return list
    
    lower = []
    same = []
    higher = []

    pivot = list[int(len(list)/2)][0]

    for item in list:
        if item[0] < pivot:
            lower.append(item)
        elif item[0] > pivot:
            higher.append(item)
        elif item[0] == pivot:
            same.append(item)

    return quick_sort(lower) + same + quick_sort(higher)


