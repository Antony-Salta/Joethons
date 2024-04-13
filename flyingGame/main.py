import pygame

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_SPEED = 600.0
FPS = 120
CLOCK = pygame.time.Clock()

window = pygame.display.set_mode(((SCREEN_WIDTH, SCREEN_HEIGHT)))
player = pygame.Rect(((SCREEN_WIDTH/2 - SCREEN_WIDTH/40), (SCREEN_HEIGHT -
                     2.5*(SCREEN_HEIGHT/20)), (SCREEN_WIDTH/20), (SCREEN_HEIGHT/20)))

run = True
while run:
    dt = CLOCK.tick(FPS)/1000.0
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (0, 0, 255), player)

    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        if ((player.x - PLAYER_SPEED * dt) >= 0):
            player.x -= PLAYER_SPEED * dt
        else:
            player.x = 0
    elif key[pygame.K_d]:
        if ((player.x + PLAYER_SPEED * dt) <= (SCREEN_WIDTH - SCREEN_WIDTH/20)):
            player.x += PLAYER_SPEED * dt
        else:
            player.x = SCREEN_WIDTH - SCREEN_WIDTH/20

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
