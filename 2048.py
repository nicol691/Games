
import pygame, sys, random, copy
from pygame.locals import *
from random import randint


# Create the constants (go ahead and experiment with different values)
BOARDWIDTH = 4           # number of columns in the board
BOARDHEIGHT = BOARDWIDTH # number of rows in the board
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
DARKORANGE =    (255, 140, 0)
DEEPPINK = 	(255, 20, 147)
RED =           (139, 0, 0)
BGCOLOR = DARKTURQUOISE
TILECOLOR = DEEPPINK
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

score = 0
winTrue = False
gameOver = False
fullCount = 0
added = 0

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT
    global score
    global winTrue
    global gameOver
    global fullCount
    global added
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('2048')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    boardList = []
    scoreList = []

    mainBoard, solutionSeq = generateNewPuzzle(40)

    while True: # main game loop
        slideTo = None # the direction, if any, a tile should slide
        msg = 'Press arrow keys to slide. Score = '+str(score)
        if winTrue == True:
            msg = 'YOU GOT THE 2048 TILE! Score = '+str(score)
        # contains the message to show in the upper left corner.
        elif gameOver == True:
            msg = 'Game Over. Score = '+str(score)

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a): #and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d): # and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w):# and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s): # and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN
                elif event.key == K_z:
                    if len(boardList) > 0:
                        mainBoard = boardList.pop()
                        score = scoreList.pop()

        if slideTo:
            newBoard = copy.deepcopy(mainBoard)
            boardList.append(copy.deepcopy(mainBoard))
            scoreList.append(score)
            pointlist = makeMove(newBoard, slideTo, True)
            slideAnimation(mainBoard, slideTo, 'Press arrow keys to slide. Score = '+str(score), 35, pointlist) # show slide on screen
            mainBoard = copy.deepcopy(newBoard)
            #Check if the game is lost
            if getBlankCount(mainBoard) == 0:
                testBoard = copy.deepcopy(mainBoard)
                testLEFT = makeMove(testBoard, LEFT, False)
                testBoard = copy.deepcopy(mainBoard)
                testRIGHT = makeMove(testBoard, RIGHT, False)
                testBoard = copy.deepcopy(mainBoard)
                testUP = makeMove(testBoard, UP, False)
                testBoard = copy.deepcopy(mainBoard)
                testDOWN = makeMove(testBoard, DOWN, False)
                if testLEFT==[] and testRIGHT==[] and testUP==[] and testDOWN==[]:
                    gameOver = True
                
            
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        
        
def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def getStartingBoard():
    # Return a board data structure.
    no1 = randint(1, int(BOARDWIDTH*BOARDHEIGHT/2))
    no2 = randint(int(BOARDWIDTH*BOARDHEIGHT/2)+1, BOARDWIDTH*BOARDHEIGHT)
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            if counter == no1 or counter == no2:
                column.append(2)
            else:
                column.append(BLANK)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1
        
    return board

def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)

def getBlankCount(board):
    # Return the count of blanks
    global gameOver
    gameOver = False
    count = 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                count = count + 1
            #elif board[x][y] != BLANK:
                   # gameOver = True
                    #print("FULLCOUNT", fullCount)
    return count

def setBlankPos(board, blankPos, number):
    # Put the number in blank position
    #print("setBlankPos")
    count = 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                count = count + 1
                #print(count, blankPos)
                if count == blankPos:
                    board[x][y] = number
                    #print("NEW: NEW x,y = ", x, y)
                    return

def blankAndAppend(x, y, fillPosition, pointlist, board, move):
    if move == LEFT or move == RIGHT:
        t=y
        y=x
        x=t
    board[x][y] = BLANK
    if move==UP or move==DOWN:
        point = (x, y, abs(y-fillPosition))
    else:
        point = (x, y, abs(x-fillPosition))
    pointlist.append(point)
    #print("LIST: ", point)

def getBoardXY(board, x, y, move):
    if move == LEFT or move == RIGHT:
        t=y
        y=x
        x=t
    return board[x][y]
    
def setBoardXY(board, x, y, move, value):
    if move == LEFT or move == RIGHT:
        t=y
        y=x
        x=t
    board[x][y] = value
        
def makeMove(board, move, updateScore):
    # This function does not check if the move is valid.
    # print("makeMove")
    pointlist = []
    global score
    global winTrue
    global fullCount
    global added
    fullCount = 0
    
    #For each column
    aMoveWasDone = False
    winTrue = False
    #print("**************************************")
    for x in range(BOARDWIDTH):
        #add numbers
        if move == UP or move == LEFT:
            fillPosition = 0
        else:
            fillPosition = BOARDHEIGHT - 1
        foundNumber = BLANK
        if move == UP or move == LEFT:
            theRange = range(0, BOARDHEIGHT, 1)
        else:
            theRange = range(BOARDHEIGHT-1, -1, -1)
        for y in theRange:
            if getBoardXY(board, x, y, move) != BLANK:
                if foundNumber == BLANK:
                    foundNumber = getBoardXY(board, x, y, move)
                    foundPosition = y
                    #print("found: ", foundNumber, " at ", foundPosition)
                else:                       
                    if getBoardXY(board, x, y, move) == foundNumber:
                        added = getBoardXY(board, x, y, move) + foundNumber
                        blankAndAppend(x, y, fillPosition, pointlist, board, move)
                        #added code
                        #print('NUMBER: ', added)
                        if updateScore:
                            if added == 2048:
                                winTrue = True
                        #print("ADD1: Removed x,y = ", x, y)
                        if move == UP or move == LEFT:
                            blankAndAppend(x, foundPosition, fillPosition, pointlist, board, move)
                            #print("ADD2: Removed x,y = ", x, foundPosition)
                        else:
                            blankAndAppend(x, foundPosition, fillPosition, pointlist, board, move)
                            #print("ADD3: Removed x,y = ", x, foundPosition)
                            #added code
                            #fullCount = fullCount + 1
                        setBoardXY(board, x, fillPosition, move, added)
                        #print("ADD4: Added x,y = ", x, fillPosition)
                        if updateScore:
                            score = score + added
                        foundNumber = BLANK
                        aMoveWasDone = True
                        if move == UP or move == LEFT:    
                            fillPosition = fillPosition + 1
                        else:
                            fillPosition = fillPosition - 1
                    else:
                        foundNumber = getBoardXY(board, x, y, move)
                        foundPosition = y
                        if getBoardXY(board, x, fillPosition, move) != BLANK:
                            if move == UP or move == LEFT:    
                                fillPosition = fillPosition + 1
                            else:
                                fillPosition = fillPosition - 1
        #shift numbers
        if move == UP or move == LEFT:
            count = BOARDHEIGHT - fillPosition - 1
        else:
            count = fillPosition
        while count > 0:
            if getBoardXY(board, x, fillPosition, move) != BLANK:
                if move == UP or move == LEFT:
                    fillPosition = fillPosition + 1
                else:
                    fillPosition = fillPosition - 1
                count = count - 1
            else:
                if move == UP or move == LEFT:
                    lastPosition = BOARDHEIGHT
                else:
                    lastPosition = 0
                if fillPosition == lastPosition:
                    count = 0
                else:
                    if move == UP or move == LEFT:
                        theRange = range(fillPosition+1, BOARDHEIGHT, 1)
                    else:
                        theRange = range(fillPosition-1, -1, -1)
                    for y in theRange:
                        if getBoardXY(board, x, y, move) == BLANK:
                            count = count - 1
                        else:
                            number = getBoardXY(board, x, y, move)
                            setBoardXY(board, x, y, move, BLANK)
                            blankAndAppend(x, y, fillPosition, pointlist, board, move)
                            #print("SHIFT: Removed x,y = ", x, y)
                            setBoardXY(board, x, fillPosition, move, number)
                            #print("SHIFT: Number x,y = ", x, fillPosition)
                            count = count - 1
                            if move == UP or move == LEFT:
                                fillPosition = fillPosition + 1
                            else:
                                fillPosition = fillPosition - 1 
                            aMoveWasDone = True
        
             
    #Add new tile
    if aMoveWasDone and score < 132:
        blankCount = getBlankCount(board)
        if blankCount>0:
            blankPos = randint(1, blankCount)
            setBlankPos(board, blankPos, 2)
    else:
        blankCount = getBlankCount(board)
        if blankCount>0:
            blankPos = randint(1, blankCount)
            no4 = randint(1,2)
            number = no4 * 2
            setBlankPos(board, blankPos, number)

    return pointlist

def isValidMove(board, move):
    return True

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    global added
    global TILECOLOR
    if number != BLANK:
        left, top = getLeftTopOfTile(tilex, tiley)
        pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
        pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
        if added == 64:
            TILECOLOR = GREEN
        if added == 128:
            TILECOLOR = BRIGHTBLUE
        if added == 512:
            TILECOLOR = DARKORANGE
        if added == 1024:
            TILECOLOR = BLACK
        if added == 2048:
            TILECOLOR = RED
        textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
        textRect = textSurf.get_rect()
        textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
        DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)


def slideAnimation(board, direction, message, animationSpeed, pointlist):
    # Note: This function does not check if the move is valid.
    #blankx, blanky = getBlankPosition(board)
    #endx, endy = (1, 1)
    
    # find max tile movement
    maxtile = 0
    for start in pointlist:
        if start[2] > maxtile:
            maxtile = start[2]
    
    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    anotherSurf = baseSurf.copy()
    
    # draw a blank space over the moving tile on the baseSurf Surface.
    for start in pointlist:
        moveLeft, moveTop = getLeftTopOfTile(start[0], start[1])
        pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))
    
    for i in range(0, maxtile*TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        for start in pointlist:
            if i<start[2]*TILESIZE:
                if direction == UP:
                    drawTile(start[0], start[1], board[start[0]][start[1]], 0, -i)
                if direction == DOWN:
                    drawTile(start[0], start[1], board[start[0]][start[1]], 0, i)
                if direction == LEFT:
                    drawTile(start[0], start[1], board[start[0]][start[1]], -i, 0)
                if direction == RIGHT:
                    drawTile(start[0], start[1], board[start[0]][start[1]], i, 0)
            else:
                if direction == UP:
                    drawTile(start[0], start[1], board[start[0]][start[1]], 0, -start[2]*TILESIZE)
                if direction == DOWN:
                    drawTile(start[0], start[1], board[start[0]][start[1]], 0, start[2]*TILESIZE)
                if direction == LEFT:
                    drawTile(start[0], start[1], board[start[0]][start[1]], -start[2]*TILESIZE, 0)
                if direction == RIGHT:
                    drawTile(start[0], start[1], board[start[0]][start[1]], start[2]*TILESIZE, 0)



        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    return (board, sequence)

if __name__ == '__main__':
    main()
