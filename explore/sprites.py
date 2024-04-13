import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, height, width, image, x, y, screen, speed):
        super().__init__()
        self.screen = screen
        self.image = pygame.transform.scale(image,[height,width])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.speed = speed
        

    def update(self, keys, dt):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.rect.y += self.speed * dt
        if keys[pygame.K_a]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.rect.x += self.speed * dt
        
    
            
        
    
class Interactable (pygame.sprite.Sprite):
    def __init__(self, height, width, image, x, y, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.transform.scale(image,[height,width])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.interacted = False
    
    
    def update(self):
        if(not self.interacted):
            pygame.draw.polygon(self.screen, (150,0,240), (((self.rect.x +self.width/2) -20, self.rect.y -30), ((self.rect.x +self.width/2), self.rect.y - 30), ((self.rect.x + self.width/2) - 10, self.rect.y)))
            
    ### This returns true if an interactable is now being interacted with, for the first/only really any time
    def interact(self):
        if self.interacted:
            return False
        self.interacted = True              
        return True
    
class Telescope (Interactable):
    def __init__(self, height, width, image, x, y, screen):
        super().__init__(height, width, image, x, y, screen)
        
    
    def interact(self ):
        if self.interacted:
            return False
        self.interacted = True  
        
        screen_size = (1280,720)
        clock = pygame.time.Clock()
        running = True
        timePassed = 0
        dt = 0

        background = pygame.image.load("explore/assets/EarthNight.png").convert_alpha()
        background = pygame.transform.scale(background, screen_size)
        newMoon = pygame.image.load("explore/assets/newMoon.png").convert_alpha()
        newMoon = pygame.transform.scale(newMoon, screen_size)
        
        crescentMoon = pygame.image.load("explore/assets/crescentMoon.png").convert_alpha()
        crescentMoon = pygame.transform.scale(crescentMoon, screen_size)
        
        halfMoon = pygame.image.load("explore/assets/halfMoon.png").convert_alpha()
        halfMoon = pygame.transform.scale(halfMoon, screen_size)
        
        fullMoon = pygame.image.load("explore/assets/fullMoon.png").convert_alpha()
        fullMoon = pygame.transform.scale(fullMoon, screen_size)
        
        exitFont = pygame.font.SysFont("Verdana", 60)
        exitButton = exitFont.render(" X ", True, (255,0,0), (0,0,0))
        exitRect = exitButton.get_rect()
        exitRect.x = screen_size[0] - exitButton.get_width()
        exitRect.y = 0
        
        font = pygame.font.SysFont("Verdana", 20)
        moonText = "The Earth has one moon, just called The Moon.\ncreative...\nThe moon can only be seen from light reflecting off the Sun at us.\n As the Moon's position changes, the way it looks changes.\n The main stages are the new moon, crescent moon,\n half moon, gibbon moon and full moon, going from nearly invisible to fully visible"
        text = font.render(moonText, True, (255,255,255), (0,0,0,0.3))
        textRect = text.get_rect()
        textRect.x= 30
        textRect.y = 50
        lines = moonText.split("\n")
        line_height = textRect.height
        lineRenders = [] 
        lineRects = []
        y = textRect.y
        for i, line in enumerate(lines):
            lineRender = font.render(line, True, (255,255,255), (0,0,0,0.3))
            lineRenders.append(lineRender)
            lineRect = lineRender.get_rect()
            lineRect.y = y + i * (line_height + 5)
            lineRects.append(lineRect)
            
        
        #playerImage = pygame.transform.scale(player,[80,80])

        self.screen.blit(background,(0,0))
        #screen.blit(player, player_pos)


        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    print(pygame.mouse.get_pos())
                    print(exitRect)
                    if exitRect.collidepoint(pygame.mouse.get_pos()):
                        print("clicked the thing")
                        running = False
            
            self.screen.blit(background,(0,0))

            keys = pygame.key.get_pressed()
            if timePassed % 20 < 5:
                self.screen.blit(newMoon, (0,0))
            elif timePassed % 20 < 10:
                self.screen.blit(crescentMoon, (0,0))
            elif timePassed % 20 < 15:
                self.screen.blit(halfMoon, (0,0))
            else:
                self.screen.blit(fullMoon, (0,0))

            # flip() the display to put your work on screen
            for i, lineRender in enumerate(lineRenders):
                self.screen.blit(lineRender, lineRects[i])
            
            self.screen.blit(exitButton, exitRect)
            pygame.display.update()
            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(60) / 1000
            timePassed += dt   
                    
        return True
            
            