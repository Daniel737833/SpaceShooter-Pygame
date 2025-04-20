# Skriv din kod här för att skapa spelet! Följ dessa steg:
# Steg 1 - Skapa en skärm och rita ett skepp
# Steg 2 - Lägga till en scrollande stjärnbakgrund
# Steg 3 - Sätt jetmotorer på rymdskeppet
# Steg 4 - Gör så rymdskeppet kan skjuta
# Steg 5 - Slumpa fram Asteroider 
# Steg 6 - Detektera kollisioner mellan rymdskeppet och asteroiden
# Steg 7 - Skapa explosionseffekten (samt lär dig partikeleffekter)
# Steg 8 - Gör så att rymdskeppet kan explodera i kollision med asteroiden
# Steg 9 - Gör så att rymdskeppet kan skjuta ner asteroider
# Steg 10 - Lägg till musik och ljudeffekter

import pygame
import random
import math


pygame.init()

SKÄRMENS_BREDD = 850
SKÄRMENS_HÖJD = 650

skärm = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))

pygame.display.set_caption("Space Shooter")

pygame.mixer.init()

pygame.mixer.music.load("assets/music/Balkan.sound.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

ljud_explosion = pygame.mixer.Sound("assets/sounds/scfi_explosion.wav")
ljud_explosion.set_volume(0.7)

ljud_huge_explosion = pygame.mixer.Sound("assets/sounds/huge_explosion.wav")
ljud_huge_explosion.set_volume(0.7)

# LADDA IN ALL GRAFIK
background_mörkblå = pygame.image.load("assets/backgrounds/bg.png")
background_stjärnor = pygame.image.load("assets/backgrounds/Stars-A.png")
sprite_spelare = pygame.image.load("assets/sprites/SpaceShip.png")
original_bild = pygame.image.load("assets/sprites/SpaceShip.png")
sprite_spelare = pygame.transform.scale(original_bild, (original_bild.get_width() // 2, original_bild.get_height() // 2))
sprite_jetstråle = pygame.image.load("assets/sprites/fire.png")
sprite_skott = pygame.image.load("assets/sprites/bullet.png")
sprite_asteroid_liten = pygame.image.load("assets/sprites/small-A.png")

# SÄTT ALLA STARTVÄRDEN TILL VARIABLER I SPELET
spelare_x = SKÄRMENS_BREDD // 2 - 120
spelare_y = SKÄRMENS_HÖJD - 200
spelarens_hastighet = 5
spelet_körs = True
jetstråle_x = spelare_x + 13
jetstråle_y = spelare_y + 46
bakgrund_y = 0
skott_lista = []
skott_räknare = 0
asteroid_liten_x = 100
asteroid_liten_x = random.randint(0, SKÄRMENS_BREDD)
asteroid_liten_y = 100
asteroid_liten_hastighet = 4
asteroid_liten_lista = []
asteroid_liten_räknare = 0
explosioner = []

poäng = 0
font = pygame.font.Font(None, 36)

class Skott:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hastighet = 10
        self.bild = sprite_skott

    def flytta(self):
        self.y = self.y - self.hastighet

    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))

class AsteroidLiten:
    def __init__(self, asteroid_liten_x, asteroid_liten_y):
        self.x = asteroid_liten_x
        self.y = asteroid_liten_y
        self.hastighet = 3 # Sänk hastigheten från 4 till 2
        self.bild = sprite_asteroid_liten
        self.kollisions_rektangel_asteroid = pygame.Rect(self.x, self.y, self.bild.get_width(), self.bild.get_height())

    def kollidera(self, kollisionsobjekt):
        if (self.kollisions_rektangel_asteroid.colliderect(kollisionsobjekt)):
            print ("kollision upptäckt!")

    def flytta(self):
        self.y = self.y + self.hastighet
        self.kollisions_rektangel_asteroid.topleft = (self.x, self.y)

    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))

class Explosion:
    def __init__(self, x, y):
        self.partiklar = []
        for _ in range(50):
            vinkel = random.uniform(0, 2 * math.pi)
            hastighet = random.uniform(2, 5)
            livstid = random.randint(20, 50)
            self.partiklar.append({
                'x': x,
                'y': y,
                'vinkel': vinkel,
                'hastighet': hastighet,
                'livstid': livstid })

    def uppdatera(self):
        for partikel in self.partiklar:
            partikel['x'] += math.cos(partikel['vinkel']) * partikel['hastighet']
            partikel['y'] += math.sin(partikel['vinkel']) * partikel['hastighet']
            partikel['livstid'] -= 1
        self.partiklar = [p for p in self.partiklar if p['livstid'] > 0]

    def rita(self, skärm):
        for partikel in self.partiklar:
            pygame.draw.circle(skärm, (255, 165, 0), (int(partikel['x']), int(partikel['y'])), 3)
    
class Partikel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.livstid = random.randint(20, 50)
        self.hastighet_x = random.uniform(-2, 2)
        self.hastighet_y = random.uniform(-2, 2)
        self.radius = random.randint(3, 6)
        self.färg = random.choice([(255, 50, 50), (255, 150, 50), (255, 255, 50)])

    def uppdatera(self):
        self.x += self.hastighet_x
        self.y += self.hastighet_y
        self.livstid -= 1

    def rita(self, skärm):
        if self.livstid > 0:
            pygame.draw.circle(skärm, self.färg, (int(self.x), int(self.y)), self.radius)
    
class Rymdskepp:
    def __init__(self):
        self.rymdskepp_x = SKÄRMENS_BREDD // 2 - 120
        self.rymdskepp_y = SKÄRMENS_HÖJD - 200
        self.sprite_rymdskepp = sprite_spelare

        self.jetstråle_x = self.rymdskepp_x + 13
        self.jetstråle_y = self.rymdskepp_y + 46
        self.sprite_jetstråle = sprite_jetstråle

        self.rymdskeppets_hastighet = 10

        self.exploderat = False

        self.kollisions_rektangel = pygame.Rect(self.rymdskepp_x, self.rymdskepp_y, self.sprite_rymdskepp.get_width(), self.sprite_rymdskepp.get_height())

    def flytta(self, riktning):
        if not self.exploderat:
            if riktning == "vänster":
                self.rymdskepp_x = self.rymdskepp_x - self.rymdskeppets_hastighet
                self.jetstråle_x = self.jetstråle_x - self.rymdskeppets_hastighet
            elif riktning == "höger":
                self.rymdskepp_x = self.rymdskepp_x + self.rymdskeppets_hastighet
                self.jetstråle_x = self.jetstråle_x + self.rymdskeppets_hastighet
            elif riktning == "upp":
                self.rymdskepp_y = self.rymdskepp_y - self.rymdskeppets_hastighet
                self.jetstråle_y = self.jetstråle_y - self.rymdskeppets_hastighet
            elif riktning == "ner":
                self.rymdskepp_y = self.rymdskepp_y + self.rymdskeppets_hastighet
                self.jetstråle_y = self.jetstråle_y + self.rymdskeppets_hastighet

            self.kollisions_rektangel.topleft = (self.rymdskepp_x, self.rymdskepp_y)

    def rita(self, skärm):
        if not self.exploderat:
            skärm.blit(self.sprite_rymdskepp, (self.rymdskepp_x, self.rymdskepp_y))
            skärm.blit(self.sprite_jetstråle, (self.jetstråle_x, self.jetstråle_y))
        else:
            self.kollisions_rektangel = pygame.Rect(0, 0, 0, 0)
            
    def kollidera(self, rymdskepp):
        if not spelare_1.exploderat:
            if (self.kollisions_rektangel.colliderect(rymdskepp)):
                print ("kollision upptäckt med rymdskeppet!")
                spelare_1.exploderat = True
                explosioner.append(Explosion(spelare_1.rymdskepp_x + 60, spelare_1.rymdskepp_y + 46) for _ in range(100))
                explosioner.append(explosion)

spelare_1 = Rymdskepp()

while (spelet_körs == True):

    skärm.blit(sprite_asteroid_liten, (asteroid_liten_x, asteroid_liten_y))

    asteroid_liten_y = asteroid_liten_y + asteroid_liten_hastighet

    skärm.blit(sprite_spelare, (spelare_x, spelare_y))
     

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            spelet_körs = False

    pygame.display.update()   

    skärm.blit(background_mörkblå, (0,0))

    skärm.blit(background_stjärnor, (0, bakgrund_y))

    skärm.blit(background_stjärnor, (0, bakgrund_y - SKÄRMENS_HÖJD))

    bakgrund_y = bakgrund_y + 2

    if bakgrund_y >= SKÄRMENS_HÖJD:
        bakgrund_y = 0


    skärm.blit(sprite_jetstråle, (spelare_x + 12, spelare_y + 50))

    for skott in reversed(skott_lista):
        skott.flytta()
        skott.rita(skärm)

        for asteroid_liten in reversed(asteroid_liten_lista):
            if pygame.Rect(skott.x, skott.y, skott.bild.get_width(), skott.bild.get_height()).colliderect(asteroid_liten.kollisions_rektangel_asteroid):
                pygame.mixer.Sound.play(ljud_explosion)  
                explosioner.append(Explosion(asteroid_liten.x, asteroid_liten.y))
                asteroid_liten_lista.remove(asteroid_liten)
                if skott in skott_lista:
                    skott_lista.remove(skott)
                poäng += 1  
                break

        if skott.y < -100:
            if skott in skott_lista:
                skott_lista.remove(skott)  
    skott_räknare += 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spelare_x > 0:
        spelare_x -= spelarens_hastighet
    if keys[pygame.K_RIGHT] and spelare_x < SKÄRMENS_BREDD - sprite_spelare.get_width():
        spelare_x += spelarens_hastighet
    if keys[pygame.K_UP] and spelare_y > 0:
        spelare_y -= spelarens_hastighet
    if keys[pygame.K_DOWN] and spelare_y < SKÄRMENS_HÖJD - sprite_spelare.get_height():
        spelare_y += spelarens_hastighet

    if keys[pygame.K_SPACE]:

        if (skott_räknare > 10):

            skott_lista.append(Skott(spelare_x + 20, spelare_y))

            skott_räknare = 0
    
    if asteroid_liten_räknare >= 20:
        asteroid_liten_lista.append(AsteroidLiten(random.randint(0, SKÄRMENS_BREDD - sprite_asteroid_liten.get_width()), 0))
        asteroid_liten_räknare = 0

    asteroid_liten_räknare += 1

    kollisions_rektamgel_spelare = pygame.Rect(spelare_x, spelare_y, sprite_spelare.get_width(), sprite_spelare.get_height())

    for asteroid_liten in reversed(asteroid_liten_lista):
        asteroid_liten.flytta()
        asteroid_liten.kollidera(spelare_1.kollisions_rektangel)
        asteroid_liten.rita(skärm)

        if (spelare_1.exploderat == True):
            paus = paus + 1
            if (paus >= 120):
                exit()

        if asteroid_liten.y > SKÄRMENS_HÖJD:
            asteroid_liten_lista.remove(asteroid_liten)

    # Lägg till en explosion vid kollision
    for asteroid_liten in reversed(asteroid_liten_lista):
        asteroid_liten.flytta()
        asteroid_liten.rita(skärm)
        asteroid_liten.rita(skärm)

    # Uppdatera kollision med asteroid för att inkludera explosion och partiklar
    for asteroid_liten in reversed(asteroid_liten_lista):
        if asteroid_liten.kollisions_rektangel_asteroid.colliderect(kollisions_rektamgel_spelare):
            pygame.mixer.Sound.play(ljud_huge_explosion)  # Spela upp ljudet vid kollision
            explosioner.append(Explosion(spelare_x, spelare_y))  # Skapa explosion vid rymdskeppets position
            partiklar = [Partikel(spelare_x, spelare_y) for _ in range(30)]  # Skapa partiklar
            explosioner.append(partiklar)
            spelet_körs = False  # Avsluta spelet direkt vid kollision
            break

    # Uppdatera och rita explosioner och partikeleffekter
    for explosion in explosioner:
        if isinstance(explosion, list):
            for partikel in explosion:
                partikel.uppdatera()
                partikel.rita(skärm)
        else:
            explosion.uppdatera()
            explosion.rita(skärm)

    # Ta bort döda partiklar
    explosioner = [e for e in explosioner if not isinstance(e, list) or any(p.livstid > 0 for p in e)]

    # Rita poäng på skärmen
    poäng_text = font.render(f"Poäng: {poäng}", True, (255, 255, 255))
    skärm.blit(poäng_text, (10, 10))

    # Lägg till Game Over-text
    if not spelet_körs:
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("SPELET ÄR SLUT!", True, (255, 0, 0))
        skärm.blit(game_over_text, (SKÄRMENS_BREDD // 2 - game_over_text.get_width() // 2, SKÄRMENS_HÖJD // 2 - game_over_text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(3000) 
        break

pygame.quit()