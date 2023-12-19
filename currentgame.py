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
clock = pygame.time.Clock()   #Sync fps with timer 
pygame.display.set_caption("Golf")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



#Loading files for use
font = pygame.font.Font("D:\keep\Coursework\coursework/gamefont.ttf", 100)
volume_font = pygame.font.Font("D:\keep\Coursework\coursework/gamefont.ttf", 70)
yakuza_bg = pygame.image.load('D:\keep\Coursework\coursework/yakuza.webp')
menu_bg = pygame.image.load('D:\keep\Coursework\coursework/menu_bg.png')



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
        distY = (veloY * time) + distmovedY  # Add gravity effect


        self.collided = False
        newX = round(startx + distX)
        newY = round(starty - distY)
        return (newX, newY)

    def reset_ball(self):
        global shoot
        shoot = True
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
    
    def change_pos(self, pos):
        self.rect = self.image.get_rect(topleft = pos)
        return True

    def update(self):
        self.clicked = self.checkclicked()
        screen.blit(self.image, self.rect)
             
class goal(pygame.sprite.Sprite):
    def __init__(self, x , y, radius):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.sound = pygame.mixer.Sound("D:\keep\Coursework\coursework/win.mp3")
        self.radius = radius
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

    def win_check(self):
        if pygame.sprite.spritecollideany(self, game_sprites):
            self.sound.play()
            return True
        return False

    def update(self):
        pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (0,0,0), (self.x, self.y), self.radius - 1)
        self.win_check()
                
def mutebuttoncheck(sound):
    global muted, image, mutebutton, music_volume
    if mutebutton.clicked:
            if muted == True:
                image = 'D:\keep\Coursework\coursework/speaker_small.png'
                muted = False
                sound.set_volume(music_volume)
            else:
                image = 'D:\keep\Coursework\coursework/speaker-off_small.png'
                muted = True
                sound.set_volume(0)
            mutebutton.image = pygame.image.load(image)
    else:
        if muted:
            sound.set_volume(0)

def ingame_menu_check(events, back_pressed = False):
    if back_pressed:
        return True
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
    return False

def volume_control(sound):
    global music_volume_surf, music_volume, display_volume, muted, volumeupbutton, volumedownbutton
    if volumeupbutton.clicked:
            if music_volume < 1:    
                music_volume += 0.1
                display_volume = int(music_volume * 100)
    if volumedownbutton.clicked:
        if music_volume >= 0.1:
            music_volume -= 0.1
            display_volume = int(music_volume * 100)
    if not muted:
        sound.set_volume(music_volume)        
    music_volume_surf = volume_font.render('Music Volume: ' + str(display_volume), False, (0, 0, 0))
           

#Grouping menu buttons together
main_menu_buttons = pygame.sprite.Group()
title_surf = font.render('Golf Game', False, (0, 0, 0))
playbtn_surf = font.render('   Play', False, (0, 0, 0))
playbutton = button((0, 255, 0), 250, 475, 300, 100)
mutebutton = imagebutton('D:\keep\Coursework\coursework/speaker_small.png', (700, 700))
settingsbutton = imagebutton('D:\keep\Coursework\coursework/settings_small.png', (30, 700))
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
backbutton = imagebutton('D:\keep\Coursework\coursework/previous-button_small.png', (700, 30))
volumeupbutton = imagebutton('D:\keep\Coursework\coursework/up_small.png', (550, 600))
volumedownbutton = imagebutton('D:\keep\Coursework\coursework/down_small.png', (550, 700))
settings_buttons.add(backbutton)
settings_buttons.add(mutebutton)
settings_buttons.add(volumedownbutton)
settings_buttons.add(volumeupbutton)

#Grouping level select buttons and variables together
font_no1 = font.render('1', False, (0,0,0))
font_no2 = font.render('2', False, (0,0,0))
font_no3 = font.render('3', False, (0,0,0))
level_select_buttons = pygame.sprite.Group()
level_one_button = button((255,255,255), 100, 100, 100, 100)
level_two_button = button((255,255,255), 100, 300, 100, 100)
level_three_button = button((255,255,255), 100, 500, 100, 100)
level_select_buttons.add(backbutton)
level_select_buttons.add(level_one_button)
level_select_buttons.add(level_two_button)
level_select_buttons.add(level_three_button)

#Grouping ingame menu buttons and variables
ingame_menu_buttons = pygame.sprite.Group()
quit_button = imagebutton('D:\keep\Coursework\coursework/power-button_small.png', (610, 110))
ingame_menu_buttons.add(mutebutton)
ingame_menu_buttons.add(backbutton)
ingame_menu_buttons.add(volumedownbutton)
ingame_menu_buttons.add(volumeupbutton)
ingame_menu_buttons.add(quit_button)




#Grouping level 1 objects and variables
level_1_group = pygame.sprite.Group()
l1platform1 = platform(200, 200, 200, 20)
l1platform2 = platform(400, 700, 200, 20)
l1platform3 = platform(500, 400, 200, 20)
level_1_group.add(l1platform1)
level_1_group.add(l1platform2)
level_1_group.add(l1platform3)

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
first_play = True
paused = False
win = False
currentlevel = 0

levels = [False, False, False]
menu_sound = pygame.mixer.Sound("D:\keep\Coursework\coursework/menu.mp3")
game_sound = pygame.mixer.Sound("D:\keep\Coursework\coursework/game.mp3")
settings_sound = pygame.mixer.Sound("D:\keep\Coursework\coursework/settings.mp3")

                               

while running:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_line = [(Ball.posX, Ball.posY), mouse_pos] #List with ball and mouse positions
    if menu:
        if first_play:
            x = Ball.posX
            y = Ball.posY
            menu_sound.play(-1)
            first_play = False
            menu_sound.set_volume(music_volume)
        mutebuttoncheck(menu_sound)
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
        screen.fill((110, 132, 153))
        level_select_buttons.update()
        screen.blit(font_no1, (level_one_button.rect.topleft[0] + 30, level_one_button.rect.topleft[1]))
        screen.blit(font_no2, (level_two_button.rect.topleft[0] + 30, level_two_button.rect.topleft[1]))
        screen.blit(font_no3, (level_three_button.rect.topleft[0] + 30, level_three_button.rect.topleft[1]))
        if first_play:
            Ball.reset_ball()
            game_sound.play(-1)
            first_play = False
            game_sound.set_volume(music_volume)
        if level_one_button.clicked or level_two_button.clicked or level_three_button.clicked:   
            if level_one_button.clicked:
                level_one_button.clicked = False
                currentlevel = 1
                levels[currentlevel - 1] = True
                print("Level 1 Starting")
            if level_two_button.clicked:
                level_two_button.clicked = False
                levels[currentlevel - 1] = True
                currentlevel = 2
            if level_three_button.clicked:
                level_three_button.clicked = False
                levels[currentlevel - 1] = True
                currentlevel = 3
            first_play = True
            level_select = False
        mutebuttoncheck(game_sound)
        if backbutton.clicked:
            menu = True
            level_select = False
            first_play = True
            game_sound.stop()
    elif settings:
        settings_buttons.update()
        mutebuttoncheck(settings_sound)
        if first_play:
            settings_sound.play(-1)
            first_play = False
            settings_sound.set_volume(music_volume)
        volume_control(settings_sound)
        screen.fill((97, 69, 181))
        screen.blit(music_volume_surf, (20, 650))
        settings_buttons.update() 
        if backbutton.clicked:
            menu = True
            settings = False
            first_play = True
            settings_sound.stop()
    elif (not paused) and shoot:
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
    for event in events: 
        if event.type == pygame.MOUSEBUTTONDOWN and (not (menu or settings or level_select)):
            if shoot == False:
                shoot = True
                x = Ball.posX
                y = Ball.posY
                time = 0
                power = math.sqrt((mouse_line[1][1] - mouse_line[0][1])**2 + (mouse_line[1][0] - mouse_line[0][0])**2) #Pythagorous Thereom equation
                angle = Ball.findAngle(pygame.mouse.get_pos()) #Passes in current mouse pos to find angle between it and the ball.
    if not (menu or settings or level_select):
        if ingame_menu_check(events) or backbutton.clicked:
            if backbutton.clicked or paused:
                backbutton.clicked = False
                paused = False
                levels[currentlevel - 1] = True #Explained below
            else:
                mutebutton.change_pos((600, 600))
                backbutton.change_pos((110, 110))
                volumedownbutton.change_pos((volumedownbutton.pos[0] + 60, volumedownbutton.pos[1] - 250))
                volumeupbutton.change_pos((volumeupbutton.pos[0] + 60, volumeupbutton.pos[1] - 250))
                paused = True            
        if paused:
            levels[currentlevel - 1] = False #List is zero indexed, but I wanted to use the actual level number so I have to minus one to get the index.
            pygame.draw.rect(screen, "grey", (100, 100, 600, 600))
            volume_control(game_sound)
            screen.blit(music_volume_surf, (110, 400))
            ingame_menu_buttons.update()
            mutebuttoncheck(game_sound)
        if win:
            pygame.draw.rect(screen, "grey", (100, 100, 600, 600))
        if quit_button.clicked:
            quit_button.clicked = False
            mutebutton.change_pos((700, 700))
            backbutton.change_pos((700, 30))
            volumedownbutton.change_pos((volumedownbutton.pos[0] - 60, volumedownbutton.pos[1] + 250))
            volumeupbutton.change_pos((volumedownbutton.pos[0] - 60, volumedownbutton.pos[1] + 250))
            first_play = True
            menu = True
            currentlevel = 0
            game_sound.stop()
            paused = False       
        if currentlevel == 1 and levels[currentlevel - 1]:
            screen.blit(yakuza_bg, (0,0))
            test_platform.update()
            game_sprites.update() #updating all game sprites
            Goal.update()
            if Goal.win_check():
                levels[currentlevel - 1] = False
                win = True
        elif currentlevel == 2 and levels[currentlevel - 1]:
            pass
        elif currentlevel == 3 and levels[currentlevel - 1]:
            pass    
    for event in events: 
            if event.type == pygame.QUIT: #When user presses the quit button
                running = False #Ends game loop
    if Ball.colissionCheck() == True:
        Ball.reset_ball()
    pygame.display.flip()   
    clock.tick(FPS) #syncs clock up to game fps


pygame.quit() #Stops code, only reached once game loop has ended.