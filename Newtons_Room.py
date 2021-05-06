import pygame
import random

class Physics_object:
    def __init__(self, mass, loc):
        self.yAccel = .98
        self.yVel = 0
        self.xAccel = 0
        self.xVel = 0
        self.x = loc[0]
        self.y = loc[1]
        self.mass = mass


class Vector:
    def __init__(self, loc_origin, loc_out):
        self.origin = loc_origin
        self.end = loc_out
        if abs(self.origin[0] - self.end[0]) > 130:
            if self.end[0]>self.origin[0]:
                self.end[0] = self.origin[0] + 130
            else:
                self.end[0] = self.origin[0] - 130
        
        if abs(self.origin[1] - self.end[1]) > 130:
            if self.end[1]>self.origin[1]:
                self.end[1] = self.origin[1] + 130
            else:
                self.end[1] = self.origin[1] - 130
        
        self.xVec = self.end[0] - self.origin[0]
        self.yVec = self.end[1] - self.origin[1]
        
        
        
    def draw(self):
        pygame.draw.line(win, (180, 40, 20), self.origin, self.end)
        


class playerBall:
    def __init__(self, loc, radius):
        self.loc = loc
        self.radius = radius
        self.mass = (radius**3)
        self.vel = [0,0]
        self.accel = [0,0]

    def set_accel(self,vectors):
        self.accel = [0,0]
        for vec in vectors:
            self.accel[0]+=vec.xVec/self.mass*1.5
            self.accel[1]+=vec.yVec/self.mass*1.5
    
    def set_vel(self, vectors):
        self.vel = [0,0]
        for vec in vectors:
            self.vel[0]+=vec.xVec/self.mass*1.5
            self.vel[1]+=vec.yVec/self.mass*1.5
    
    
    def update(self):
        self.vel = [self.vel[0]+self.accel[0], self.vel[1]+self.accel[1]]
        self.loc = [self.vel[0]+self.loc[0], self.vel[1]+self.loc[1]]
        
    def draw(self):
        pygame.draw.circle(win, (95, 115, 220), self.loc, self.radius)
        # pygame.display.update()
        
class playerTarget:
    def __init__(self, loc):
        self.loc = loc
        self.radius = 30
        
    def draw(self):
        pygame.draw.circle(win, (11, 93, 12), self.loc, self.radius)
        
    def detectVictiory(self, playerLoc):
        dist = ((self.loc[0]-playerLoc[0])**2 + (self.loc[1]-playerLoc[1])**2)**0.5
        
        return dist<25
        



    
    

def level1(playerLoc, targetLoc): #Normal levels. Player makes forces, ball moves way it's supposed.
    
    run = True #Keeps the game running
    
    prev_space_state = False
    prev_click_state = False
    forceArrows = [Vector(playerLoc, playerLoc),Vector(playerLoc, playerLoc)]
    player = playerBall(playerLoc, 20)
    
    forceIndex = 0
    goal = playerTarget(targetLoc)

    movestate = False
    while run:
        win.fill((220, 220, 220)) #resets background
        # Current_click_state = pygame.mouse.get_pressed() #Checks mouse input
        
        key_states = pygame.key.get_pressed() #Detects key presses
        
        player.draw() #Draws player ball
        goal.draw()
            
        if not movestate: #Still state code
            
            for arrow in forceArrows:
                arrow.draw()
                
            if(pygame.mouse.get_pressed()[0]):
                if not prev_click_state:
                    prev_click_state = True
                    if forceIndex == 1:
                        forceArrows[1] = Vector(player.loc, [player.loc[0],pygame.mouse.get_pos()[1]])
                    else:
                        forceArrows[0] = Vector(player.loc, [pygame.mouse.get_pos()[0], player.loc[1]])
                    
            else:
                prev_click_state = False
                
        else: #Move state
            player.update()
            if goal.detectVictiory(player.loc): #Ends the game if you press escape
                run = False



        #Code that runs regardless of state
        
        if key_states[pygame.K_SPACE]: #changes move state upon space press
            if not prev_space_state:
                movestate = not movestate
                if not movestate: 
                    #Resets if going from move to still state
                    player = playerBall(playerLoc.copy(), 20)
                    forceArrows = [Vector(playerLoc, playerLoc),Vector(playerLoc, playerLoc)]
                else:
                    player.set_accel(forceArrows)
                
                prev_space_state = True
        else:
            prev_space_state = False
            
        
        if key_states[pygame.K_UP] or key_states[pygame.K_DOWN]:
            forceIndex = 1
            
        elif key_states[pygame.K_RIGHT] or key_states[pygame.K_LEFT]:
            forceIndex = 0
        
        
        
        
        if key_states[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            
        pygame.event.pump()
        pygame.display.update()
        

def predictionLevel(playerLoc):
    
    run = True #Keeps the game running
    prev_space_state = False
    prev_click_state = False
    forceArrows = [Vector(playerLoc,[random.randint(playerLoc[0]-200, playerLoc[0]+200), playerLoc[1]]),Vector(playerLoc,[playerLoc[0],random.randint(playerLoc[1]-200, playerLoc[1]+200)])]
    player = playerBall(playerLoc, 20)
    
    goal = playerTarget([0,0])

    movestate = False
    while run:
        win.fill((220, 220, 220)) #resets background
        # Current_click_state = pygame.mouse.get_pressed() #Checks mouse input
        
        key_states = pygame.key.get_pressed() #Detects key presses
        
        player.draw() #Draws player ball
        goal.draw()
            
        if not movestate: #Still state code
            
            for arrow in forceArrows:
                arrow.draw()
                
            if(pygame.mouse.get_pressed()[0]):
                if not prev_click_state:
                    prev_click_state = True
                    goal = playerTarget(pygame.mouse.get_pos())
                    
            else:
                prev_click_state = False
                
        else: #Move state
            player.update()
            if goal.detectVictiory(player.loc): #Ends the game if you press escape
                run = False



        #Code that runs regardless of state
        
        if key_states[pygame.K_SPACE]: #changes move state upon space press
            if not prev_space_state:
                movestate = not movestate
                if not movestate: 
                    #Resets if going from move to still state
                    player = playerBall(playerLoc.copy(), 20)
                    forceArrows = [Vector(playerLoc,[random.randint(playerLoc[0]-200, playerLoc[0]+200), playerLoc[1]]),Vector(playerLoc,[playerLoc[0],random.randint(playerLoc[1]-200, playerLoc[1]+200)])]
                else:
                    player.set_accel(forceArrows)
                
                prev_space_state = True
        else:
            prev_space_state = False
        
        
        if key_states[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            
        pygame.event.pump()
        pygame.display.update()
    
if __name__ == '__main__':  # Runner
    pygame.init()
    windowWidth = 900
    windowHeight = 700
    win = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption("Get the blue sphere to the green sphere!")
    level1([300,650], [300,100])
    
    pygame.display.set_caption("Don't worry, it gets more complex from here.")
    level1([150,650], [700,100])
    
    pygame.display.set_caption("Can you predict the trajectory?")
    predictionLevel([450,350])
    
    
    
    pygame.quit()