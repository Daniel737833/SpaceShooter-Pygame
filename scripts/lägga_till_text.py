import pygame

# Initiera Pygame
pygame.init()

# Skapa skärmen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Ladda en font (inbyggd i Pygame)
font = pygame.font.Font(None, 74)  # Standardfont, storlek 74

# Skapa en text
text = font.render("GAME OVER", True, (255, 0, 0))  # Röd färg
text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Centrera texten

# Spelloop
running = True
while running:
    screen.fill((0, 0, 0))  # Svart bakgrund
    screen.blit(text, text_rect)  # Rita texten på skärmen
    
    pygame.display.flip()  # Uppdatera skärmen
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
