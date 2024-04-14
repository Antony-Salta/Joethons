import pygame
import asyncio
import random


def astroidGen():
    global astroidArray, SCREEN_HEIGHT, SCREEN_WIDTH, PROJECTILE_SIZE, astroidDirectionArray, ASTROID_SIZE
    astroidX = random.randint(0, int(SCREEN_WIDTH-PROJECTILE_SIZE))
    astroidArray.append(pygame.Rect(
        (astroidX, SCREEN_WIDTH/20, ASTROID_SIZE, ASTROID_SIZE)))
    direction = random.randint(0, 2)
    if direction == 0:
        astroidDirectionArray.append(0)
    elif direction == 1:
        astroidDirectionArray.append(-2)
    else:
        astroidDirectionArray.append(2)


def astroidsMove():
    global astroidArray, astroidDirectionArray
    for i in range(0, len(astroidArray)):
        pygame.draw.rect(window, (255, 255, 255), astroidArray[i])
        astroidArray[i].move_ip(astroidDirectionArray[i], 4)


def astroidClear():
    global astroidArray, astroidDirectionArray
    indexesToDel = []
    for i in range(0, len(astroidArray)):
        if astroidArray[i].x < 0 - ASTROID_SIZE or astroidArray[i].x > SCREEN_WIDTH or astroidArray[i].y > SCREEN_HEIGHT:
            indexesToDel.append(i)
    for i in reversed(indexesToDel):
        del astroidArray[i]
        del astroidDirectionArray[i]


def drawMainScreen():
    global window, textSurface, player, distance, font, SCREEN_WIDTH
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (0, 0, 255), player)
    distanceText = "Distance remaining: " + str(int(distance)) + "km"
    textSurface = font.render(
        distanceText, True, (255, 255, 255), (0, 0, 0))
    window.blit(textSurface, dest=(0, 0))
    livesText = "Lives: " + str(LIVES)
    textSurface = font.render(livesText, True, (255, 255, 255))
    window.blit(textSurface, dest=(
        SCREEN_WIDTH - textSurface.get_width(), 0))


def resetGameState():
    global alive, LIVES, player, SCREEN_WIDTH, PLAYER_WIDTH, SCREEN_HEIGHT, PLAYER_HEIGHT, projectileArray, astroidArray, start, distance
    alive = True
    LIVES = 3
    player = pygame.Rect(((SCREEN_WIDTH/2 - PLAYER_WIDTH/2), (SCREEN_HEIGHT - 2.5*(
        PLAYER_HEIGHT)), (PLAYER_WIDTH), (PLAYER_HEIGHT)))
    projectileArray = []
    astroidArray = []
    start = False
    distance = distanceTotal


def setupGameOver():
    global window, font, SCREEN_WIDTH, SCREEN_HEIGHT, textSurface, retryRect, retrySurface
    window.fill((0, 0, 0))
    retrySurface = font.render("RETRY", False, (255, 255, 255))
    retryRect = retrySurface.get_rect()
    retryRect.x = SCREEN_WIDTH/2 - retryRect.width/2
    retryRect.y = 0.75*SCREEN_HEIGHT
    pygame.draw.rect(window, (0, 255, 0), retryRect)
    textSurface = font.render(
        "You crashed! Game Over!", False, (255, 255, 255))
    window.blit(textSurface, (SCREEN_WIDTH/2 - textSurface.get_width() /
                              2, SCREEN_HEIGHT/2 - textSurface.get_height()/2))
    window.blit(retrySurface, retryRect)
    pygame.display.update()
    return retryRect


async def main():
    global SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PROJECTILE_COOLDOWN_TIME, FPS, COUNTDOWN, CLOCK, PROJECTILE_SIZE, PLAYER_HEIGHT, PLAYER_SPEED, ASTROID_SPAWN_TIME, ASTROID_SIZE, LIVES, window, player, font, projectileArray, projectileArraySize, projectileCurrCooldown, projectileCooldownBool, astroidArray, astroidDirectionArray, timeForAstroidSpawn, distance, distanceTotal, distancePerMS, countdownStart, alive, run, start, dt, retrySurface, retryRect
    while run:
        for event in pygame.event.get():
            drawMainScreen()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_SPACE:
                    start = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retryRect.collidepoint(pygame.mouse.get_pos()):
                    setupGameOver()
                    resetGameState()

        if alive and distance > 0 and start:
            currentTime = pygame.time.get_ticks()
            elapsedTime = currentTime - countdownStart
            if distanceTotal - elapsedTime*distancePerMS > 0:
                distance = distanceTotal - elapsedTime*distancePerMS
            else:
                distance = 0

            window.fill((0, 0, 0))
            pygame.draw.rect(window, (0, 0, 255), player)
            distanceText = "Distance remaining: " + str(int(distance)) + "km"
            textSurface = font.render(
                distanceText, True, (255, 255, 255), (0, 0, 0))
            window.blit(textSurface, dest=(0, 0))
            livesText = "Lives: " + str(LIVES)
            textSurface = font.render(livesText, True, (255, 255, 255))
            window.blit(textSurface, dest=(
                SCREEN_WIDTH - textSurface.get_width(), 0))

            if projectileCurrCooldown:
                projectileCurrCooldown += CLOCK.get_time()
                if projectileCurrCooldown > PROJECTILE_COOLDOWN_TIME:
                    projectileCurrCooldown = 0
                    projectileCurrCooldown = False

            timeForAstroidSpawn += CLOCK.get_time()
            if timeForAstroidSpawn > ASTROID_SPAWN_TIME:
                timeForAstroidSpawn = 0
                astroidGen()

            astroidsMove()
            astroidClear()

            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                if ((player.x - PLAYER_SPEED * dt) >= 0):
                    player.x -= PLAYER_SPEED * dt
                else:
                    player.x = 0
            if key[pygame.K_d]:
                if ((player.x + PLAYER_SPEED * dt) <= (SCREEN_WIDTH - PLAYER_WIDTH)):
                    player.x += PLAYER_SPEED * dt
                else:
                    player.x = SCREEN_WIDTH - PLAYER_WIDTH
            if key[pygame.K_SPACE] and projectileCurrCooldown == False:
                projectileCurrCooldown = True
                projectileArraySize += 1
                projectileArray.append(pygame.Rect(
                    ((player.x + PROJECTILE_SIZE/2), player.y, PROJECTILE_SIZE, PROJECTILE_SIZE)))

            indexes = []
            for i in range(0, projectileArraySize):
                pygame.draw.rect(window, (0, 255, 0), projectileArray[i])
                projectileArray[i].move_ip(0, -5)
                if projectileArray[i]. y < 0 - PROJECTILE_SIZE:
                    indexes.append(i)

            for i in reversed(indexes):
                del projectileArray[i]
                projectileArraySize -= 1

            indexes = []
            astroidIndexes = []
            for i in range(0, len(projectileArray)):
                for j in range(0, len(astroidArray)):
                    if projectileArray[i].colliderect(astroidArray[j]):
                        indexes.append(i)
                        astroidIndexes.append(j)

            for i in reversed(indexes):
                del projectileArray[i]
                projectileArraySize -= 1

            for i in reversed(astroidIndexes):
                del astroidArray[i]
                del astroidDirectionArray[i]

            for i in range(0, len(astroidArray)):
                if player.colliderect(astroidArray[i]):
                    del astroidArray[i]
                    del astroidDirectionArray[i]
                    LIVES -= 1
                    if LIVES == 0:
                        alive = False
                    break

        if alive == False:
            retryRect = setupGameOver()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retryRect.collidepoint(pygame.mouse.get_pos()):
                        resetGameState()
        if distance == 0:
            window.fill((0, 0, 0))
            textSurface = font.render(
                "Congratulations! You made it through the asteroids!", False, (255, 255, 255))
            window.blit(textSurface, (SCREEN_WIDTH/2 - textSurface.get_width() /
                        2, SCREEN_HEIGHT/2 - textSurface.get_height()/2))

        pygame.display.update()
        dt = CLOCK.tick(FPS)/1000.0
        await asyncio.sleep(0)

    pygame.quit()

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_SPEED = 600.0
PROJECTILE_COOLDOWN_TIME = 200
FPS = 120
COUNTDOWN = 2 * 60 * 1000
CLOCK = pygame.time.Clock()
PROJECTILE_SIZE = SCREEN_WIDTH/160
PLAYER_HEIGHT = SCREEN_HEIGHT/20
PLAYER_WIDTH = SCREEN_HEIGHT/40
ASTROID_SPAWN_TIME = 500
ASTROID_SIZE = PROJECTILE_SIZE*4
LIVES = 3

window = pygame.display.set_mode(((SCREEN_WIDTH, SCREEN_HEIGHT)))
player = pygame.Rect(((SCREEN_WIDTH/2 - PLAYER_WIDTH/2), (SCREEN_HEIGHT -
                     2.5*(PLAYER_HEIGHT)), (PLAYER_WIDTH), (PLAYER_HEIGHT)))
font = pygame.font.SysFont("verdana", 30)

projectileArray = []
projectileArraySize = 0
projectileCurrCooldown = 0
projectileCooldownBool = False

astroidArray = []
astroidDirectionArray = []
timeForAstroidSpawn = 0

distanceTotal = 100000000
distance = distanceTotal
distancePerMS = distance/COUNTDOWN
countdownStart = pygame.time.get_ticks()

alive = True
run = True
start = False
dt = 0

retrySurface = font.render("RETRY", False, (255, 255, 255))
retryRect = retrySurface.get_rect()
retryRect.x = SCREEN_WIDTH/2 - retryRect.width/2
retryRect.y = 0.75*SCREEN_HEIGHT

asyncio.run(main())
