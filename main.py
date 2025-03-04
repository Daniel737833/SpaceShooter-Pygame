# Skriv din kod här för att skapa spelet! Följ dessa steg:
'''
Steg 1 - Skapa en skärm och rita ett skepp
Steg 2 - Lägga till en scrollande stjärnbakgrund
Steg 3 - Sätt jetmotorer på rymdskeppet
Steg 4 - Gör så rymdskeppet kan skjuta
Steg 5 - Slumpa fram Asteroider 
Steg 6 - Detektera kollisioner mellan rymdskeppet och asteroiden
Steg 7 - Skapa explosionseffekten (samt lär dig partikeleffekter)
Steg 8 - Gör så att rymdskeppet kan explodera i kollision med asteroiden
Steg 9 - Gör så att rymdskeppet kan skjuta ner asteroider
Steg 10 - Lägg till musik och ljudeffekter
'''
import pygame

SKÄRMENS_BREDD = 850
SKÄRMENS_HÖJD = 650

skärm = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))

pygame.display.set_caption("Space Shooter")

spelet_körs = True

original_bild = pygame.image.load("assets/sprites/spaceShip.png")

sprite_spelare = pygame.transform.scale(original_bild, (original_bild.get_width() // 2, original_bild.get_height() // 2))

spelare_x = SKÄRMENS_BREDD // 2 - 120
spelare_y = SKÄRMENS_HÖJD - 200
spelarens_hastighet = 1

background_mörkblå = pygame.image.load("assets/backgrounds/bg.png")
background_stjärnor = pygame.image.load("assets/backgrounds/Stars-A.png")

bakgrund_y = 0

while (spelet_körs == True):

    skärm.fill((0, 0, 30))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            spelet_körs = False
        
    skärm.blit(background_mörkblå, (0,0))

    skärm.blit(background_stjärnor, (0, bakgrund_y))

    skärm.blit(background_stjärnor, (0, bakgrund_y - SKÄRMENS_HÖJD))

    bakgrund_y = bakgrund_y + 2

    if bakgrund_y >= SKÄRMENS_HÖJD:
        bakgrund_y = 0

    skärm.blit(sprite_spelare, (spelare_x, spelare_y))
    pygame.display.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spelare_x > 0:
        spelare_x = spelare_x - spelarens_hastighet
    if keys[pygame.K_RIGHT] and spelare_x < SKÄRMENS_BREDD - sprite_spelare.get_width():
        spelare_x = spelare_x + spelarens_hastighet
    if keys[pygame.K_UP] and spelare_y > 0:
        spelare_y = spelare_y - spelarens_hastighet
    if keys[pygame.K_DOWN] and spelare_y < SKÄRMENS_HÖJD - sprite_spelare.get_width() + 26:
        spelare_y = spelare_y + spelarens_hastighet

pygame.quit()