import pygame
import numpy
import random
from math import floor
from sys import exit

#---------------------------------
class character:
    def __init__(self):
        self.pos = [0, 0]
        self.velocity = [0, 0]
        self.goal = [0, 0]
        self._clock = 0
#---------------------------------
def convertPosToArray(x, y):
    xArr = (x - GridSpace[0]) / GridSize
    yArr = (y - GridSpace[1]) / GridSize

    return [int(floor(xArr)), int(floor(yArr))]
#---------------------------------
def _random(x, y):
    return random.uniform(x, y)
#---------------------------------
def drawGrid(x, y, r, g, b):
    pygame.draw.rect(screen, (r, g, b),(GridSpace[0] + GridSize * x, GridSpace[1] + GridSize * y, GridSize - 2, GridSize - 2))
#---------------------------------
def moveToGoal(pos, goal):
    if pos[0] < goal[0]: pos[0] += 1
    elif pos[0] > goal[0]: pos[0] -= 1

    if pos[1] < goal[1]: pos[1] += 1
    if pos[1] > goal[1]: pos[1] -= 1
#---------------------------------

height = 1250
width = 640

pygame.init()
screen = pygame.display.set_mode((height, width))
pygame.display.set_caption("PSEMO's Game")
pygame.display.set_icon(pygame.image.load('icon.png'))

clock = pygame.time.Clock()

GridSpace = [25, 20]
GridSize = 20

GridAmmount = [(height - GridSpace[0] * 2) / GridSize, (width - GridSpace[1] * 2) / GridSize]
GridAmmount = [int(GridAmmount[0]), int(GridAmmount[1])]

MChar = character()
MChar.pos = [int((_random(0, GridAmmount[0]))), int((_random(0, GridAmmount[1])))]
MChar.goal = MChar.pos

game_map = numpy.zeros((GridAmmount[0], GridAmmount[1]))

framerate = 65

selectedUnits = []

while 1:
    LMouseDown = False
    #---------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                LMouseDown = True
    #---------------------------------    
    ms = clock.tick(framerate)
    screen.fill((50, 50, 50))
    #---------------------------------
    MouseX, MouseY = pygame.mouse.get_pos()
    MouseX, MouseY = convertPosToArray(MouseX, MouseY)
    #---------------------------------
    for x in range(GridAmmount[0]):
        for y in range(GridAmmount[1]):
            #highlight the box mouse is over
            if MouseX == x and MouseY == y:
                if LMouseDown:
                    if MChar in selectedUnits:
                        MChar.goal = [x, y]
                        selectedUnits.clear()
                    else:
                        if MChar.pos != [x, y]:
                            game_map[x, y] += 1
                            if game_map[x, y] > 3: game_map[x, y] = 0
                else:
                    drawGrid(x, y, 255, 255, 255)
            else:           
                if game_map[x, y] == 1:
                    drawGrid(x, y, 255, 100, 100)
                elif game_map[x, y] == 2:
                    drawGrid(x, y, 100, 255, 100)
                elif game_map[x, y] == 3:
                    drawGrid(x, y, 100, 100, 255)
                else:
                    drawGrid(x, y, 0, 0, 0) 

            if MChar.pos[0] == x and MChar.pos[1] == y:
                drawGrid(x, y, 0, 255, 0)
    #---------------------------------
    if MChar.pos != MChar.goal:
        MChar._clock += ms
        if MChar._clock > 200:
            MChar._clock = 0
            moveToGoal(MChar.pos, MChar.goal)
    #---------------------------------
    if MChar.pos[0] == MouseX and MChar.pos[1] == MouseY:
        if LMouseDown:
            if MChar not in selectedUnits:
                selectedUnits.append(MChar)
    #---------------------------------
    pygame.display.flip()