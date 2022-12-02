import pygame
import random
from pygame import mixer

class meteorit:
    def __init__(self, bredd, höjd, bildKälla, slumpX):
        self.bredd = bredd
        self.höjd = höjd
        self.bildkälla = bildKälla
        self.meteorit = pygame.transform.scale(pygame.image.load(bildKälla), (self.bredd, self.höjd))
        self.meteoritRektangel = pygame.Rect(slumpX, -self.höjd, self.bredd-self.bredd/10, self.höjd-self.höjd/10)
        self.fallHastighet = random.randrange(4, 6)

    def fallLinje(self):
        self.meteoritRektangel.y += self.fallHastighet
    def getPosY(self):
        return self.meteoritRektangel.y
    def getPosX(self):
        return self.meteoritRektangel.x

class explosion:
    def __init__(self, ljudKälla, volym, meteorit, fallX, fallY):
        self.explosionsLjud = mixer.Sound(ljudKälla)
        self.explosionsLjud.set_volume(volym)
        self.fallX = fallX
        self.fallY = fallY
        self.explosion = pygame.transform.scale(pygame.image.load(meteorit.bildkälla), (meteorit.bredd/4, meteorit.höjd/4))
        self.explosionRektangel = pygame.Rect(meteorit.getPosX() + meteorit.bredd/2, meteorit.getPosY() + meteorit.höjd/2,
                                              meteorit.bredd/5, meteorit.höjd/5)

    def fallLinje(self):
        self.explosionRektangel.y += self.fallY
        self.explosionRektangel.x += self.fallX
    def getPosX(self):
        return self.explosionRektangel.x
    def getPosY(self):
        return self.explosionRektangel.y

class skott:
    def __init__(self, bredd, höjd, bildKälla, ljudKälla, volym, skepp):
        self.bredd = bredd
        self.höjd = höjd
        self.skjutLjud = mixer.Sound(ljudKälla)
        self.skjutLjud.set_volume(volym)
        self.skepp = skepp
        self.skott = pygame.transform.scale(pygame.image.load(bildKälla), (self.bredd, self.höjd))
        self.skottRektangel = pygame.Rect(skepp.getPosX() + (skepp.skeppBredd / 2 - self.bredd / 2), skepp.getPosY() - self.höjd,
                                     self.bredd, self.höjd)

    def skottLinje(self):
        self.skottRektangel.y -= self.skepp.hastighet*3.5
    def getPosY(self):
        return self.skottRektangel.y

class rymdskepp:
    def __init__(self, fönsterBredd, fönsterHöjd):
        self.skeppBredd = 80
        self.skeppHöjd = 80
        self.fönsterBredd = fönsterBredd
        self.fönsterHöjd = fönsterHöjd
        self.startPosX = fönsterBredd/2 - self.skeppBredd/2
        self.startPosY = fönsterHöjd - self.skeppHöjd*2
        self.hastighet = 5
        self.rymdskepp = pygame.transform.scale(pygame.image.load('skeppet.png'), (self.skeppBredd, self.skeppHöjd))
        self.rektangel = pygame.Rect(self.startPosX, self.startPosY, self.skeppBredd-self.skeppBredd/3, self.skeppHöjd-self.skeppHöjd/3)

    def getPosX(self):
        return self.rektangel.x
    def getPosY(self):
        return self.rektangel.y
    def gåNedåt(self):
        if self.rektangel.y < self.fönsterHöjd-self.skeppHöjd:
            self.rektangel.y += self.hastighet
    def gåUppåt(self):
        if self.rektangel.y > 0:
            self.rektangel.y -= self.hastighet
    def gåÅtHöger(self):
        if self.rektangel.x < self.fönsterBredd-self.skeppBredd:
            self.rektangel.x += self.hastighet
    def gåÅtVänster(self):
        if self.rektangel.x > 0:
            self.rektangel.x -= self.hastighet