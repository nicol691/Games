
# WhackAMole.py
# Whack-a-mole game using pygame


import pygame, random
from pygame.locals import *
from pygame.font import *



# some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
DARKGRAY = (150,150,150)

RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
DARKGREEN = ( 0, 155, 0)
BLUE  = ( 0,   0,   255)

holeposition = [(50,0),(200,100),(450,200), (300,300), (100,300), (400,0), (0,200)]
molearray = []

MinTimeMoleHidden = 4000
MaxTimeMoleHidden = 8000
MinTimeMoleAppear = 4000
MaxTimeMoleAppear = 8000


# ---------------------------------------------------------

class Mole(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("MOLE5.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0]-30,pos[1]-50)


    # move mole to a new random location
    # after it is hit
    def flee(self):
        index = random.randint(0, len(holeposition)-1)
        pos = holeposition[index]
        self.rect.topleft = (pos[0]-30,pos[1]-50)


    def draw(self, screen):
        screen.blit(self.image, self.rect)


# ---------------------------------------------------------


class Shovel(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Untitled.png").convert_alpha()
        self.rect = self.image.get_rect()


    # did the shovel hit the mole?
    def hit(self, target):
        return self.rect.colliderect(target)


    # follows the mouse cursor
    def update(self, pt):
        self.rect.center = pt


    def draw(self, screen):
        screen.blit(self.image, self.rect)


# -----------------------------------

#------------------------------------

def centerImage(screen, im):
    x = (scrWidth - im.get_width())/2
    y = (scrHeight - im.get_height())/2
    screen.blit(im, (x,y))



# ---------- main -------------

pygame.init()
screen = pygame.display.set_mode([640,480])
screen.fill(DARKGREEN)
pygame.display.set_caption("Whack-a-mole")
scrWidth, scrHeight = screen.get_size()


# hide the mouse cursor
# pygame.mouse.set_visible(False)

font = pygame.font.Font(None, 40)

hitSnd = pygame.mixer.Sound('punch.wav')
hitSnd.set_volume(1)


# create sprites and a group
for pos in holeposition:
    mole = Mole(pos)       #Mole position
    hidden = False         #Mole hidden
    noticks = pygame.time.get_ticks() + random.randint(MinTimeMoleHidden, MaxTimeMoleHidden) #Let the mole appear randomly
    moleSta = [mole, False, noticks]
        
    molearray.append(moleSta)
shovel = Shovel()

# game vars
hits = 0
mousePos = (scrWidth/2, scrHeight/2)
isPressed = False

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(30) 

   
    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()

        if event.type == MOUSEBUTTONDOWN:
            isPressed = True

            
    # update game
    shovel.update(mousePos)

    #Get ticks passed
    tickspassed = pygame.time.get_ticks()

    # time elapsed (in secs)
    time = int(tickspassed/1000)

    if time <= 80:
      if isPressed:
        isPressed = False
        for moleSta in molearray:
          if moleSta[1]:
              if shovel.hit(moleSta[0]):
                  moleSta[1] = False
                  moleSta[2] = tickspassed + random.randint(MinTimeMoleHidden, MaxTimeMoleHidden) #Let the mole hide randomly
                  hitSnd.play()
                  hits += 1
      


      # redraw game
      screen.fill(DARKGRAY)
      Gimage = pygame.image.load("hole.png")
      for pos in holeposition:
        screen.blit(Gimage, pos)
      for moleSta in molearray:
        if moleSta[1]:
            moleSta[0].draw(screen)
      shovel.draw(screen)
      pygame.display.update()

      #Is it time for the mole to appear or hide?
      for moleSta in molearray:
        if tickspassed > moleSta[2]:
            if moleSta[1]: #Mole visable, hide it
                moleSta[1] = False
                moleSta[2] = tickspassed + random.randint(MinTimeMoleHidden, MaxTimeMoleHidden) #Let the mole hide randomly
            else:         #Mole hidden, show it
                moleSta[1] = True
                moleSta[2] = tickspassed + random.randint(MinTimeMoleAppear, MaxTimeMoleAppear) #Let the mole appear randomly
    else:
        timeIm = font.render("TIME IS UP", True, DARKGREEN)
        screen.blit(timeIm, (100,10))    
    

    
    if hits == 0:
        MinTimeMoleHidden = 4000
        MaxTimeMoleHidden = 8000
        MinTimeMoleAppear = 4000
        MaxTimeMoleAppear = 8000
    if hits == 30 :
        MinTimeMoleHidden = 3000
        MaxTimeMoleHidden = 6000
        MinTimeMoleAppear = 3000
        MaxTimeMoleAppear = 6000
    if hits == 50:
        MinTimeMoleHidden = 2000
        MaxTimeMoleHidden = 4000
        MinTimeMoleAppear = 2000
        MaxTimeMoleAppear = 4000
    if hits == 75:
        MinTimeMoleHidden = 1000
        MaxTimeMoleHidden = 2000
        MinTimeMoleAppear = 1000
        MaxTimeMoleAppear = 2000
    if hits == 100:
        MinTimeMoleHidden = 500
        MaxTimeMoleHidden = 1000
        MinTimeMoleAppear = 500
        MaxTimeMoleAppear = 1000

    if time <= 80:
      timeIm = font.render(str(time), True, DARKGREEN)
      screen.blit(timeIm, (10,10))
        
    
    
    hitIm = font.render("Hits = " + str(hits), True, DARKGREEN)
    #centerImage(screen, hitIm)
    screen.blit(hitIm, (100,400))

    pygame.display.update()


pygame.quit()


