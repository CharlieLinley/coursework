import pygame
import random
import math

SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 800
FPS = 60
BLUE = (0,0,255)
yakuza_bg = pygame.image.load('C:/Users/Charlie/Desktop/Coursework/coursework/yakuza.webp')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Golf")

class ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 10
        self.posX = SCREEN_WIDTH / 2
        self.posY = SCREEN_HEIGHT - self.radius
        self.collided = True

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
            print('Collided')
            #if velY negative then 

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
        

#grouping sprites for easy updating
game_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
Ball = ball()
test_platform = platform(200, 200, 200, 10)
game_sprites.add(Ball)
platforms.add(test_platform)

click_posX = 0
click_posY = 0
time = 0
power = 0
angle = 0
shoot = False
# bounceCalc = False #Keeps track if a Position has been stored for bounce angle calc.
# checkReady = False #Tracks if ball pos should be checked.


'''Main Game Loop'''
clock = pygame.time.Clock()   ## Sync fps with timer 
running = True
while running:
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
                # angle = Ball.findAngle((prevX, prevY))
                # print('Bounce angle is', angle)
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
            power *= 0.9 #Energy lost to wall
        
        

            
    clock.tick(FPS) #syncs clock up to game fps
    mouse_pos = pygame.mouse.get_pos()
    mouse_line = [(Ball.posX, Ball.posY), mouse_pos] #List with ball and mouse positions
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
                angle = Ball.findAngle(pygame.mouse.get_pos()) #Passes in current mouse pos to find angle between it and the ball.
    #screen.fill(BLUE)
    screen.blit(yakuza_bg, (0,0))
    game_sprites.update() #updating all game sprites
    #platforms.update()
    test_platform.update()
    pygame.display.flip()
        

pygame.quit() #Stops code, only reached once game loop has ended.