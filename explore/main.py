# Example file showing a circle moving on screen
import pygame
from sprites import Telescope, Hammer, Thermometer, Clock, Player
import json
import asyncio
# pygame setup

# planets = {
#     "Earth" : {"Name": "Earth", "featherSpeed" : 100, "hammerSpeed" : 400, "maxTemp" : 57.2, "minTemp": -89.2, "dayLength" : 24,
#                "skyText": """
#         The Earth has one moon, just called The Moon.
#         creative...
#         The moon can only be seen from light reflecting off the Sun at us.
#         As the Moon's position changes, the way it looks changes.
#         The main stages are the new moon, crescent moon,
#         half moon, gibbon moon and full moon, going from nearly invisible to fully visible
         
#         There's also last of the sunset at the bottom, making different 
#         colours because of how theEarth's atmosphere scatters the light.""",
        
#         "gravityText": """Hammer time!
#         Gravity accelerates everything at the same rate.
#         So with no atmosphere to slow things down, the hammer and feather
#         would fall at the same speed.
#         But because the hammer is denser than the feather, it's affected by 
#         air resistance less than the feather, so hits the ground earlier""",
#         "TemperatureText": """Nice and mild.
#         The highest temperature on Earth recordeed was 57.2C, 
#         and the lowest temperature recorder was -89.2C.
#         Compared to other planets, this is very mild, 
#         and part of why Earth is said to be in the 
#         "Goldilocks zone" of the solar system.
#         Not too hot, or too cold!""",
        
#         "temperatureText": """Nice and mild.
#         The highest temperature on Earth recordeed was 57.2°C, 
#         and the lowest temperature recorder was -89.2°C.
#         Compared to other planets, this is very mild, 
#         and part of why Earth is said to be in the 
#         "Goldilocks zone" of the solar system.
#         Not too hot, or too cold!""",
        
#         "dayText": """Yeah, there's 24 hours in a day,
#         this is far more interesting for the other planets.
#         A day is the amount of time it takes for a planet to rotate
#         about its axis. And a year is the amount of time that it takes for a 
#         planet to rotate around the sun. A year is actually 365.24 days long.
#         That's why we have leap years,so that the calendar can catch up again."""},
#     "Mercury" : {"Name": "Mercury", "featherSpeed" : 133, "hammerSpeed" : 133, "maxTemp" : 420, "minTemp": -170, "dayLength": 176 * 24,
#                  "skyText" : """Ah. It's a bit big, innit?
#                  Mercury's too small to have anything around it, being less than 
#                  1.5x the size of our moon.
#                  You'll notice the sky is still black, even with the Sun out.
#                  That's because Mercury basically has no atmosphere, so there 
#                  is no air to scatter the light and make a sky.""",
                 
#                  "gravityText": """Here, the gravity is a lot weaker at about 3.7 m/s^2
#                  so both of the objects fall slower. However, Mercury has almost no
#                  atmosphere, so there is no air resistance to slow down the feather.
#                  That means they fall together, and slowly.""",
                  
#                  "temperatureText": """Mercury's temperatures vary massively, because
#                  it's so close to the Sun, It can heat up 420°C during its long days.
#                  But because it has no atmosphere to hold heat in,
#                  the temperature can plummet to -170°C when its out of the sun.
#                  It's like an extreme version of the deserts on Earth.""",
                 
#                  "dayText" : """Mercury's days are extremely long. In fact, 
#                  they are longer than a year on Mercury!
#                  A Mercury day takes 176 Earth days to complete.
#                  A year on Mercury is only 88 days, so a day on Mercury takes
#                  nearly twice as long!
                 
#                  Also, Mercury has a very elliptical orbit, meaning it orbits in
#                  an oval around the Sun.
#                  This means that when Mercury is close to the Sun, 
#                  it can actually stop or move slighly backward across the sky ,like a less 
#                  extreme version of noon going on for double the time here."""
#                  }
# }# this name thing is dumb, but i only pass the inner dictionary in to the interactables and I need the name there

# with open("planets.json", "w") as outfile:
#     json.dump(planets,outfile)
   
with open("planets.json", "r") as infile: 
    planets = json.load(infile)


#TODO, change this to read from a file or something
chosenPlanet = planets["Earth"]

pygame.init()
screen_size = (1280,720)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True
dt = 0


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
background = pygame.image.load("assets/"+chosenPlanet["Name"]+"/background.png").convert_alpha()
background = pygame.transform.scale(background, screen_size)
playerImage = pygame.image.load("assets/joestronaut.png").convert_alpha()
#playerImage = pygame.transform.scale(player,[80,80])

allSprites = pygame.sprite.Group()

playerGroup = pygame.sprite.Group()
player = Player(80,80, playerImage, player_pos.x, player_pos.y, screen, 400)
player.add(playerGroup,allSprites)
screen.blit(background,(0,0))
#screen.blit(player, player_pos)

interactables = pygame.sprite.Group()
telescopeImage = pygame.image.load("assets/telescope.png").convert_alpha()
telescope = Telescope(70,90,telescopeImage, 600, 500, screen, chosenPlanet)
interactables.add(telescope)

hammerImage = pygame.image.load("assets/hammer.png").convert_alpha()
hammer = Hammer(60,60,hammerImage, 1000, 200, screen, chosenPlanet)
interactables.add(hammer)

thermometerImage = pygame.image.load("assets/hotThermometer.png").convert_alpha()
thermometer = Thermometer(50,70,thermometerImage,1000,600,screen,chosenPlanet)
interactables.add(thermometer)

clockImage = pygame.image.load("assets/clock.png").convert_alpha()
clockTimer = Clock(60,60,clockImage,300,300,screen,chosenPlanet)
interactables.add(clockTimer)

font = pygame.font.SysFont("Verdana", 30)
exit = font.render("EXIT", True, (255,0,0), None)
exitRect = exit.get_rect()
exitRect.x = screen_size[0]/2
exitRect.y = screen_size[1] -50


async def main():
    global screen, clock, dt, running, player, interactables, hammer, telescope, clock, thermometer
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.blit(background,(0,0))
        screen.blit(exit,exitRect)
        

        keys = pygame.key.get_pressed()
        
        if player.rect.x > screen_size[0] - player.width:
            player.rect.x = screen_size[0] - player.width
        elif player.rect.x < 0:
            player.rect.x = 0
        if player.rect.y > screen_size[1] - player.height:
            player.rect.y = screen_size[1] - player.height
        elif player.rect.y < 0:
            player.rect.y = 0
        
        
        # make sure you are actually able to have a spot where you only interact with one interactable. I did have it exclusive before, but then there's the issue of not being able to redo experiments, even though you can close out of them whenever 
        if(keys[pygame.K_SPACE]): 
            if(exitRect.colliderect(player.rect)):
                running = False
            collidingSprites = pygame.sprite.spritecollide(player, interactables, False)
            if collidingSprites != None and len(collidingSprites) > 0:
                await collidingSprites[0].interact()
        
        # flip() the display to put your work on screen
        interactables.draw(screen)
        playerGroup.update(keys, dt)
        playerGroup.draw(screen)
        pygame.display.update()
        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
        await asyncio.sleep(0)

    pygame.quit()
asyncio.run(main())