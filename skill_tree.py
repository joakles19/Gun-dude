#Skill tree

class Node(object):
    def __init__(self,value):
        self.node_value = value
        self.left = None
        self.right = None

class Tree(object):
    def __init__(self,root):
        self.root = Node(root)

pwrup_tree = Tree("Base")
pwrup_tree.root.left = Node("Damage up")
pwrup_tree.root.right = Node("Health up")
pwrup_tree.root.left.left = Node("Damage up 2")
pwrup_tree.root.left.right = Node("Fire rate up")
pwrup_tree.root.right.left = Node("Coin Multiplier")
pwrup_tree.root.right.right = Node("Health up 2")
pwrup_tree.root.left.left.left = Node("Damage up 3")
pwrup_tree.root.left.left.right = Node("Lazer")
pwrup_tree.root.left.right.left = Node("Fire rate up 2")
pwrup_tree.root.left.right.right = Node("More nukes")
pwrup_tree.root.right.left.left = Node("Coin multiplier 2")
pwrup_tree.root.right.left.right = Node("Invincibilty")
pwrup_tree.root.right.right.left = Node("[Passive healing")
pwrup_tree.root.right.right.right = Node("Health up 3")

print(pwrup_tree.root.right.node_value)