import pygame, database
pygame.init()
screen = pygame.display.set_mode((1280,720))

class username:
    def __init__(self):
        self.list = []

    def backspace(self):
        if len(self.list) > 0:
            self.list.pop()    

    def add(self,input):
        if (input >= 97 and input <= 122) or (input >= 48 and input <= 58):
            self.type(input)
        if input == 8:
            self.backspace()
        print(self.list)

    def type(self,input):
        alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        numbers = ["0","1","2","3","4","5","6","7","8","9"]
        typekey = ""
        if input >= 97 and input <= 122:
            input -= 97
            typekey = alphabet[input]
        if input >= 48 and input <= 58:
            input -= 48
            typekey = numbers[input]
        if input == 32:
            pass

        self.list.append(typekey)
    


Username = username()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            Username.add(event.key)

    pygame.display.update()