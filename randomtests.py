import pygame
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
BLUE = (0, 0, 255)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Golf")

class ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 10
        self.posX = 400
        self.posY = 790
        self.veloX = 0
        self.veloY = 0  # Add initial vertical velocity attribute
        self.shooting = False

    def ball_path(self, startx, starty, power, ang, time):
        veloX = math.cos(ang) * power
        veloY = math.sin(ang) * power

        distX = veloX * time
        distY = (veloY * time) + (0.5 * (9.8) * (time ** 2))  # Add gravity effect

        newX = round(startx + distX)
        newY = round(starty - distY)

        return (newX, newY)

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

    def update(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.posX, self.posY), self.radius)
        pygame.draw.circle(screen, (0, 0, 0), (self.posX, self.posY), self.radius - 1)
        pygame.draw.line(screen, (255, 255, 255), mouse_line[0], mouse_line[1])

game_sprites = pygame.sprite.Group()
Ball = ball()
game_sprites.add(Ball)

click_posX = 0
click_posY = 0
time = 0
power = 0
angle = 0
shoot = False

GROUND_LEVEL = SCREEN_HEIGHT - Ball.radius

'''Main Game Loop'''
clock = pygame.time.Clock()
running = True
while running:
    if Ball.shooting:
        if Ball.posY <= GROUND_LEVEL:
            time += 0.05
            po = Ball.ball_path(x, y, power, angle, time)
            Ball.posX = po[0]
            Ball.posY = po[1]
        else:
            # Reverse the initial vertical velocity for bounce
            Ball.veloY = -Ball.veloY
            Ball.posY = GROUND_LEVEL
    else:
        Ball.shooting = False
        Ball.posY = GROUND_LEVEL
    if Ball.posX > (SCREEN_HEIGHT - Ball.radius):
        Ball.posX = 800
    elif Ball.posX < (0 - Ball.radius):
        Ball.posX = 0
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()
    mouse_line = [(Ball.posX, Ball.posY), mouse_pos]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not Ball.shooting:
                Ball.shooting = True
                x = Ball.posX
                y = Ball.posY
                time = 0
                power = math.sqrt(
                    (mouse_line[1][1] - mouse_line[0][1]) ** 2 + (mouse_line[1][0] - mouse_line[0][0]) ** 2
                )
                angle = Ball.findAngle(pygame.mouse.get_pos())
                Ball.veloY = power * math.sin(angle)  # Store initial vertical velocity
    screen.fill(BLUE)
    game_sprites.update()
    pygame.display.flip()

pygame.quit()
