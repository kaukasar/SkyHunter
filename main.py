import sys
import threading
import schedule
import pygame
from pygame import mixer
import random
from resurser import rymdskepp, meteorit, explosion, skott

class svårighetsgrad:
    def __init__(self):
        self.grad = 1.0
        self.ökningsTid = 10

    def öka(self):
        if self.grad > 0.19:
            self.grad -= 0.1

bg = pygame.image.load('quasar.jpg')
fönsterBredd, fönsterHöjd = 1200, 1024
fönster = pygame.display.set_mode((fönsterBredd, fönsterHöjd))
meteoritTyper = ('meteorit1.png', 'meteorit2.png', 'meteorit3.png', 'meteorit4.png', 'meteorit5.png')
pygame.display.set_caption("Sky Hunter")
FPS = 60
mixer.init()
pygame.font.init()
skepp = rymdskepp(fönsterBredd, fönsterHöjd)
skottLista = []
meteoritLista = []
explosionLista = []
sv = svårighetsgrad()
skeppetTräffat = pygame.USEREVENT + 1

def meteoritGenerator():
    typ = random.choice(meteoritTyper)
    xKoordinat = random.randrange(50, fönsterBredd-90)
    m = meteorit(random.randrange(50, 80), random.randrange(50, 80), typ, xKoordinat)
    meteoritLista.append(m)
    print(sv.grad)
    tråd = threading.Timer(sv.grad, meteoritGenerator)
    tråd.daemon = True # Detta behöver vara satt för att tråden ska dö när man anropar sys.exit()
    tråd.start()

def explosionGenerator(meteorit):
    for _ in range(3):
        xpl = explosion('explosion.mp3', 0.2 ,  meteorit, random.randrange(-10, 10), random.randrange(-10, 10))
        explosionLista.append(xpl)
    xpl.explosionsLjud.play()

meteoritGenerator()
schedule.every(sv.ökningsTid).seconds.do(sv.öka)

def gameOver(poäng):
    mixer.Sound('arcade-explosion-echo.wav').play().set_volume(0.3)
    ritaText = pygame.font.SysFont('comicsans', 80).render("Game Over!", 1, (255, 255, 255))
    ritaText2 = pygame.font.SysFont('comicsans', 60).render(f'Du fick {poäng} poäng', 1, (255, 255, 255))
    fönster.blit(ritaText, (fönsterBredd/2 - ritaText.get_width()/2, fönsterHöjd/2 - ritaText.get_height()))
    fönster.blit(ritaText2, (fönsterBredd / 2 - ritaText2.get_width() / 2, fönsterHöjd / 2))
    fönster.blit(pygame.transform.scale(pygame.image.load('exp.png'), (skepp.skeppBredd, skepp.skeppHöjd)), (skepp.getPosX(), skepp.getPosY()))
    pygame.display.update()
    pygame.time.delay(20000)
    pygame.quit()
    sys.exit()

def rita(poäng):
    fönster.blit(bg, (0, 0))
    fönster.blit(skepp.rymdskepp, (skepp.rektangel.x, skepp.rektangel.y))
    poängKollen = pygame.font.SysFont('comicsans', 40).render(f'{poäng}', 1, (255, 255, 255))
    fönster.blit(poängKollen, (fönsterBredd - (poängKollen.get_width() + 10), fönsterHöjd - poängKollen.get_height()))
    j = 0
    while len(meteoritLista) > j:
        fönster.blit(meteoritLista[j].meteorit, (meteoritLista[j].meteoritRektangel.x, meteoritLista[j].meteoritRektangel.y))
        meteoritLista[j].fallLinje()
        if meteoritLista[j].getPosY() > fönsterHöjd:
            meteoritLista.remove(meteoritLista[j])
        j += 1
    i = 0
    while len(skottLista) > i:
        fönster.blit(skottLista[i].skott, (skottLista[i].skottRektangel.x, skottLista[i].skottRektangel.y))
        skottLista[i].skottLinje()
        if skottLista[i].getPosY() < 0:
            skottLista.remove(skottLista[i])
        i += 1
    k = 0
    while len(explosionLista) > k:
        fönster.blit(explosionLista[k].explosion, (explosionLista[k].explosionRektangel.x, explosionLista[k].explosionRektangel.y))
        explosionLista[k].fallLinje()
        if explosionLista[k].getPosX() > fönsterBredd or explosionLista[k].getPosX() < 0 or explosionLista[k].getPosY() > fönsterHöjd or explosionLista[k].getPosY() < 0:
            explosionLista.remove(explosionLista[k])
        k += 1
    pygame.display.update()


def main():
    poäng = 0
    mixer.Sound('technoTF.mp3').play(-1).set_volume(0.18)
    klocka = pygame.time.Clock()
    while True:
        klocka.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_LCTRL or event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER)  and len(skottLista) < 3:
                sk = skott(12, 24, 'skott1.png', 'zap-mot.wav', 0.1, skepp)
                skottLista.append(sk)
                sk.skjutLjud.play()
            if event.type == skeppetTräffat:
                gameOver(poäng)

        knapp_intryckt = pygame.key.get_pressed()
        if knapp_intryckt[pygame.K_DOWN] or knapp_intryckt[pygame.K_s]:
            skepp.gåNedåt()
        if knapp_intryckt[pygame.K_UP] or knapp_intryckt[pygame.K_w]:
            skepp.gåUppåt()
        if knapp_intryckt[pygame.K_RIGHT] or knapp_intryckt[pygame.K_d]:
            skepp.gåÅtHöger()
        if knapp_intryckt[pygame.K_LEFT] or knapp_intryckt[pygame.K_a]:
            skepp.gåÅtVänster()

        for s in skottLista:
            for m in meteoritLista:
                resultat = s.skottRektangel.colliderect(m.meteoritRektangel)
                if resultat:
                    explosionGenerator(m)
                    meteoritLista.remove(m)
                    skottLista.remove(s)
                    poäng += 1
                    print(resultat)

        for s in skottLista:
            for e in explosionLista:
                resultat = s.skottRektangel.colliderect(e.explosionRektangel)
                if resultat:
                    mixer.Sound('short-explosion.wav').play().set_volume(0.2)
                    explosionLista.remove(e)
                    skottLista.remove(s)
                    poäng += 1
                    print(f'{resultat} skräp')

        for m in meteoritLista:
            resultat = skepp.rektangel.colliderect(m.meteoritRektangel)
            if resultat:
                pygame.event.post(pygame.event.Event(skeppetTräffat))
                print("Skeppet blev träffat")

        for k in explosionLista:
            resultat = skepp.rektangel.colliderect(k.explosionRektangel)
            if resultat:
                pygame.event.post(pygame.event.Event(skeppetTräffat))
                print("Skeppet blev träffat")
        rita(poäng)
        schedule.run_pending()

# denna rad ser till att main metoden endast körs om man kör denna fil direkt, istället för att importera den
if __name__ == "__main__":
    main()
