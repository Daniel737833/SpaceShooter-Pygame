import pygame
import random

# Initiera pygame
pygame.init()

# Skärmstorlek
SKÄRM_BREDD = 800
SKÄRM_HÖJD = 600
skärm = pygame.display.set_mode((SKÄRM_BREDD, SKÄRM_HÖJD))
pygame.display.set_caption("Explosion med partiklar")

# Färger
SVART = (0, 0, 0)
FÄRG_LISTA = [(255, 50, 50), (255, 150, 50), (255, 255, 50)]  # Röd, orange, gul

# Klass för en enskild partikel
class Partikel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.livstid = random.randint(20, 50)  # Hur länge partikeln lever
        self.hastighet_x = random.uniform(-2, 2)  # Slumpmässig rörelse i x-led
        self.hastighet_y = random.uniform(-2, 2)  # Slumpmässig rörelse i y-led
        self.radius = random.randint(3, 6)  # Storlek på partikeln
        self.färg = random.choice(FÄRG_LISTA)  # Slumpmässig färg

    def uppdatera(self):
        self.x += self.hastighet_x  # Flytta partikeln i x-led
        self.y += self.hastighet_y  # Flytta partikeln i y-led
        self.livstid -= 1  # Minska livslängden

    def rita(self, skärm):
        if self.livstid > 0:
            pygame.draw.circle(skärm, self.färg, (int(self.x), int(self.y)), self.radius)

# Lista för alla explosioner (varje explosion är en lista med partiklar)
explosioner = []

# Spelloop
spelet_körs = True
while spelet_körs:
    skärm.fill(SVART)

    # Händelsehantering
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spelet_körs = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Skapa explosion vid musklick
            mus_x, mus_y = pygame.mouse.get_pos()
            explosion = [Partikel(mus_x, mus_y) for _ in range(30)]  # Skapa 30 partiklar
            explosioner.append(explosion)

    # Uppdatera och rita explosionerna
    for explosion in explosioner:
        for partikel in explosion:
            partikel.uppdatera()
            partikel.rita(skärm)

    # Ta bort döda partiklar (de som har en livslängd på 0)
    explosioner = [[p for p in explosion if p.livstid > 0] for explosion in explosioner]
    explosioner = [e for e in explosioner if len(e) > 0]  # Ta bort tomma explosioner

    pygame.display.update()
    pygame.time.delay(16)  # Kontrollera hastigheten på spelet (ca 60 FPS)

pygame.quit()
