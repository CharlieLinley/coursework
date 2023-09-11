import pygame
import random
import math

SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 800
FPS = 60
BLUE = (0,0,255)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Golf")

arrow_image = pygame.image.load('C:/Users/Charlie/Desktop/Coursework/coursework/arrow.png').convert_alpha()
arrow_image = pygame.transform.scale(arrow_image, (100,100))
class player_arrow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = arrow_image
        self.clean_image = self.image.copy()
        self.current_angle = 0
        self.rect = self.image.get_rect(center = (600,600))
    
    def center_rotate(self, angle):
        self.current_angle += angle
        if self.current_angle < 0:
            self.current_angle = 0
        elif self.current_angle > 180:
            self.current_angle = 180
        center_loc = self.rect.center #Get center of image before rotation
        rot_sprite = pygame.transform.rotate(self.clean_image, self.current_angle) #Rotating image by given angle.
        self.rect = rot_sprite.get_rect(center = center_loc)
        self.image = rot_sprite
        

    def update(self):
        #Set rect center to ball current center
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.center_rotate(1)
        if keys[pygame.K_DOWN]:
            self.center_rotate(-1)
        screen.blit(self.image, self.rect)

class ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 10
        self.posX = 400
        self.posY = 700
        #self.jumping = False
    
    # def gravity(self):
    #     self.posY += 1
    #     if self.posY > 700:
    #         self.posY = 700
    #         self.jumping = False

    def ball_path(startx, starty, power, ang, time):
        pass

    
    def update(self):
        # keys = pygame.key.get_pressed()
        # for key in keys:
        #    if keys[pygame.K_SPACE] and (not self.jumping):
        #        self.posY -= 100
        #        self.jumping = True
        pygame.draw.circle(screen, (255,255,255), (self.posX, self.posY), self.radius) #White (255,255,255) Outline to circle
        pygame.draw.circle(screen, (0,0,0), (self.posX, self.posY), self.radius - 1) #Main Black (0,0,0) circle body
        pygame.draw.line(screen, (255,255,255), mouse_line[0], mouse_line[1]) #Draws line between mouse and ball.
        #self.gravity()


#grouping sprites for easy updating
game_sprites = pygame.sprite.Group()
Arrow = player_arrow()
Ball = ball()
game_sprites.add(Arrow)
game_sprites.add(Ball)

click_posX = 0
click_posY = 0
time = 0
power = 0
angle = 0
shoot = False


'''Main Game Loop'''
clock = pygame.time.Clock()   ## Sync fps with timer 
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_line = [(Ball.posX, Ball.posY), mouse_pos] #List with ball and mouse positions
    clock.tick(FPS) #syncs clock up to game fps
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #When user presses the quit button
            running = False #Ends game loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            if shoot == False:
                shoot = True
                x = Ball.posX
                y = Ball.posY
                time = 0
                power = math.sqrt((mouse_line[1][1] - mouse_line[0][1])**2 + (mouse_line[1][0] - mouse_line[0][0])**2) #Pythagorous Thereom equation
                print(power)

        screen.fill(BLUE)
        game_sprites.update() #updating all game sprites
        pygame.display.flip()
\

pygame.quit() #Stops code, only reached once game loop has ended.