# Example file showing a circle moving on screen
import pygame
from sprites import Telescope, Hammer, Player
# pygame setup
pygame.init()
screen_size = (1280,720)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
background = pygame.image.load("explore/assets/grass.png").convert_alpha()
background = pygame.transform.scale(background, screen_size)
playerImage = pygame.image.load("explore/assets/joestronaut.png").convert_alpha()
#playerImage = pygame.transform.scale(player,[80,80])

allSprites = pygame.sprite.Group()

playerGroup = pygame.sprite.Group()
player = Player(80,80, playerImage, player_pos.x, player_pos.y, screen, 400)
player.add(playerGroup,allSprites)
screen.blit(background,(0,0))
#screen.blit(player, player_pos)

interactables = pygame.sprite.Group()
telescopeImage = pygame.image.load("explore/assets/telescope.png").convert_alpha()
telescope = Telescope(70,90,telescopeImage, 600, 500, screen)
interactables.add(telescope)

hammerImage = pygame.image.load("explore/assets/hammer.png").convert_alpha()
hammer = Hammer(70,90,hammerImage, 600, 500, screen)
interactables.add(telescope)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(background,(0,0))
    #screen.blit(player, player_pos)
    

    keys = pygame.key.get_pressed()
    
    if player.rect.x > screen_size[0] - player.width:
        player.rect.x = screen_size[0] - player.width
    elif player.rect.x < 0:
        player.rect.x = 0
    if player.rect.y > screen_size[1] - player.height:
        player.rect.y = screen_size[1] - player.height
    elif player.rect.y < 0:
        player.rect.y = 0
    
    
    # Explaining this: if you hit space, you can interact with an interactable thing, if you're touching one. 
    # If you are, then it'll go through the list until it interacts with one of them, then it will stop
    if(keys[pygame.K_SPACE]): 
        collidingSprites = pygame.sprite.spritecollide(player, interactables, False)
        if collidingSprites != None and len(collidingSprites) > 0:
            for i in range(len(collidingSprites)):
                if collidingSprites[0].interact():
                    break
    
    # flip() the display to put your work on screen
    interactables.update()
    interactables.draw(screen)
    playerGroup.update(keys, dt)
    playerGroup.draw(screen)
    pygame.display.update()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()