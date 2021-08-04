import random

import pygame

import os
os.chdir("/Users/mac/PycharmProjects/Untitled")
pygame.init()

# Image Initializations+
TetrisIcon = pygame.image.load("videogame.png")
Images = [["tetrisL.png"], ["tetrisZ.png"], ["tetrisZmirror.png"], ["tetrisLine.png"], ["tetrisLmirror.png"],
          ["tetrisSquare.png"], ["tetrisT.png"]]

Hold_Images = [["tetrisLimg.png", "tetrisLimg1.png", "tetrisLimg2.png", "tetrisLimg3.png"],
               ["tetrisZimg.png", "tetrisZimg1.png"], ["tetrisZmirrorimg.png", "tetrisZmirrorimg1.png"]
    , ["tetrisLineimg.png", "tetrisLineimg1.png"],
               ["tetrisLmirrorimg.png", "tetrisLmirrorimg1.png", "tetrisLmirrorimg2.png", "tetrisLmirrorimg3.png"],
               ["tetrisSquareimg.png"],
               ["tetrisTimg.png", "tetrisTimg1.png", "tetrisTimg2.png", "tetrisTimg3.png"]]

# Display Initialization
Disp = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Tetris")
pygame.display.set_icon(TetrisIcon)
pygame.font.init()
# Colour Initializations
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (0, 128, 128)
MY_MIX = (0, 76, 160)

# Global Variables for keeping track of everything
nextlist = []
holdelement = [-1, -1, -1]
Myspritegroup = pygame.sprite.Group()
mysprites = []
Font = pygame.font.Font(None, 64)
Mainrect = pygame.draw.rect(Disp, MY_MIX, (400 - 160, 32, 320, 704))
Score = 0

for i in range(5):
    nextlist.append(random.randint(0, 6))


def create_blocks():
    for i in range(23):
        for c in range(11):
            pygame.draw.rect(Disp, YELLOW, (400 - 160, 32, 32 * c, 32 * i), 1)


def display_hold():
    global holdelement
    text = Font.render("Hold", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.x = 60
    text_rect.y = 16
    Disp.blit(text, text_rect)
    Hold_rect = pygame.draw.rect(Disp, MY_MIX, (400 - 160 - 232, 80, 200, 200), 5)
    text1 = Font.render("Score", True, (255, 255, 255))
    text_rect1 = text1.get_rect()
    text_rect1.x = 48
    text_rect1.y = Hold_rect.bottom + 32
    Disp.blit(text1, text_rect1)
    text2 = Font.render(str(Score), True, (255, 255, 255))
    text_rect2 = text2.get_rect()
    text_rect2.x = 32 + 48
    text_rect2.y = text_rect1.bottom
    Disp.blit(text2, text_rect2)
    if holdelement[0] != -1:
        image = pygame.image.load(Hold_Images[holdelement[0]][holdelement[1]]).convert_alpha()
        image_rect = image.get_rect()
        image_rect.center = Hold_rect.center
        Disp.blit(image, image_rect)


def next_display():
    text = Font.render("Next", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.x = 50 + 400 + 160 + 32
    text_rect.y = 16
    Disp.blit(text, text_rect)
    global nextlist
    next_rect1 = pygame.draw.rect(Disp, MY_MIX, (400 + 160 + 32, 64, 200, 200), 5)
    next_rect2 = pygame.draw.rect(Disp, MY_MIX, (400 + 160 + 32, 64 + 200, 200, 200), 5)
    next_rect3 = pygame.draw.rect(Disp, MY_MIX, (400 + 160 + 32, 64 + 400, 200, 200), 5)
    image1 = pygame.image.load(Hold_Images[nextlist[1]][0]).convert_alpha()
    image_rect1 = image1.get_rect()
    image_rect1.center = next_rect1.center
    Disp.blit(image1, image_rect1)
    image2 = pygame.image.load(Hold_Images[nextlist[2]][0]).convert_alpha()
    image_rect2 = image2.get_rect()
    image_rect2.center = next_rect2.center
    Disp.blit(image2, image_rect2)
    image3 = pygame.image.load(Hold_Images[nextlist[3]][0]).convert_alpha()
    image_rect3 = image3.get_rect()
    image_rect3.center = next_rect3.center
    Disp.blit(image3, image_rect3)


class obj(pygame.sprite.Sprite):
    #  This is a single block of size 32*32 px
    # Variables For obj
    # playerX = 0  # keeps track of x coordinates
    # playerY = 0  # keeps track of y coordinates
    image = None
    rect = None

    def __init__(self, shapevar):
        pygame.sprite.Sprite.__init__(self)  # initializing it as a sprite
        self.image = pygame.image.load(Images[shapevar][0]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.top = Mainrect.top  # Fitting it inside described play area
        self.rect.left = Mainrect.left
        Myspritegroup.add(self)
        mysprites.append(self)


class Container:
    # Class Variables
    mysprite = []  # This is a list for keeping track of my sprites obj
    shapevar = 0  # tracks shape
    rotvar = 0  # tracks current rotation
    maxrot = 0  # tracks max rotation
    changeY = 0
    Lock = False

    def __init__(self, isHold=False):
        self.Lock = False
        self.mysprite.clear()
        if not isHold:
            self.shapevar = nextlist[0]
        else:
            self.shapevar = holdelement[0]
            self.rotvar = holdelement[1]
            self.maxrot = holdelement[2]
        for i in range(4):
            self.mysprite.append(obj(self.shapevar))
        self.create(isHold)

    def rot(self, Clock=True):
        if self.shapevar != 5:
            if Clock:
                self.rotvar += 1
                if self.rotvar > self.maxrot:
                    self.rotvar = 0
                self.create(True, True)
                if self.rot_collide():
                    self.rotvar -= 1
                    if self.rotvar < 0:
                        self.rotvar = self.maxrot
                    self.create(True, True)
            else:
                self.rotvar -= 1
                if self.rotvar < 0:
                    self.rotvar = self.maxrot
                self.create(True, True)
                if self.rot_collide():
                    self.rotvar += 1
                    if self.rotvar > self.maxrot:
                        self.rotvar = 0
                    self.create(True, True)

    def movex(self, Right=True):
        Collide = False
        changeX = 0
        if Right:
            changeX = +32
        else:
            changeX = -32
        if Right:
            for i in self.mysprite:
                i.rect.x += changeX
                Myspritegroup.remove(i)
                if i.rect.right > Mainrect.right:
                    Collide = True
            if not Collide:
                for sprites in Myspritegroup:
                    for i in self.mysprite:
                        if pygame.sprite.collide_rect(i, sprites):
                            Collide = True
                        if Collide:
                            break
                    if Collide:
                        break
            if Collide:
                for i in self.mysprite:
                    i.rect.x -= changeX
            for i in self.mysprite:
                Myspritegroup.add(i)
        else:
            for i in self.mysprite:
                i.rect.x += changeX
                Myspritegroup.remove(i)
                if i.rect.left < Mainrect.left:
                    Collide = True
            if not Collide:
                for sprites in Myspritegroup:
                    for i in self.mysprite:
                        if pygame.sprite.collide_rect(i, sprites):
                            Collide = True
                        if Collide:
                            break
                    if Collide:
                        break
            if Collide:
                for i in self.mysprite:
                    i.rect.x -= changeX
            for i in self.mysprite:
                Myspritegroup.add(i)

    def movey(self, Speed=False, MOVE=False):
        Collide = False
        self.changeY = 1
        if Speed and not self.Lock:
            self.changeY = 2
        else:
            self.changeY = 1
        if MOVE:
            self.changeY = 32
        for i in self.mysprite:
            i.rect.y += self.changeY
            Myspritegroup.remove(i)
            if i.rect.bottom > Mainrect.bottom:
                Collide = True
        if not Collide:
            for sprites in Myspritegroup:
                for i in self.mysprite:
                    if pygame.sprite.collide_rect(i, sprites):
                        Collide = True
                    if Collide:
                        break
                if Collide:
                    break
        if Collide:
            for i in self.mysprite:
                i.rect.y -= self.changeY
        for i in self.mysprite:
            Myspritegroup.add(i)

    def rot_collide(self):
        Collide = False
        for i in self.mysprite:
            Myspritegroup.remove(i)
            if i.rect.bottom > Mainrect.bottom:
                Collide = True
            if i.rect.left < Mainrect.left:
                Collide = True
            if i.rect.right > Mainrect.right:
                Collide = True
        if not Collide:
            for sprites in Myspritegroup:
                for i in self.mysprite:
                    if pygame.sprite.collide_rect(i, sprites):
                        Collide = True
                    if Collide:
                        break
                if Collide:
                    break
        for i in self.mysprite:
            Myspritegroup.add(i)
        return Collide

    def collide(self):  # function for detecting collision for locking the object
        Collide = False
        for i in self.mysprite:
            Myspritegroup.remove(i)
            i.rect.y += self.changeY
            if i.rect.bottom > Mainrect.bottom:
                Collide = True
        if not Collide:
            for sprites in Myspritegroup:
                for i in self.mysprite:
                    if pygame.sprite.collide_rect(i, sprites):
                        Collide = True
                    if Collide:
                        break
                if Collide:
                    break
        for i in self.mysprite:
            i.rect.y -= self.changeY
        for i in self.mysprite:
            Myspritegroup.add(i)
        return Collide

    def create(self, isHold=False, rot=False):
        # Now Program for creation of each Tetris shape with each rotation

        if self.shapevar == 0:
            if not isHold:
                self.rotvar = random.randint(0, 3)
                self.maxrot = 3
            if self.rotvar == 0:
                self.mysprite[1].rect.left = self.mysprite[0].rect.left
                self.mysprite[1].rect.top = self.mysprite[0].rect.bottom
                self.mysprite[2].rect.left = self.mysprite[1].rect.left
                self.mysprite[2].rect.top = self.mysprite[1].rect.bottom
                self.mysprite[3].rect.left = self.mysprite[2].rect.right
                self.mysprite[3].rect.top = self.mysprite[2].rect.top
            if self.rotvar == 1:
                self.mysprite[1].rect.top = self.mysprite[0].rect.top
                self.mysprite[1].rect.right = self.mysprite[0].rect.left
                self.mysprite[2].rect.top = self.mysprite[1].rect.top
                self.mysprite[2].rect.right = self.mysprite[1].rect.left
                self.mysprite[3].rect.left = self.mysprite[2].rect.left
                self.mysprite[3].rect.top = self.mysprite[2].rect.bottom
            if self.rotvar == 2:
                self.mysprite[1].rect.bottom = self.mysprite[0].rect.top
                self.mysprite[1].rect.left = self.mysprite[0].rect.left
                self.mysprite[2].rect.bottom = self.mysprite[1].rect.top
                self.mysprite[2].rect.left = self.mysprite[1].rect.left
                self.mysprite[3].rect.right = self.mysprite[2].rect.left
                self.mysprite[3].rect.top = self.mysprite[2].rect.top
            if self.rotvar == 3:
                self.mysprite[1].rect.top = self.mysprite[0].rect.top
                self.mysprite[1].rect.left = self.mysprite[0].rect.right
                self.mysprite[2].rect.top = self.mysprite[1].rect.top
                self.mysprite[2].rect.left = self.mysprite[1].rect.right
                self.mysprite[3].rect.left = self.mysprite[2].rect.left
                self.mysprite[3].rect.bottom = self.mysprite[2].rect.top

        if self.shapevar == 1:
            if not isHold:
                self.rotvar = random.randint(0, 1)
                self.maxrot = 1
            if self.rotvar == 0:
                self.mysprite[1].rect.left = self.mysprite[0].rect.right
                self.mysprite[1].rect.top = self.mysprite[0].rect.top
                self.mysprite[2].rect.left = self.mysprite[1].rect.left
                self.mysprite[2].rect.top = self.mysprite[1].rect.bottom
                self.mysprite[3].rect.left = self.mysprite[2].rect.right
                self.mysprite[3].rect.top = self.mysprite[2].rect.top
            if self.rotvar == 1:
                self.mysprite[1].rect.top = self.mysprite[0].rect.bottom
                self.mysprite[1].rect.left = self.mysprite[0].rect.left
                self.mysprite[2].rect.top = self.mysprite[1].rect.top
                self.mysprite[2].rect.right = self.mysprite[1].rect.left
                self.mysprite[3].rect.left = self.mysprite[2].rect.left
                self.mysprite[3].rect.top = self.mysprite[2].rect.bottom

        if self.shapevar == 2:
            if not isHold:
                self.rotvar = random.randint(0, 1)
                self.maxrot = 1
            if self.rotvar == 0:
                self.mysprite[1].rect.right = self.mysprite[0].rect.left
                self.mysprite[1].rect.top = self.mysprite[0].rect.top
                self.mysprite[2].rect.left = self.mysprite[1].rect.left
                self.mysprite[2].rect.top = self.mysprite[1].rect.bottom
                self.mysprite[3].rect.right = self.mysprite[2].rect.left
                self.mysprite[3].rect.top = self.mysprite[2].rect.top
            if self.rotvar == 1:
                self.mysprite[1].rect.top = self.mysprite[0].rect.bottom
                self.mysprite[1].rect.left = self.mysprite[0].rect.left
                self.mysprite[2].rect.top = self.mysprite[1].rect.top
                self.mysprite[2].rect.left = self.mysprite[1].rect.right
                self.mysprite[3].rect.left = self.mysprite[2].rect.left
                self.mysprite[3].rect.top = self.mysprite[2].rect.bottom
        if self.shapevar == 3:
            if not isHold:
                self.rotvar = random.randint(0, 1)
                self.maxrot = 1
            if self.rotvar == 0:
                self.mysprite[1].rect.left = self.mysprite[0].rect.right
                self.mysprite[1].rect.top = self.mysprite[0].rect.top
                self.mysprite[2].rect.left = self.mysprite[1].rect.right
                self.mysprite[2].rect.top = self.mysprite[1].rect.top
                self.mysprite[3].rect.left = self.mysprite[2].rect.right
                self.mysprite[3].rect.top = self.mysprite[2].rect.top
            if self.rotvar == 1:
                self.mysprite[1].rect.top = self.mysprite[0].rect.bottom
                self.mysprite[1].rect.left = self.mysprite[0].rect.left
                self.mysprite[2].rect.top = self.mysprite[1].rect.bottom
                self.mysprite[2].rect.left = self.mysprite[1].rect.left
                self.mysprite[3].rect.left = self.mysprite[2].rect.left
                self.mysprite[3].rect.top = self.mysprite[2].rect.bottom
        if self.shapevar == 4:
            if not isHold:
                self.rotvar = random.randint(0, 3)
                self.maxrot = 3
            if self.rotvar == 0:
                self.mysprite[1].rect.left = self.mysprite[0].rect.left
                self.mysprite[1].rect.top = self.mysprite[0].rect.bottom
                self.mysprite[2].rect.left = self.mysprite[1].rect.left
                self.mysprite[2].rect.top = self.mysprite[1].rect.bottom
                self.mysprite[3].rect.right = self.mysprite[2].rect.left
                self.mysprite[3].rect.top = self.mysprite[2].rect.top
            if self.rotvar == 1:
                self.mysprite[1].rect.top = self.mysprite[0].rect.top
                self.mysprite[1].rect.right = self.mysprite[0].rect.left
                self.mysprite[2].rect.top = self.mysprite[1].rect.top
                self.mysprite[2].rect.right = self.mysprite[1].rect.left
                self.mysprite[3].rect.left = self.mysprite[2].rect.left
                self.mysprite[3].rect.bottom = self.mysprite[2].rect.top
            if self.rotvar == 2:
                self.mysprite[1].rect.bottom = self.mysprite[0].rect.top
                self.mysprite[1].rect.left = self.mysprite[0].rect.left
                self.mysprite[2].rect.bottom = self.mysprite[1].rect.top
                self.mysprite[2].rect.left = self.mysprite[1].rect.left
                self.mysprite[3].rect.left = self.mysprite[2].rect.right
                self.mysprite[3].rect.top = self.mysprite[2].rect.top
            if self.rotvar == 3:
                self.mysprite[1].rect.top = self.mysprite[0].rect.top
                self.mysprite[1].rect.left = self.mysprite[0].rect.right
                self.mysprite[2].rect.top = self.mysprite[1].rect.top
                self.mysprite[2].rect.left = self.mysprite[1].rect.right
                self.mysprite[3].rect.left = self.mysprite[2].rect.left
                self.mysprite[3].rect.top = self.mysprite[2].rect.bottom

        if self.shapevar == 5:
            if not isHold:
                self.rotvar = 0
                self.maxrot = 0
            if self.rotvar == 0:
                self.mysprite[1].rect.left = self.mysprite[0].rect.right
                self.mysprite[1].rect.top = self.mysprite[0].rect.top
                self.mysprite[2].rect.left = self.mysprite[1].rect.left
                self.mysprite[2].rect.top = self.mysprite[1].rect.bottom
                self.mysprite[3].rect.right = self.mysprite[2].rect.left
                self.mysprite[3].rect.top = self.mysprite[2].rect.top
        if self.shapevar == 6:
            if not isHold:
                self.rotvar = random.randint(0, 3)
                self.maxrot = 3
            if self.rotvar == 0:
                self.mysprite[1].rect.left = self.mysprite[0].rect.right
                self.mysprite[1].rect.top = self.mysprite[0].rect.top
                self.mysprite[2].rect.left = self.mysprite[1].rect.right
                self.mysprite[2].rect.top = self.mysprite[1].rect.top
                self.mysprite[3].rect.right = self.mysprite[2].rect.left
                self.mysprite[3].rect.bottom = self.mysprite[2].rect.top
            if self.rotvar == 1:
                self.mysprite[1].rect.top = self.mysprite[0].rect.bottom
                self.mysprite[1].rect.left = self.mysprite[0].rect.left
                self.mysprite[2].rect.top = self.mysprite[1].rect.bottom
                self.mysprite[2].rect.left = self.mysprite[1].rect.left
                self.mysprite[3].rect.left = self.mysprite[2].rect.right
                self.mysprite[3].rect.bottom = self.mysprite[2].rect.top
            if self.rotvar == 2:
                self.mysprite[1].rect.top = self.mysprite[0].rect.top
                self.mysprite[1].rect.right = self.mysprite[0].rect.left
                self.mysprite[2].rect.top = self.mysprite[1].rect.top
                self.mysprite[2].rect.right = self.mysprite[1].rect.left
                self.mysprite[3].rect.left = self.mysprite[2].rect.right
                self.mysprite[3].rect.top = self.mysprite[2].rect.bottom
            if self.rotvar == 3:
                self.mysprite[1].rect.bottom = self.mysprite[0].rect.top
                self.mysprite[1].rect.left = self.mysprite[0].rect.left
                self.mysprite[2].rect.bottom = self.mysprite[1].rect.top
                self.mysprite[2].rect.left = self.mysprite[1].rect.left
                self.mysprite[3].rect.right = self.mysprite[2].rect.left
                self.mysprite[3].rect.top = self.mysprite[2].rect.bottom
        if not rot:
            for i in self.mysprite:
                if i.rect.top < Mainrect.top:
                    for z in self.mysprite:
                        z.rect.y += 32
                if i.rect.left < Mainrect.left:
                    for z in self.mysprite:
                        z.rect.x += 32
