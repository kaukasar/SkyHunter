import sys
import threading
import schedule
import pygame
from pygame import mixer
import random
from resurser import rymdskepp, meteorit, explosion, skott, stjärna, powerup

class svårighetsgrad:
    def __init__(self):
        self.grad = 1.0
        self.ökningsTid = 10

    def öka(self):
        if self.grad > 0.11:
            self.grad -= 0.1
        elif self.grad > 0.02 and self.grad < 0.12:
            self.grad -= 0.01
        print(round(sv.grad * 100))

bg = pygame.image.load('quasar.jpg')
fönsterBredd, fönsterHöjd = 1200, 1024
fönster = pygame.display.set_mode((fönsterBredd, fönsterHöjd))
meteoritTyper = ('meteorit1.png', 'meteorit2.png', 'meteorit3.png', 'meteorit4.png', 'meteorit5.png')
pygame.display.set_caption("Sky Hunter")
skepp = rymdskepp(fönsterBredd, fönsterHöjd)
mixer.init()
pygame.font.init()
skottLista, meteoritLista, explosionLista, stjärnLista, powerupLista = [], [], [], [], []
sv = svårighetsgrad()
skeppetTräffat = pygame.USEREVENT + 1
FPS = 60

def meteoritGenerator():
    try:
        typ = random.choice(meteoritTyper)
        xKoordinat = random.randrange(1, fönsterBredd-60)
        m = meteorit(random.randrange(45, 85), random.randrange(45, 85), typ, xKoordinat)
        meteoritLista.append(m)
        tråd = threading.Timer(sv.grad, meteoritGenerator)
        tråd.daemon = True # Detta behöver vara satt för att tråden ska dö när man anropar sys.exit()
        tråd.start()
    except:
        pass

def explosionGenerator(meteorit):
    try:
        for _ in range(3):
            xpl = explosion('explosion.mp3', 0.2, meteorit, random.randrange(-10, 10), random.randrange(-10, 10))
            explosionLista.append(xpl)
        xpl.explosionsLjud.play()
    except:
        pass

def stjärnGenerator():
    st = stjärna(random.randrange(50, fönsterBredd-400))
    stjärnLista.append(st)

def powerupGenerator():
    power = powerup(random.randrange(220, fönsterBredd-250))
    powerupLista.append(power)

meteoritGenerator()
schedule.every(sv.ökningsTid).seconds.do(sv.öka)
schedule.every(int(sv.ökningsTid*1.4)).seconds.do(stjärnGenerator)
schedule.every(int(sv.ökningsTid*3.9)).seconds.do(powerupGenerator)

def gameOver(poäng):
    try:
        mixer.Sound('arcade-explosion-echo.wav').play().set_volume(0.3)
        ritaText = pygame.font.SysFont('comicsans', 80).render("Game Over!", 1, (255, 255, 255))
        ritaText2 = pygame.font.SysFont('comicsans', 60).render(f'Du fick {poäng} poäng', 1, (255, 255, 255))
        fönster.blit(pygame.transform.scale(pygame.image.load('exp.png'), (skepp.skeppBredd, skepp.skeppHöjd)),
                     (skepp.getPosX(), skepp.getPosY()))
        fönster.blit(ritaText, (fönsterBredd/2 - ritaText.get_width()/2, fönsterHöjd/2 - ritaText.get_height()))
        fönster.blit(ritaText2, (fönsterBredd / 2 - ritaText2.get_width() / 2, fönsterHöjd / 2))
        pygame.display.update()
        pygame.time.delay(10000)
        pygame.quit()
        sys.exit()
    except:
        pass

def rita(poäng):
    try:
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
        s = 0
        while len(stjärnLista) > s:
            fönster.blit(stjärnLista[s].stjärna, (stjärnLista[s].stjärnaRektangel.x, stjärnLista[s].stjärnaRektangel.y))
            stjärnLista[s].fallLinje()
            if stjärnLista[s].getPosY() > fönsterHöjd:
                stjärnLista.remove(stjärnLista[s])
            s += 1
        p = 0
        while len(powerupLista) > p:
            fönster.blit(powerupLista[p].powerup, (powerupLista[p].powerupRektangel.x, powerupLista[p].powerupRektangel.y))
            powerupLista[p].fallLinje()
            if powerupLista[p].getPosY() > fönsterHöjd:
                powerupLista.remove(powerupLista[p])
            p += 1
        pygame.display.update()
    except:
        pass

def main():
    poäng = 0
    skottTyp = 1
    mixer.Sound('technoTF.mp3').play(-1).set_volume(0.19)
    klocka = pygame.time.Clock()
    speletIgång = True
    while speletIgång:
        klocka.tick(FPS)
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    speletIgång = False
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_LCTRL or event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER)  and len(skottLista) < 3:
                    if skottTyp == 1:
                        sk = skott(14, 26, 'skott1.png', 'zap-mot.wav', 0.05, skepp)
                    if skottTyp == 2:
                        sk = skott(22, 26, 'skott2.png', 'zap-mot.wav', 0.05, skepp)
                    if skottTyp == 3:
                        sk = skott(30, 30, 'skott3.png', 'zap-mot.wav', 0.05, skepp)
                    skottLista.append(sk)
                    sk.skjutLjud.play()
                if event.type == skeppetTräffat:
                    speletIgång = False
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

            for s in skottLista:
                for e in explosionLista:
                    resultat = s.skottRektangel.colliderect(e.explosionRektangel)
                    if resultat:
                        mixer.Sound('short-explosion.wav').play().set_volume(0.2)
                        explosionLista.remove(e)
                        skottLista.remove(s)
                        poäng += 1

            for m in meteoritLista:
                resultat = skepp.rektangel.colliderect(m.meteoritRektangel)
                if resultat:
                    pygame.event.post(pygame.event.Event(skeppetTräffat))

            for k in explosionLista:
                resultat = skepp.rektangel.colliderect(k.explosionRektangel)
                if resultat:
                    pygame.event.post(pygame.event.Event(skeppetTräffat))

            for s in stjärnLista:
                resultat = skepp.rektangel.colliderect(s.stjärnaRektangel)
                if resultat:
                    mixer.Sound('coin.wav').play().set_volume(0.3)
                    stjärnLista.remove(s)
                    poäng += 10

            for p in powerupLista:
                resultat = skepp.rektangel.colliderect(p.powerupRektangel)
                if resultat:
                    mixer.Sound('powerup.wav').play().set_volume(0.4)
                    powerupLista.remove(p)
                    if skottTyp < 3:
                        skottTyp += 1
        except:
            pass
        rita(poäng)
        schedule.run_pending()
    pygame.quit()
    sys.exit()
# denna rad ser till att main metoden endast körs om man kör denna fil direkt, istället för att importera den
if __name__ == "__main__":
    main()
