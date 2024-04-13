import pygame

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_SPEED = 600.0
PROJECTILE_COOLDOWN_TIME = 200
FPS = 120
CLOCK = pygame.time.Clock()
PROJECTILE_SIZE = SCREEN_WIDTH/160
PLAYER_HEIGHT = SCREEN_HEIGHT/20
PLAYER_WIDTH = SCREEN_HEIGHT/40

window = pygame.display.set_mode(((SCREEN_WIDTH, SCREEN_HEIGHT)))
player = pygame.Rect(((SCREEN_WIDTH/2 - PLAYER_WIDTH/2), (SCREEN_HEIGHT -
                     2.5*(PLAYER_HEIGHT)), (PLAYER_WIDTH), (PLAYER_HEIGHT)))
projectileArray = []
projectileArraySize = 0
projectileCurrCooldown = 0
projectileCooldownBool = False

run = True
while run:
    dt = CLOCK.tick(FPS)/1000.0
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (0, 0, 255), player)

    if projectileCurrCooldown:
        projectileCurrCooldown += CLOCK.get_time()
        if projectileCurrCooldown > PROJECTILE_COOLDOWN_TIME:
            projectileCurrCooldown = 0
            projectileCurrCooldown = False

    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        if ((player.x - PLAYER_SPEED * dt) >= 0):
            player.x -= PLAYER_SPEED * dt
        else:
            player.x = 0
    if key[pygame.K_d]:
        if ((player.x + PLAYER_SPEED * dt) <= (SCREEN_WIDTH - SCREEN_WIDTH/20)):
            player.x += PLAYER_SPEED * dt
        else:
            player.x = SCREEN_WIDTH - SCREEN_WIDTH/20
    if key[pygame.K_SPACE] and projectileCurrCooldown == False:
        projectileCurrCooldown = True
        projectileArraySize += 1
        projectileArray.append(pygame.Rect(
            ((player.x + PROJECTILE_SIZE/2), player.y, PROJECTILE_SIZE, PROJECTILE_SIZE)))

    indexes = []
    for i in range(0, projectileArraySize):
        pygame.draw.rect(window, (0, 255, 255), projectileArray[i])
        projectileArray[i].move_ip(0, -5)
        if projectileArray[i]. y < 0 - PROJECTILE_SIZE:
            indexes.append(i)

    for i in range(0, len(indexes)):
        del projectileArray[indexes[i]]
        projectileArraySize -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
