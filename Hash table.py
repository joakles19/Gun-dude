import pygame
pygame.init()

#Hash table

class HashTable():

    def __init__(self):
        self.size = 1000
        self.table = [None] * self.size

    def add(self, item):
        hashcode = self.hash(item)
        if hashcode >= self.size:
            # Resize the table.
            self.size *= 2
            # etc.
        else:
            self.table[hashcode] = item

    def hash(key):
        sum = 0
        if key != None:
            for letter in key:
                sum += ord(letter)
        print(sum)