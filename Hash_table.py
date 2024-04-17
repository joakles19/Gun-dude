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