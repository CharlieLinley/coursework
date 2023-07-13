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
        self.image = pygame.image.load("C:/Users/Charlie/Desktop/School/Coursework/latest/arrow.png").convert_alpha() #Full path (//CFBS-SVR-FILE1/PupilsData/2017/Linleyc/RedirectedProfileFolders/Desktop/Game Files/)
        self.clean_image = self.image.copy()
        self.rect = self.image.get_rect(center = (400,400))
        self.current_angle = 0
    

    def center_rotate(self, angle):
        self.current_angle += angle
        print(self.current_angle)
        if self.current_angle < 0:
            self.current_angle = 0
        elif self.current_angle > 180:
            self.current_angle = 180
        center_loc = self.rect.center #Get center of image before rotation
        print(center_loc)
        rot_sprite = pygame.transform.rotate(self.clean_image, self.current_angle) #Rotating image by given angle.
        self.rect = rot_sprite.get_rect(center = center_loc)
        self.image = rot_sprite
    
    def player_controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            print('Up')
            self.center_rotate(5)
        if keys[pygame.K_DOWN]:
            print('Down')
            self.center_rotate(-5)

    def update(self):
        self.player_controls()


#grouping sprites for easy updating
game_sprites = pygame.sprite.Group()
Arrow = player_arrow()
game_sprites.add(Arrow)

def main_game():
    clock = pygame.time.Clock()   ## Sync fps with timer 
    running = True
    while running:
        clock.tick(FPS) #syncs clock up to game fps
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #When user presses the quit button
                running = False #Ends game loop
        game_sprites.update() #updating all game sprites
        screen.fill(BLUE)
        game_sprites.draw(screen)
        pygame.display.flip()

main_game()


pygame.quit() #Stops code, only reached once game loop has ended.