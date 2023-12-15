import pygame
import random
import math

#Defining Global Variables
SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 800
FPS = 60
BLUE = (0,0,255)

#Pygame Boilerplate (Initialising pygame, setting caption and screen with size.)
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()   ## Sync fps with timer 
pygame.display.set_caption("Golf")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



#Loading files for use
font = pygame.font.Font("C:/Users/clinl/Desktop/Coursework/coursework/gamefont.ttf", 100)
volume_font = pygame.font.Font("C:/Users/clinl/Desktop/Coursework/coursework/gamefont.ttf", 70)
title_surf = font.render('Golf Game', False, (0, 0, 0))
playbtn_surf = font.render('   Play', False, (0, 0, 0))
yakuza_bg = pygame.image.load('C:/Users/clinl/Desktop/Coursework/coursework/yakuza.webp')
menu_bg = pygame.image.load('C:/Users/clinl/Desktop/Coursework/coursework/menu_bg.png')



class ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 10
        self.posX = SCREEN_WIDTH / 2
        self.posY = SCREEN_HEIGHT - self.radius
        self.collided = True
        self.rect = pygame.Rect(self.posX - self.radius, self.posY - self.radius, self.radius * 2, self.radius * 2)

    def ball_path(self, startx, starty, power, ang, time):
        veloX = math.cos(ang) * power
        veloY = math.sin(ang) * power
        
        distX = veloX * time
        distmovedY = (0.5 * (-300) * (time ** 2))
        if distmovedY > (veloY * time):
            print('Falling')
        distY = (veloY * time) + distmovedY  # Add gravity effect


        self.collided = False
        newX = round(startx + distX)
        newY = round(starty - distY)
        return (newX, newY)

    def reset_ball(self):
        self.posX = SCREEN_WIDTH / 2
        self.posY = SCREEN_HEIGHT - self.radius
        

    def findAngle(self, pos):
        X = self.posX
        Y = self.posY
        try:
            angle = math.atan((Y - pos[1]) / (X - pos[0])) #Tan Trig to find angle
        except:
            angle = math.pi / 2 
        if pos[1] < Y and pos[0] > X:
            angle = abs(angle)
        elif pos[1] < Y and pos[0] < X:
            angle = math.pi - angle
        elif pos[1] > Y and pos[0] > X:
            angle = math.pi + abs(angle)
        elif pos[1] > Y and pos[0] > X:
            angle = (math.pi * 2) - angle
        
        return angle

    def getImpactAngle(self, ang, power, wall = False): # Default wall value of false.
        veloX = math.cos(ang) * power
        if wall:
            veloX = -veloX
        veloY = math.sin(ang) * power 
        impact_angle = math.atan2(veloY, veloX)  # Use atan2 to get the correct angle

        return impact_angle
    
    def colissionCheck(self):
        if pygame.sprite.spritecollideany(self, platforms):
            return True
        

    def update(self):
        self.rect = pygame.Rect(self.posX - self.radius, self.posY - self.radius, self.radius * 2, self.radius * 2)
        pygame.draw.circle(screen, (255,255,255), (self.posX, self.posY), self.radius) #White (255,255,255) Outline to circle
        pygame.draw.circle(screen, (0,0,0), (self.posX, self.posY), self.radius - 1) #Main Black (0,0,0) circle body
        pygame.draw.line(screen, (255,255,255), mouse_line[0], mouse_line[1]) #Draws line between mouse and ball.#
        pygame.draw.rect(screen, BLUE, self.rect)
        self.colissionCheck()

class platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.posX = x
        self.posY = y
        self.pWidth = width
        self.pHeight = height
        self.rect = pygame.Rect(self.posX, self.posY, self.pWidth, self.pHeight)
    
    def update(self):
        pygame.draw.rect(screen, BLUE, self.rect)
        
class button(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.clicked = False
        self.rect = pygame.Rect(x, y, width, height)

    def checkclicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
           for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    print('Button being clicked')
                    return True
        else:
            return False
    
    def update(self):
        pygame.draw.rect(screen, self.color, self.rect)
        self.clicked = self.checkclicked()

class imagebutton(button):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.clicked = False
        self.pos = pos
        self.rect = self.image.get_rect(topleft = pos)

        

    def update(self):
        self.clicked = self.checkclicked()
        screen.blit(self.image, self.rect)
             
class goal(pygame.sprite.Sprite):
    def __init__(self, x , y, radius):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

    def win_check(self):
        if pygame.sprite.spritecollideany(self, game_sprites):
            print('Win')

    def update(self):
        pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (0,0,0), (self.x, self.y), self.radius - 1)
        self.win_check()
                
def mutebuttoncheck(sound, sound_volume):
    global muted, image, menu_sound, mutebutton
    if mutebutton.clicked:
            if muted == True:
                image = 'C:/Users/clinl/Desktop/Coursework/coursework/speaker_small.png'
                muted = False
                sound.set_volume(sound_volume)
            else:
                image = 'C:/Users/clinl/Desktop/Coursework/coursework/speaker-off_small.png'
                muted = True
                sound.set_volume(0)
            mutebutton.image = pygame.image.load(image)


#Grouping menu buttons together
main_menu_buttons = pygame.sprite.Group()
playbutton = button((0, 255, 0), 250 , 475, 300, 100)
mutebutton = imagebutton('C:/Users/clinl/Desktop/Coursework/coursework/speaker_small.png', (700, 700))
settingsbutton = imagebutton('C:/Users/clinl/Desktop/Coursework/coursework/settings_small.png', (30, 700))
main_menu_buttons.add(playbutton)
main_menu_buttons.add(mutebutton)
main_menu_buttons.add(settingsbutton)

#Temp while setting up level select
game_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
Ball = ball()
Goal = goal(600, 400, 20)
test_platform = platform(200, 200, 200, 10)
game_sprites.add(Ball)
platforms.add(test_platform)

#Grouping settings buttons and variables together
music_volume = 1
display_volume = int(music_volume * 100)
#sfx_volume = 100
music_volume_surf = volume_font.render('Music Volume: ' + str(display_volume), False, (0, 0, 0))
settings_buttons = pygame.sprite.Group()
backbutton = imagebutton('C:/Users/clinl/Desktop/Coursework/coursework/previous-button_small.png', (700, 30))
volumeupbutton = imagebutton('C:/Users/clinl/Desktop/Coursework/coursework/up_small.png', (550, 600))
volumedownbutton = imagebutton('C:/Users/clinl/Desktop/Coursework/coursework/down_small.png', (550, 700))
settings_buttons.add(backbutton)
settings_buttons.add(mutebutton)
settings_buttons.add(volumedownbutton)
settings_buttons.add(volumeupbutton)

#Defining some key variables to be used in the main loop
click_posX = 0
click_posY = 0
time = 0
power = 0
angle = 0
shoot = False
running = True
menu = True
muted = False
level_select = False
settings = False
first_play = bool(True)
menu_sound = pygame.mixer.Sound("C:/Users/clinl/Desktop/Coursework/coursework/menu.mp3")
game_sound = pygame.mixer.Sound("C:/Users/clinl/Desktop/Coursework/coursework/game.mp3")
settings_sound = pygame.mixer.Sound("C:/Users/clinl/Desktop/Coursework/coursework/settings.mp3")

while running:
    events = pygame.event.get()
    if menu:  
        mutebuttoncheck(menu_sound, music_volume)
        if first_play:
            menu_sound.play(-1)
            first_play = False
        screen.blit(menu_bg, (0,0))
        main_menu_buttons.update()
        screen.blit(title_surf, (250, 200))
        screen.blit(playbtn_surf, playbutton.rect.topleft)
        if playbutton.clicked:
            first_play = True
            menu_sound.stop()
            playbutton.clicked = False
            menu = False
            level_select = True
        if settingsbutton.clicked:
            menu_sound.stop()
            first_play = True
            menu = False
            settings = True           
    elif level_select:
        if first_play:
            game_sound.play(-1)
            first_play = False
        screen.fill((110, 132, 153))
    elif settings:
        if muted:
            settings_sound.set_volume(0 )
        settings_buttons.update()
        mutebuttoncheck(settings_sound, music_volume)
        if first_play:
            settings_sound.play(-1)
            first_play = False
        screen.fill((97, 69, 181))
        screen.blit(music_volume_surf, (20, 650))
        settings_buttons.update()
        if volumeupbutton.clicked:
            if music_volume < 1:    
                music_volume += 0.1
                display_volume = int(music_volume * 100)
        if volumedownbutton.clicked:
            if music_volume >= 0.1:
                music_volume -= 0.1
                display_volume = int(music_volume * 100)
        if not muted:
            settings_sound.set_volume(music_volume)        
        music_volume_surf = volume_font.render('Music Volume: ' + str(display_volume), False, (0, 0, 0)) 
        if backbutton.clicked:
            menu = True
            settings = False
            first_play = True
            settings_sound.stop()
                 
    else:
        mouse_pos = pygame.mouse.get_pos()
        mouse_line = [(Ball.posX, Ball.posY), mouse_pos] #List with ball and mouse positions
        if shoot:
            if Ball.posY <= (SCREEN_HEIGHT - Ball.radius): #Ensures ball is off the ground
                time += 0.05
                po = Ball.ball_path(x,y,power,angle,time)
                Ball.posX = po[0]
                Ball.posY = po[1]
            else:
                Ball.posY = SCREEN_HEIGHT - Ball.radius 
                power *= 0.8  #Simulating energy lost to friction / elastic heat
                if power > 1:
                    x = Ball.posX
                    y = Ball.posY
                    time = 0
                    angle = Ball.getImpactAngle(angle, power)
                    print(angle)
                else:
                    shoot = False
            if Ball.posX >= (SCREEN_HEIGHT - Ball.radius):
                Ball.posX = SCREEN_WIDTH - Ball.radius
                angle = Ball.getImpactAngle(angle, power, True)
                x = Ball.posX
                y = Ball.posY
                time = 0
                power *= 0.8 #Energy lost to wall
            elif Ball.posX <= (0 - Ball.radius):
                Ball.posX = Ball.radius
                angle = Ball.getImpactAngle(angle, power, True)
                x = Ball.posX
                y = Ball.posY
                time = 0
                power *= 0.8 #Energy lost to wall     
        else:         
            for event in events: 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if shoot == False:
                        shoot = True
                        x = Ball.posX
                        y = Ball.posY
                        time = 0
                        power = math.sqrt((mouse_line[1][1] - mouse_line[0][1])**2 + (mouse_line[1][0] - mouse_line[0][0])**2) #Pythagorous Thereom equation
                        angle = Ball.findAngle(pygame.mouse.get_pos()) #Passes in current mouse pos to find angle between it and the ball.
        if Ball.colissionCheck() == True:
            shoot = False
            Ball.reset_ball()       

        screen.blit(yakuza_bg, (0,0))
        test_platform.update()
        game_sprites.update() #updating all game sprites
        Goal.update()
    
        
    for event in events: 
            if event.type == pygame.QUIT: #When user presses the quit button
                running = False #Ends game loop
    pygame.display.flip()   
    clock.tick(FPS) #syncs clock up to game fps


pygame.quit() #Stops code, only reached once game loop has ended.