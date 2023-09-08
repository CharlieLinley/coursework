import pygame
import random

SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 800
FPS = 60
BLUE = (0,0,255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Golf")

class player_arrow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('C:/Users/Charlie/Desktop/Coursework/coursework/arrow.png').convert_alpha()
        self.clean_image = self.image.copy()
        self.current_angle = 0
        self.rect = self.image.get_rect(center = (400,400))
    
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
        self.posX = 400
        self.posY = 700
        self.jumping = False
        self.image = pygame.image.load("C:/Users/Charlie/Desktop/Coursework/coursework/ball.png")
    
    def gravity(self):
        self.posY += 1
        if self.posY > 700:
            self.posY = 700
            self.jumping = False
    
    def update(self):
        keys = pygame.key.get_pressed()
        for key in keys:
           if keys[pygame.K_SPACE] and (not self.jumping):
               self.posY -= 100
               self.jumping = True
        screen.blit(self.image, (self.posX, self.posY))
        self.gravity()


#grouping sprites for easy updating
game_sprites = pygame.sprite.Group()
Arrow = player_arrow()
Ball = ball()
game_sprites.add(Arrow)
game_sprites.add(Ball)

def main_game():
    clock = pygame.time.Clock()   ## Sync fps with timer 
    running = True
    while running:
        clock.tick(FPS) #syncs clock up to game fps
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #When user presses the quit button
                running = False #Ends game loop
        screen.fill(BLUE)
        game_sprites.update() #updating all game sprites
        pygame.display.flip()

main_game()


pygame.quit() #Stops code, only reached once game loop has ended.