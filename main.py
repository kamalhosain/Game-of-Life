import pygame, sys
from pygame.locals import *
import numpy as np
import time

#INITALIZE PYGAME
pygame.init()

#SCREEN SETTINGS
WIDTHSCREEN, HEIGHTSCREEN = 600,600
BGCOLOR = (25,25,25)
screen = pygame.display.set_mode((WIDTHSCREEN,HEIGHTSCREEN))
screen.fill(BGCOLOR)
pygame.display.set_caption("Conway's Game of Life")

#CELLS
AMOUNTCELLSX, AMOUNTCELLSY = 50,50

WIDTHCELL = WIDTHSCREEN / AMOUNTCELLSX
HEIGHTCELL = HEIGHTSCREEN / AMOUNTCELLSY

#CELL STATE. 1=ALIVE ; 0=DEAD
gameState = np.zeros((AMOUNTCELLSX,AMOUNTCELLSY))

#PAUSE
pausePressed = True

#GAME LOOP
while True:

    newGameState = np.copy(gameState)

    #CLEAN SCREEN
    screen.fill(BGCOLOR)

    time.sleep(0.1)


    events = pygame.event.get()
    for event in events:

        #PAUSE
        if event.type == pygame.KEYDOWN:
            pausePressed = not pausePressed

        #MOUSE CLICK
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            cellX, cellY = int(np.floor(posX / WIDTHCELL)), int(np.floor(posY / HEIGHTCELL))
            newGameState[cellX, cellY] = not mouseClick[2]

        #QUIT
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #GRID
    for y in range(0, AMOUNTCELLSX):
        for x in range(0, AMOUNTCELLSY):

            if not pausePressed:

                #CALCULATE THE NUMBER OF NEIGHBORS
                amountNeighbors = gameState[(x-1) % AMOUNTCELLSX, (y+1) % AMOUNTCELLSY] + \
                                  gameState[x % AMOUNTCELLSX, (y+1) % AMOUNTCELLSY] + \
                                  gameState[(x+1) % AMOUNTCELLSX, (y+1) % AMOUNTCELLSY] + \
                                  gameState[(x-1) % AMOUNTCELLSX, y % AMOUNTCELLSY] + \
                                  gameState[(x+1) % AMOUNTCELLSX, y % AMOUNTCELLSY ] + \
                                  gameState[(x-1) % AMOUNTCELLSX, (y-1) % AMOUNTCELLSY] + \
                                  gameState[x % AMOUNTCELLSX, (y-1) % AMOUNTCELLSY] + \
                                  gameState[(x+1) % AMOUNTCELLSX, (y-1) % AMOUNTCELLSY]

                #RULE_1
                if gameState[x,y] == 0 and amountNeighbors == 3:
                    newGameState[x,y] = 1

                #RULE_2
                elif gameState[x,y] == 1 and (amountNeighbors < 2 or amountNeighbors > 3):
                    newGameState[x,y] = 0

            #CELL POLYGON
            poly = [(x * WIDTHCELL , y * HEIGHTCELL),
                    ((x+1) * WIDTHCELL , y * HEIGHTCELL),
                    ((x+1) * WIDTHCELL , (y+1) * HEIGHTCELL),
                    (x * WIDTHCELL , (y+1) * HEIGHTCELL)]


            if newGameState[x,y] == 0:
                pygame.draw.polygon(screen,(128,128,128),poly,1)
            else:
                pygame.draw.polygon(screen,(255,255,255),poly,0)

    #UPDATE GAMESTATE
    gameState = np.copy(newGameState)

    #UPDATE SCREEN
    pygame.display.flip()