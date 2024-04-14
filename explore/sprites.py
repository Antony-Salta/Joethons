import pygame
import asyncio

screen_size = (1280,720)

###Returns the Surface object list and the associated Rect list  
def makeMultilineText(text, font):
    textRender = font.render(text, True, (255,255,255), (0,0,0,0.3))
    textRect = textRender.get_rect()
    textRect.x= 30
    textRect.y = screen_size[1]/2
    lines = text.split("\n")
    line_height = textRect.height
    lineRenders = [] 
    lineRects = []
    y = textRect.y
    for i, line in enumerate(lines):
        lineRender = font.render(line, True, (255,255,255), (0,0,0,0.3))
        lineRenders.append(lineRender)
        lineRect = lineRender.get_rect()
        lineRect.y = y + i * line_height 
        lineRects.append(lineRect)
    return lineRenders, lineRects
    
            


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
    def __init__(self, height, width, image, x, y, screen, planet):
        super().__init__()
        self.screen = screen
        self.image = pygame.transform.scale(image,[height,width])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.interacted = False
        self.planet = planet
    
    
    def update(self):
        if(not self.interacted):
            pygame.draw.polygon(self.screen, (150,0,240), (((self.rect.x +self.width/2) -20, self.rect.y -30), ((self.rect.x +self.width/2), self.rect.y - 30), ((self.rect.x + self.width/2) - 10, self.rect.y)))
            
    ### This returns true if an interactable is now being interacted with, for the first/only really any time
    async def interact(self):
        if self.interacted:
            return False
        self.interacted = True              
        return True
    
class Telescope (Interactable):
    def __init__(self, height, width, image, x, y, screen, planet):
        super().__init__(height, width, image, x, y, screen, planet)
        
    
    async def interact(self):
        self.interacted = True  
        

        clock = pygame.time.Clock()
        running = True
        timePassed = 0
        dt = 0
        
        

        background = pygame.image.load("assets/"+self.planet["Name"]+"/sky.png").convert_alpha()
        background = pygame.transform.scale(background, screen_size)
        
        if self.planet["Name"] == "Earth":
            newMoon = pygame.image.load("assets/Earth/newMoon.png").convert_alpha()
            newMoon = pygame.transform.scale(newMoon, screen_size)
            
            crescentMoon = pygame.image.load("assets/Earth/crescentMoon.png").convert_alpha()
            crescentMoon = pygame.transform.scale(crescentMoon, screen_size)
            
            halfMoon = pygame.image.load("assets/Earth/halfMoon.png").convert_alpha()
            halfMoon = pygame.transform.scale(halfMoon, screen_size)
            
            fullMoon = pygame.image.load("assets/Earth/fullMoon.png").convert_alpha()
            fullMoon = pygame.transform.scale(fullMoon, screen_size)
        
        exitFont = pygame.font.SysFont("Verdana", 60)
        exitButton = exitFont.render(" X ", True, (255,0,0), (0,0,0))
        exitRect = exitButton.get_rect()
        exitRect.x = screen_size[0] - exitButton.get_width()
        exitRect.y = 0
        
        font = pygame.font.SysFont("Verdana", 20)
        moonText = self.planet["skyText"]
        
        lineRenders, lineRects = makeMultilineText(moonText, font)
        
        #playerImage = pygame.transform.scale(player,[80,80])

        self.screen.blit(background,(0,0))
        #screen.blit(player, player_pos)


        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    if exitRect.collidepoint(pygame.mouse.get_pos()):
                        running = False
            
            self.screen.blit(background,(0,0))

            keys = pygame.key.get_pressed()
            if self.planet["Name"] == "Earth":
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
            await asyncio.sleep(0)

            
class Hammer (Interactable):
    def __init__(self, height, width, image, x, y, screen, planet):
        super().__init__(height, width, image, x, y, screen, planet)
    

    async def interact(self ):
        
        print("Made it here")
        
        self.interacted = True  
        
        screen_size = (1280,720)
        clock = pygame.time.Clock()
        running = True
        timePassed = 0
        dt = 0

        background = pygame.image.load("assets/"+self.planet["Name"]+"/horizon.png").convert_alpha()
        background = pygame.transform.scale(background, screen_size)
        
        
        exitFont = pygame.font.SysFont("Verdana", 60)
        exitButton = exitFont.render(" X ", True, (255,0,0), (0,0,0))
        exitRect = exitButton.get_rect()
        exitRect.x = screen_size[0] - exitButton.get_width()
        exitRect.y = 0
        
        font = pygame.font.SysFont("Verdana", 20)
        text = self.planet["gravityText"]
        
        lineRenders, lineRects = makeMultilineText(text, font)
        
        hammerImage = pygame.image.load("assets/hammer.png").convert_alpha()
        hammerImage = pygame.transform.scale(hammerImage, (80,80))
        hammerRect = hammerImage.get_rect()
        hammerRect.x = screen_size[0] * 9/16
        hammerRect.y = screen_size[1] * 1/4
        
        featherImage = pygame.image.load("assets/feather.png").convert_alpha()
        featherImage = pygame.transform.scale(featherImage, (60,60))
        featherRect = featherImage.get_rect()
        featherRect.x = screen_size[0] * 7/16
        featherRect.y = screen_size[1] * 1/4
        
        hammerTime = 0
        featherTime = 0
        
        font = pygame.font.SysFont("Fixed", 20)
        featherTimer = font.render(str(featherTime), True, (255,255,255), (0,0,0,0.1)) 
        hammerTimer = font.render(str(featherTime), True, (255,255,255), (0,0,0,0.1)) 
        
        ftRect = featherTimer.get_rect()
        htRect = featherTimer.get_rect()
        
        ftRect.x = featherRect.x
        ftRect.y = screen_size[1] * 7/8
        
        htRect.x = hammerRect.x
        htRect.y = screen_size[1] * 7/8
        
        
        self.screen.blit(background,(0,0))

        bothDown = False
        spacePressed = False
        selectedRect = None
        
        prompt = font.render("Press space to drop the hammer and feather.", True, (255,255,255), (0,0,0,0)).convert_alpha()
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    if exitRect.collidepoint(pygame.mouse.get_pos()):
                        running = False
                    if hammerRect.collidepoint(pygame.mouse.get_pos()):
                        selectedRect = hammerRect
                    if featherRect.collidepoint(pygame.mouse.get_pos()):
                        selectedRect = featherRect
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    selectedRect = None
            
            self.screen.blit(background,(0,0))
            #drag around selectedObject
            if selectedRect != None and pygame.mouse.get_pos()[1] <= screen_size[1] * 3/4:
                selectedRect.y = pygame.mouse.get_pos()[1]
            
            # flip() the display to put your work on screen
            
            keys = pygame.key.get_pressed()
            
            if(keys[pygame.K_SPACE]):
                spacePressed = True
            
            if spacePressed:
                if bothDown:
                    for i, lineRender in enumerate(lineRenders):
                        self.screen.blit(lineRender, lineRects[i])
                    
                else:
                    if hammerRect.y <= screen_size[1] * 3/4:
                        hammerRect.y += self.planet["hammerSpeed"] * dt
                        hammerTime += dt
                    if featherRect.y <= screen_size[1] * 3/4:
                        featherRect.y += self.planet["featherSpeed"] * dt
                        featherTime += dt
                    elif hammerRect.y >= screen_size[1] * 3/4 and featherRect.y >= screen_size[1] * 3/4:
                        bothDown = True
            else:
                self.screen.blit(prompt, (screen_size[0] /2 - prompt.get_width()/2, 0))
                
            featherTimer = font.render("{:.3f}".format(featherTime), True, (255,255,255), (0,0,0,0.1)) 
            hammerTimer = font.render("{:.3f}".format(hammerTime), True, (255,255,255), (0,0,0,0.1))
 
            
            self.screen.blit(hammerImage, hammerRect)
            self.screen.blit(featherImage, featherRect)
            self.screen.blit(exitButton, exitRect)
            self.screen.blit(featherTimer, ftRect)
            self.screen.blit(hammerTimer, htRect)
            pygame.display.update()
            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(60) / 1000
            timePassed += dt 
            await asyncio.sleep(0)
              
                    
            
            
class Thermometer(Interactable):
    def __init__(self, height, width, image, x, y, screen, planet):
        super().__init__(height, width, image, x, y, screen, planet)
    

    async def interact(self ):
        self.interacted = True  
        
        screen_size = (1280,720)
        clock = pygame.time.Clock()
        running = True
        timePassed = 0
        dt = 0

        background = pygame.image.load("assets/"+self.planet["Name"]+"/thermometerPlanet.png").convert_alpha()
        background = pygame.transform.scale(background, screen_size)
        
        
        exitFont = pygame.font.SysFont("Verdana", 60)
        exitButton = exitFont.render(" X ", True, (255,0,0), (0,0,0))
        exitRect = exitButton.get_rect()
        exitRect.x = screen_size[0] - exitButton.get_width()
        exitRect.y = 0
        
        font = pygame.font.SysFont("Verdana", 20)
        text = self.planet["temperatureText"]
        
        lineRenders, lineRects = makeMultilineText(text, font)
        
        maxTemp = self.planet["maxTemp"]
        minTemp = self.planet["minTemp"]
        average = (maxTemp + minTemp)/2
        
        highTemperature =average
        lowTemperature = average
        
        #upDiff and downDiff are the amount that the thermometers will change by across the whole transition
        diff = maxTemp - average
        
        font = pygame.font.SysFont("Fixed", 30)
        hotThermometer = font.render("{:.3f}°C".format(highTemperature), True, (255,255,255), (0,0,0,0.1)) 
        coldThermometer = font.render("{:.3f}°C".format(lowTemperature), True, (255,255,255), (0,0,0,0.1)) 
        
        hotRect = hotThermometer.get_rect()
        coldRect = coldThermometer.get_rect()
        
        hotRect.x = screen_size[0] * 2/3
        hotRect.y = screen_size[1] * 3/5
        
        coldRect.x = screen_size[0] * 9/16
        coldRect.y = screen_size[1] * 7/8
        
        countdown = 7
        timePassed = 0
        
        self.screen.blit(background,(0,0))
        
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    if exitRect.collidepoint(pygame.mouse.get_pos()):
                        running = False
            
            self.screen.blit(background,(0,0))

            
            # flip() the display to put your work on screen
            
            if(highTemperature  + (dt/countdown) * diff < maxTemp):
                highTemperature += (dt/countdown) * diff
                lowTemperature -= (dt/countdown) * diff  
            else:
                for i, lineRender in enumerate(lineRenders):
                    self.screen.blit(lineRender, lineRects[i])
            
            hotThermometer = font.render("{:.1f}°C".format(highTemperature), True, (255,255,255), (0,0,0,0.1)) 
            coldThermometer = font.render("{:.1f}°C".format(lowTemperature), True, (255,255,255), (0,0,0,0.1)) 

            self.screen.blit(exitButton, exitRect)
            self.screen.blit(hotThermometer, hotRect)
            self.screen.blit(coldThermometer, coldRect)
            pygame.display.update()
            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(60) / 1000
            timePassed += dt  
            await asyncio.sleep(0) 

    
    
class Clock(Interactable):
    def __init__(self, height, width, image, x, y, screen, planet):
        super().__init__(height, width, image, x, y, screen, planet)
    

    async def interact(self ):
        self.interacted = True  
        
        screen_size = (1280,720)
        clock = pygame.time.Clock()
        running = True
        timePassed = 0
        dt = 0

        dawn = pygame.image.load("assets/"+self.planet["Name"]+"/dawn.png").convert_alpha()
        dawn = pygame.transform.scale(dawn, screen_size)
        
        noon = pygame.image.load("assets/"+self.planet["Name"]+"/noon.png").convert_alpha()
        noon = pygame.transform.scale(noon, screen_size)
        dusk = pygame.image.load("assets/"+self.planet["Name"]+"/dusk.png").convert_alpha()
        dusk = pygame.transform.scale(dusk, screen_size)
        midnight = pygame.image.load("assets/"+self.planet["Name"]+"/midnight.png").convert_alpha()
        midnight = pygame.transform.scale(midnight, screen_size)
        
        
        exitFont = pygame.font.SysFont("Verdana", 60)
        exitButton = exitFont.render(" X ", True, (255,0,0), (0,0,0))
        exitRect = exitButton.get_rect()
        exitRect.x = screen_size[0] - exitButton.get_width()
        exitRect.y = 0
        
        font = pygame.font.SysFont("Verdana", 20)
        text = self.planet["dayText"]
        
        lineRenders, lineRects = makeMultilineText(text, font)
        
        dayLength = self.planet["dayLength"]
        timePassed = 0
        time = 0
        timeChunk = 0
        
        font = pygame.font.SysFont("Fixedsys", 50)
        timer = font.render("{:.3f}°C".format(time), True, (255,255,255), (0,0,0,0.1)) 
        timerRect = timer.get_rect()
        
        timerRect.x = screen_size[0] * 1/2 - timerRect.width/2
        timerRect.y = screen_size[1] * 7/8
        
        #the time, in seconds, before the different day stages repeat
        if self.planet["Name"] == "Mercury":
            repeatTime = 25
        else:
            repeatTime = 20
        dayComplete = False
        noon
        
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    if exitRect.collidepoint(pygame.mouse.get_pos()):
                        running = False
            
            if timePassed % repeatTime < 5:
                self.screen.blit(midnight, (0,0))
            elif timePassed % repeatTime < 10:
                self.screen.blit(dawn, (0,0))
            elif timePassed % repeatTime < repeatTime -5:
                self.screen.blit(noon, (0,0))
            else:
                self.screen.blit(dusk, (0,0))
            
            if time < dayLength:
                time += (dt/repeatTime) * dayLength
            if time > dayLength: 
                time = dayLength
                dayComplete = True
            if time >= timeChunk + dayLength /(repeatTime / 5): # This just avoids having to have extra if statements for my mercury joke
                timeChunk += dayLength /(repeatTime /5)
                

            
            # flip() the display to put your work on screen
            
            for i, lineRender in enumerate(lineRenders):
                self.screen.blit(lineRender, lineRects[i])
            
            timerMessage = ""
            if dayComplete:
                timerMessage += "1 day is "
            timerMessage += "{:.2f} hrs".format(timeChunk)
            #Also give it in days if it's longer than 2 Earth days
            if timeChunk >= 48:
                timerMessage += " = {:.2f} days".format(timeChunk/24)
            if dayComplete:
                " long"
            
            timer = font.render(timerMessage, True, (255,255,255), (0,0,0,0.1))
            timerRect = timer.get_rect()
            timerRect.x = screen_size[0] * 1/2 - timerRect.width/2
            timerRect.y = screen_size[1] * 7/8

            self.screen.blit(exitButton, exitRect)
            self.screen.blit(timer, timerRect)
            pygame.display.update()
            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(60) / 1000
            timePassed += dt   
            await asyncio.sleep(0)
