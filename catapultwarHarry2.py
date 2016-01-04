import random, pygame, sys
from pygame.locals import *
 
#from SixNet.Connection import ConnectionListener, connection
from time import sleep

"""class CatapultWar(self, ConnectionListener):
    self.connect()
    connection.Pump()
    Pump()"""

FPS = 30
WINDOWWIDTH = 1600
WINDOWHEIGHT = 900
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 15
BOARDHEIGHT = 15
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

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
HIGHLIGHTCOLOR = BLUE

FIREBOMB = 'firebomb'
CROSSBOMB = 'crossbomb'
NAPALM = 'napalm'
GUILLOTINE = 'guillotine'
ROCKET = 'rocket'
LUCKY = 'lucky'
SUPERLUCKY = 'superlucky'
BENTENG = 'benteng'
NONE = 'none'

POWERUPS = ((FIREBOMB, 5), (CROSSBOMB, 5), (NAPALM, 3), (GUILLOTINE, 2), (ROCKET, 2), (LUCKY, 5), (SUPERLUCKY, 3))

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 #membaca posisi x cursor mouse pada surface
    mousey = 0 #membaca posisi y cursor mouse pada surface
    pygame.display.set_caption('Catapult War')
    
    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1, 0.0)
    
    musicCastle = inisialisasiMusicEffect()

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    player1 = 5
    takeshi1 = 5
    setBenteng = False
    turn = 0

    DISPLAYSURF.fill(BGCOLOR)
    drawBoard(mainBoard, revealedBoxes)
    pygame.display.update()

    while True:
        mouseClicked = False
        playerPU = ''
        turnLeft = 3

        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)
        drawBentengLawan(5)
        drawBentengHancur(0)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        if takeshi1 != 0:
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            if boxx != None and boxy != None:
                if not revealedBoxes[boxx][boxy]:
                    drawHighlightBox(boxx, boxy)
                if not revealedBoxes[boxx][boxy] and mouseClicked:
                    takeshi1 -= 1
                    mainBoard[boxx][boxy] = BENTENG
                    revealedBoxes[boxx][boxy] = True
                    drawIcon(BENTENG, boxx, boxy)
                    musicCastle.play()
        else:
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            if boxx != None and boxy != None:
                if not revealedBoxes[boxx][boxy]:
                    drawHighlightBox(boxx, boxy)
                if not revealedBoxes[boxx][boxy] and mouseClicked:
                    fireCatapult(mainBoard,revealedBoxes,boxx,boxy,FIREBOMB)
                    """
                    if mainBoard[boxx][boxy] == NONE:
                        a = 5
                    elif mainBoard[boxx][boxy] == BENTENG:
                        player1 -= 1
                    else:
                        playerpu = mainBoard[boxx][boxy]
                    """

            """
            if player1 == 0:
                gameWonAnimation(mainBoard)
                pygame.time.wait(2000)

                        # Reset the board
                mainBoard = getRandomizedBoard()
                revealedBoxes = generateRevealedBoxesData(False)

                # Show the fully unrevealed board for a second.
                drawBoard(mainBoard, revealedBoxes)
                pygame.display.update()
                pygame.time.wait(1000)

                # Replay the start game animation.
                startGameAnimation(mainBoard)
            """

        turn += 1
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawBentengHancur(score):
    scoreSurf = BASICFONT.render('Benteng Hancur: %d' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 400, 75)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    
def drawBentengLawan(score):
    scoreSurf = BASICFONT.render('Benteng Lawan: %d' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 400, 105)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def inisialisasiMusicEffect():
    musicCastle = pygame.mixer.Sound('buildCastle.ogg')
    #castleDestroy = pygame.mixer.Sound('')
    #catapultFire = pygame.mixer.Sound('')

    return musicCastle
def generateRevealedBoxesData(val):
    # Menutup semua box di board
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    # Meletakkan POWERUPS secara random di board
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(NONE)
        board.append(column)

    powerups = []
    for items in POWERUPS:
        for i in range(items[1]):
            powerups.append(items[0])

    random.shuffle(powerups)

    while(len(powerups) != 0):
        xcoord = random.randint(0, BOARDWIDTH - 1)
        ycoord = random.randint(0, BOARDHEIGHT - 1)
        if board[xcoord][ycoord] == NONE:
            board[xcoord][ycoord] = powerups[0]
            del powerups[0]
        else:
            continue

    return board

def fireCatapult(board, revealedBoxes, boxx, boxy, powerup):
    boxes = []
    boxes.append((boxx, boxy))
    revealedBoxes[boxx][boxy] = True

    if(powerup == FIREBOMB):
        boxes = []
        boxes.append((boxx, boxy))
        revealedBoxes[boxx][boxy] = True

        if(boxx - 1 >= 0 and not revealedBoxes[boxx - 1][boxy]):
            boxes.append((boxx - 1, boxy))
            revealedBoxes[boxx - 1][boxy] = True
        if(boxx + 1 < BOARDWIDTH and not revealedBoxes[boxx + 1][boxy]):
            boxes.append((boxx + 1, boxy))
            revealedBoxes[boxx + 1][boxy] = True
        if(boxy - 1 >= 0 and not revealedBoxes[boxx][boxy - 1]):
            boxes.append((boxx, boxy - 1))
            revealedBoxes[boxx][boxy - 1] = True
        if(boxy + 1 < BOARDHEIGHT and not revealedBoxes[boxx][boxy + 1]):
            boxes.append((boxx, boxy + 1))
            revealedBoxes[boxx][boxy + 1] = True

    #elif(powerup == CROSSBOMB):

    #elif(powerup == NAPALM):

    #elif(powerup == GUILLOTINE):

    #elif(powerup == ROCKET):

    #else:

    revealBoxesAnimation(board, boxes)

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


def drawIcon(shape, boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == BENTENG:
        DISPLAYSURF.blit(pygame.image.load('gambar/benteng.png'),(left,top))
    elif shape == FIREBOMB:
        DISPLAYSURF.blit(pygame.image.load('gambar/firebomb.png'),(left,top))
    elif shape == CROSSBOMB:
        DISPLAYSURF.blit(pygame.image.load('gambar/crossbomb.png'),(left,top))
    elif shape == NAPALM:
        DISPLAYSURF.blit(pygame.image.load('gambar/napalm.png'),(left,top))
    elif shape == GUILLOTINE:
        DISPLAYSURF.blit(pygame.image.load('gambar/guillotine.png'),(left,top))
    elif shape == LUCKY:
        DISPLAYSURF.blit(pygame.image.load('gambar/lucky.png'),(left,top))
    elif shape == SUPERLUCKY:
        DISPLAYSURF.blit(pygame.image.load('gambar/superlucky.png'),(left,top))


def getShape(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape = getShape(board, box[0], box[1])
        drawIcon(shape, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
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
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon.
                shape = getShape(board, boxx, boxy)
                drawIcon(shape, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


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


if __name__ == '__main__':
    main()