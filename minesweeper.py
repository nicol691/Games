# Memory Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *


FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 10 # number of columns of icons
BOARDHEIGHT = 7 # number of rows of icons
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

NoMines = 10

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = RED

MINE = 'mine'
EMPTY = 'empty'
ZERO='0'
ONE = '1'
TWO = '2'
THREE = '3'
FOUR = '4'
FIVE = '5'
SIX = '6'
SEVEN = '7'
EIGHT = '8'
ALLSHAPES = (MINE, EMPTY)
pygame.init()

#add music
pygame.mixer.music.load('minemusic.wav')
pygame.mixer.music.play(-1)


print("Input level difficulty: 1(easy), 2(medium), 3(hard)")
gameLevel = int(input())

if gameLevel == 1:
    BOARDWIDTH = 5 
    BOARDHEIGHT = 5 
    NoMines = 4
if gameLevel == 2:
    BOARDWIDTH = 10 
    NoMines = 10
if gameLevel == 3:
    WINDOWWIDTH = 800 
    WINDOWHEIGHT = 800
    BOARDWIDTH = 14 
    BOARDHEIGHT = 10 
    NoMines = 20
                
def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Minesweeper Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)
    
 


    
    DISPLAYSURF.fill(BGCOLOR)
#NB    startGameAnimation(mainBoard))


    GameRunning = True
    while True: # main game loop
        mouseClicked = False
        flagClicked = False
       
        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, revealedBoxes)
        #GameImage = pygame.image.load("moon.png")
        #DISPLAYSURF.blit(GameImage,(300,0))
        #pygame.display.update()
       
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                mousePos = True
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if event.button == 1:
                    mouseClicked = True
                elif event.button == 3:
                    flagClicked = True    
    
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            #if not revealedBoxes[boxx][boxy] and GameRunning:
               # drawHighlightBox(boxx, boxy)         
            if not revealedBoxes[boxx][boxy] and mouseClicked and GameRunning and not getFlag(mainBoard, boxx, boxy):
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # set the box as "revealed"

            if flagClicked and GameRunning:
                reverseFlag(mainBoard, boxx, boxy)
   
            iconshape = getShapeColorNumber(mainBoard, boxx, boxy)
                
            if iconshape[0] == MINE and mouseClicked == True:
                GameRunning = False
                for x in range(BOARDWIDTH):
                    for y in range(BOARDHEIGHT):
                        ishape = getShapeColorNumber(mainBoard, x, y)
                        if ishape[0] == MINE:
                            revealedBoxes[x][y] = True
                        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
 
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    # puts mines
    icons = []
    for i in range(NoMines):
        icons.append([MINE, ORANGE, 0, False])
    for i in range(BOARDWIDTH*BOARDHEIGHT-NoMines):
        icons.append([EMPTY, ORANGE, 0, False])
    random.shuffle(icons) # randomize the order of the icons list
 
    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)

 
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y][0] == MINE:
                if y > 0:
                    board[x][y-1][2] = board[x][y-1][2] + 1
                if y < BOARDHEIGHT-1:
                    board[x][y+1][2] = board[x][y+1][2] + 1
                if x > 0:
                    board[x-1][y][2] = board[x-1][y][2] + 1
                if x < BOARDWIDTH-1:
                    board[x+1][y][2] = board[x+1][y][2] + 1
                if x > 0 and y < BOARDHEIGHT-1:
                    board[x-1][y+1][2] = board[x-1][y+1][2] + 1
                if y > 0 and x < BOARDWIDTH-1:
                    board[x+1][y-1][2] = board[x+1][y-1][2] + 1
                if x < BOARDWIDTH-1 and y < BOARDHEIGHT-1:
                    board[x+1][y+1][2] = board[x+1][y+1][2] + 1
                if x > 0 and y > 0:
                    board[x-1][y-1][2] = board[x-1][y-1][2] + 1
    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, number, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half =    int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == MINE:
        pygame.draw.circle(DISPLAYSURF, RED, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
        pygame.draw.rect(DISPLAYSURF, RED, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))

    elif shape == EMPTY:
        if number == 1:
            message_display('1', left + half, top + half)
        elif number == 2:
            message_display('2', left + half, top + half)
        elif number == 3:
            message_display('3', left + half, top + half)
        elif number == 4:
            message_display('4', left + half, top + half)
        elif number == 5:
            message_display('5', left + half, top + half)
        elif number == 6:
            message_display('6', left + half, top + half)
        elif number == 7:
            message_display('7', left + half, top + half)
        elif number == 8:
            message_display('8', left + half, top + half)
       


def getShapeColorNumber(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    # number of mines is stored in board[x][y][2]
    return board[boxx][boxy][0], board[boxx][boxy][1], board[boxx][boxy][2]

def getFlag(board, boxx, boxy):
    return board[boxx][boxy][3]

def setFlag(board, boxx, boxy, flag):
    board[boxx][boxy][3] = flag

def reverseFlag(board, boxx, boxy):
    board[boxx][boxy][3] = not board[boxx][boxy][3]

def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color, number = getShapeColorNumber(board, box[0], box[1])
        drawIcon(shape, color, number, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage, CHECK TO SEE IF YOU CAN CHANGE BOXCOLOR
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
                if getFlag(board, boxx, boxy):
                    drawHighlightBox(boxx, boxy) 
            else:
                # Draw the (revealed) icon.
                shape, color, number = getShapeColorNumber(board, boxx, boxy)
                drawIcon(shape, color, number, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True

def message_display(text, left, top):
    largeText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (left,top)
    DISPLAYSURF.blit(TextSurf, TextRect)
    #pygame.display.update()

def text_objects(text, font):
    textSurface = font.render(text, True, CYAN)
    return textSurface, textSurface.get_rect()
    
if __name__ == '__main__':
    main()


    
    
