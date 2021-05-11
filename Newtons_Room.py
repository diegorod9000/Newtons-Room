import pygame
import random
import time



def distBetween(loc1,loc2):
    xDist = (loc1[0] - loc2[0])**2
    yDist = (loc1[1] - loc2[1])**2
    return (xDist + yDist)**0.5

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
        
    def draw_blue(self):
        pygame.draw.line(win, (20, 40, 180), self.origin, self.end)
        

class Surface:
    def __init__(self, loc_origin, loc_out, fric = 0):
        self.origin = loc_origin
        self.end = loc_out
        if self.end[0] < self.origin[0]:
            temp = self.end.copy()
            self.end = self.origin
            self.origin = temp
        self.fric = fric
    
    def draw(self):
        pygame.draw.line(win, (90, 40, 20), self.origin, self.end)
        
    def detectCollision_horizontal(self, player):
        if not (player.loc[0] < self.end[0] and player.loc[0] > self.end[1]):
            return False
        playerYMax = player.loc[1] + player.radius
        playerYMin = player.loc[1] - player.radius
        if playerYMax > self.end[1] and playerYMin < self.end[1]:
            player.loc[1] = self.end[1] - player.radius
    
    def friction(self, player):
        pass
            
    

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
    
    def add_accel(self, vec):
        self.accel[0]+=vec.xVec/self.mass*1.5
        self.accel[1]+=vec.yVec/self.mass*1.5
        
    def set_vel(self, vectors):
        self.vel = [0,0]
        for vec in vectors:
            self.vel[0]+=vec.xVec/self.mass* 100
            self.vel[1]+=vec.yVec/self.mass* 100
    
    
    def update(self):
        self.vel = [self.vel[0]+self.accel[0], self.vel[1]+self.accel[1]]
        self.loc = [self.vel[0]+self.loc[0], self.vel[1]+self.loc[1]]
        
    def draw(self):
        pygame.draw.circle(win, (95, 115, 220), self.loc, self.radius)
        # pygame.display.update()
        
class playerTarget:
    def __init__(self, loc, radius = 30):
        self.loc = loc
        self.radius = radius
        
    def draw(self):
        pygame.draw.circle(win, (11, 93, 12), self.loc, self.radius)
        
    def detectVictiory(self, playerLoc):
        dist = ((self.loc[0]-playerLoc[0])**2 + (self.loc[1]-playerLoc[1])**2)**0.5
        
        return dist<30
    
    def detectVictiory_big(self, playerLoc):
        dist = ((self.loc[0]-playerLoc[0])**2 + (self.loc[1]-playerLoc[1])**2)**0.5
        
        return dist<45
        



    
    
levelIndex = 0
def zeroGravity(playerLoc, targetLoc): #Normal levels. Player makes forces, ball moves way it's supposed.
    
    run = True #Keeps the game running
    
    prev_space_state = False
    prev_click_state = False
    forceArrows = [Vector(playerLoc, playerLoc),Vector(playerLoc, playerLoc)]
    player = playerBall(playerLoc, 20)
    
    forceIndex = 0
    goal = playerTarget(targetLoc)

    movestate = False
    pygame.event.pump()
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
                return True



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
        
        if key_states[pygame.K_a]:
            return False
            
        if key_states[pygame.K_d]:
            return True
        
        
        if key_states[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            
        pygame.event.pump()
        pygame.display.update()
    return True
        

def predictionLevel(playerLoc):
    
    run = True #Keeps the game running
    prev_space_state = False
    prev_click_state = False
    forceArrows = [Vector(playerLoc,[random.randint(playerLoc[0]-200, playerLoc[0]+200), playerLoc[1]]),Vector(playerLoc,[playerLoc[0],random.randint(playerLoc[1]-200, playerLoc[1]+200)])]
    player = playerBall(playerLoc, 20)
    
    goal = playerTarget([-30,-30])

    movestate = False
    pygame.event.pump()
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
                    if distBetween(playerLoc, pygame.mouse.get_pos()) >200:
                        goal = playerTarget(pygame.mouse.get_pos())
                    
            else:
                prev_click_state = False
                
        else: #Move state
            player.update()
            if goal.detectVictiory(player.loc): #Ends the game if you press escape
                run = False
                return True



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
        
        
        if key_states[pygame.K_a]:
            return False
            
        if key_states[pygame.K_d]:
            return True
        
        if key_states[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            
        pygame.event.pump()
        pygame.display.update()
    return True

def predictionLevel_hard(playerLoc, numArrows):
    
    run = True #Keeps the game running
    prev_space_state = False
    prev_click_state = False
    forceArrows = []
    for i in range(numArrows):
        forceArrows.append(Vector(playerLoc, [random.randint(playerLoc[0]-200, playerLoc[0]+200),random.randint(playerLoc[1]-200, playerLoc[1]+200)]))
    player = playerBall(playerLoc, 20)
    
    goal = playerTarget([-30,-30])

    movestate = False
    pygame.event.pump()
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
                    if distBetween(playerLoc, pygame.mouse.get_pos()) >250:
                        goal = playerTarget(pygame.mouse.get_pos())
                    
            else:
                prev_click_state = False
                
        else: #Move state
            player.update()
            if goal.detectVictiory(player.loc): #Ends the game if you press escape
                run = False
                return True



        #Code that runs regardless of state
        
        if key_states[pygame.K_SPACE]: #changes move state upon space press
            if not prev_space_state:
                movestate = not movestate
                if not movestate: 
                    #Resets if going from move to still state
                    player = playerBall(playerLoc.copy(), 20)
                    forceArrows = []
                    for i in range(numArrows):
                        forceArrows.append(Vector(playerLoc, [random.randint(playerLoc[0]-200, playerLoc[0]+200),random.randint(playerLoc[1]-200, playerLoc[1]+200)]))
                else:
                    player.set_accel(forceArrows)
                
                prev_space_state = True
        else:
            prev_space_state = False
        
        
        if key_states[pygame.K_a]:
            return False
            
        if key_states[pygame.K_d]:
            return True
        
        if key_states[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            
        pygame.event.pump()
        pygame.display.update()
    return True


def gravitySurvival():
    run = True #Keeps the game running
    playerLoc = [450,350]
    prev_space_state = False
    prev_click_state = False
    forceArrows = [Vector(playerLoc, playerLoc),Vector(playerLoc, playerLoc), Vector(playerLoc, [playerLoc[0], playerLoc[1] + 80])]
    player = playerBall(playerLoc, 20)
    survivalTime = 0
    forceIndex = 0

    movestate = False
    pygame.event.pump()
    while run:
        win.fill((220, 220, 220)) #resets background
        # Current_click_state = pygame.mouse.get_pressed() #Checks mouse input
        
        key_states = pygame.key.get_pressed() #Detects key presses
        
        player.draw() #Draws player ball
            
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
            survivalTime +=1
            if survivalTime==500:
                return True
            if player.loc[1]<10 or player.loc[1]>690 or player.loc[0]<10 or player.loc[0]>890:
                player = playerBall(playerLoc.copy(), 20)
                forceArrows = [Vector(playerLoc, playerLoc),Vector(playerLoc, playerLoc), Vector(playerLoc, [playerLoc[0], playerLoc[1] + 100])]
                survivalTime = 0
                movestate = False
                


        #Code that runs regardless of state
        
        if key_states[pygame.K_SPACE]: #changes move state upon space press
            if not prev_space_state:
                movestate = not movestate
                if not movestate: 
                    #Resets if going from move to still state
                    player = playerBall(playerLoc.copy(), 20)
                    forceArrows = [Vector(playerLoc, playerLoc),Vector(playerLoc, playerLoc), Vector(playerLoc, [playerLoc[0], playerLoc[1] + 100])]
                    survivalTime = 0
                else:
                    player.set_accel(forceArrows)
                
                prev_space_state = True
        else:
            prev_space_state = False
            
        
        if key_states[pygame.K_UP] or key_states[pygame.K_DOWN]:
            forceIndex = 1
            
        elif key_states[pygame.K_RIGHT] or key_states[pygame.K_LEFT]:
            forceIndex = 0
        
        if key_states[pygame.K_a]:
            return False
            
        if key_states[pygame.K_d]:
            return True
        
        
        if key_states[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            
        pygame.event.pump()
        pygame.display.update()
    return True

def target_Gravity(playerLoc, targetLoc):
    run = True #Keeps the game running
    
    prev_space_state = False
    prev_click_state = False
    forceArrows = [Vector(playerLoc, playerLoc),Vector(playerLoc, playerLoc), Vector(playerLoc, [playerLoc[0], playerLoc[1] + 80])]
    player = playerBall(playerLoc, 20)
    
    forceIndex = 0
    goal = playerTarget(targetLoc, 45)

    movestate = False
    pygame.event.pump()
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
            if goal.detectVictiory_big(player.loc): #Ends the game if you press escape
                run = False
                return True



        #Code that runs regardless of state
        
        if key_states[pygame.K_SPACE]: #changes move state upon space press
            if not prev_space_state:
                movestate = not movestate
                if not movestate: 
                    #Resets if going from move to still state
                    player = playerBall(playerLoc.copy(), 20)
                    forceArrows = [Vector(playerLoc, playerLoc),Vector(playerLoc, playerLoc), Vector(playerLoc, [playerLoc[0], playerLoc[1] + 80])]
                else:
                    player.set_accel(forceArrows)
                
                prev_space_state = True
        else:
            prev_space_state = False
            
        
        if key_states[pygame.K_UP] or key_states[pygame.K_DOWN]:
            forceIndex = 1
            
        elif key_states[pygame.K_RIGHT] or key_states[pygame.K_LEFT]:
            forceIndex = 0
        
        if key_states[pygame.K_a]:
            return False
            
        if key_states[pygame.K_d]:
            return True
        
        
        if key_states[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            
        pygame.event.pump()
        pygame.display.update()
    return True
    
def predictionLevel_Gravity(playerLoc, numArrows):
    
    run = True #Keeps the game running
    prev_space_state = False
    prev_click_state = False
    forceArrows = [Vector(playerLoc, [playerLoc[0], playerLoc[1] + 80])]
    for i in range(numArrows):
        forceArrows.append(Vector(playerLoc, [random.randint(playerLoc[0]-200, playerLoc[0]+200),random.randint(playerLoc[1]-200, playerLoc[1]+200)]))
    player = playerBall(playerLoc, 20)
    
    goal = playerTarget([-30,-30])

    movestate = False
    pygame.event.pump()
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
                    if distBetween(playerLoc, pygame.mouse.get_pos()) >250:
                        goal = playerTarget(pygame.mouse.get_pos())
                    
            else:
                prev_click_state = False
                
        else: #Move state
            player.update()
            if goal.detectVictiory(player.loc): #Ends the game if you press escape
                run = False
                return True



        #Code that runs regardless of state
        
        if key_states[pygame.K_SPACE]: #changes move state upon space press
            if not prev_space_state:
                movestate = not movestate
                if not movestate: 
                    #Resets if going from move to still state
                    player = playerBall(playerLoc.copy(), 20)
                    forceArrows = [Vector(playerLoc, [playerLoc[0], playerLoc[1] + 80])]
                    for i in range(numArrows):
                        forceArrows.append(Vector(playerLoc, [random.randint(playerLoc[0]-200, playerLoc[0]+200),random.randint(playerLoc[1]-200, playerLoc[1]+200)]))
                else:
                    player.set_accel(forceArrows)
                
                prev_space_state = True
        else:
            prev_space_state = False
        
        
        if key_states[pygame.K_a]:
            return False
            
        if key_states[pygame.K_d]:
            return True
        
        if key_states[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            
        pygame.event.pump()
        pygame.display.update()
    return True

def target_Momentum(playerLoc, targetLoc):
    run = True #Keeps the game running
    
    prev_space_state = False
    prev_click_state = False
    forceArrows = [Vector(playerLoc, [playerLoc[0], playerLoc[1] + 80])]
    momentumArrows = [Vector(playerLoc, playerLoc),Vector(playerLoc, playerLoc)]
    player = playerBall(playerLoc, 20)
    
    arrowIndex = 0
    goal = playerTarget(targetLoc, 45)

    movestate = False
    pygame.event.pump()
    while run:
        win.fill((220, 220, 220)) #resets background
        # Current_click_state = pygame.mouse.get_pressed() #Checks mouse input
        
        key_states = pygame.key.get_pressed() #Detects key presses
        
        player.draw() #Draws player ball
        goal.draw()
            
        if not movestate: #Still state code
            
            for arrow in forceArrows:
                arrow.draw()
            for arrow in momentumArrows:
                arrow.draw_blue()
                
            if(pygame.mouse.get_pressed()[0]):
                if not prev_click_state:
                    prev_click_state = True
                    if arrowIndex == 1:
                        momentumArrows[1] = Vector(player.loc, [player.loc[0],pygame.mouse.get_pos()[1]])
                    else:
                        momentumArrows[0] = Vector(player.loc, [pygame.mouse.get_pos()[0], player.loc[1]])
                    
            else:
                prev_click_state = False
                
        else: #Move state
            player.update()
            if goal.detectVictiory_big(player.loc): #Ends the game if you press escape
                run = False
                return True



        #Code that runs regardless of state
        
        if key_states[pygame.K_SPACE]: #changes move state upon space press
            if not prev_space_state:
                movestate = not movestate
                if not movestate: 
                    #Resets if going from move to still state
                    player = playerBall(playerLoc.copy(), 20)
                    forceArrows = [Vector(playerLoc, [playerLoc[0], playerLoc[1] + 80])]
                    momentumArrows = [Vector(playerLoc, playerLoc),Vector(playerLoc, playerLoc)]
                else:
                    player.set_accel(forceArrows)
                    player.set_vel(momentumArrows)
                
                prev_space_state = True
        else:
            prev_space_state = False
            
        
        if key_states[pygame.K_UP] or key_states[pygame.K_DOWN]:
            arrowIndex = 1
            
        elif key_states[pygame.K_RIGHT] or key_states[pygame.K_LEFT]:
            arrowIndex = 0
        
        if key_states[pygame.K_a]:
            return False
            
        if key_states[pygame.K_d]:
            return True
        
        
        if key_states[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            
        pygame.event.pump()
        pygame.display.update()
    return True
    
if __name__ == '__main__':  # Runner
    pygame.init()
    windowWidth = 900
    windowHeight = 700
    win = pygame.display.set_mode((windowWidth, windowHeight))
    levelIndex = 0
    while(levelIndex<50):
        if levelIndex == 0:
            pygame.display.set_caption("Get the blue sphere to the green sphere!")
            if zeroGravity([300,650], [300,100]):
                levelIndex+=1
        
        elif levelIndex == 1:
            pygame.display.set_caption("Easy peasy.")
            if zeroGravity([150,450], [700,450]):
                levelIndex+=1
            else:
                levelIndex-=1
            
        elif levelIndex == 2:
            pygame.display.set_caption("2 Arrows!")
            if zeroGravity([175,550], [350,250]):
                levelIndex+=1
            else:
                levelIndex-=1
        elif levelIndex == 3:
            pygame.display.set_caption("I think you're getting the hang of this")
            if zeroGravity([800,650],[122, 79]):
                levelIndex+=1
            else:
                levelIndex-=1
                
        elif levelIndex == 4:
            pygame.display.set_caption("Can you predict the trajectory?")
            if predictionLevel([450,350]):
                levelIndex+=1
            else:
                levelIndex-=1
        elif levelIndex == 5:
            pygame.display.set_caption("Impressive!")
            if predictionLevel([300,200]):
                levelIndex+=1
            else:
                levelIndex-=1
        elif levelIndex == 6:
            pygame.display.set_caption("Oh wait this one is actually easy.")
            if predictionLevel_hard([450,350], 1):
                levelIndex+=1
            else:
                levelIndex-=1
        elif levelIndex == 7:
            pygame.display.set_caption("This one isn't so easy though!")
            if predictionLevel_hard([450,350], 2):
                levelIndex+=1
            else:
                levelIndex-=1
        elif levelIndex == 8:
            pygame.display.set_caption("This gets hard quickly! Think you still got it?")
            if predictionLevel_hard([450,350], 3):
                levelIndex+=1
            else:
                levelIndex-=1
        elif levelIndex == 9:
            pygame.display.set_caption("This is getting out of hand.")
            if predictionLevel_hard([450,350], 4):
                levelIndex+=1
            else:
                levelIndex-=1
        elif levelIndex == 10:
            pygame.display.set_caption("Newton just activated Gravity! Survive until he deactivates the walls!")
            if gravitySurvival():
                levelIndex+=1
            else:
                levelIndex-=1 
        elif levelIndex == 11:
            pygame.display.set_caption("Since you now need to deal with gravity, we went ahead and made the goal bigger.")
            if target_Gravity([600,300], [200,300]):
                levelIndex+=1
            else:
                levelIndex-=1
        elif levelIndex == 12:
            pygame.display.set_caption("Gravity actually isn't that bad!")
            if target_Gravity([600,200], [250,555]):
                levelIndex+=1
            else:
                levelIndex-=1
        elif levelIndex == 13:
            pygame.display.set_caption("Can you still predict trajectories?")
            if predictionLevel_Gravity([450,350], 2):
                levelIndex+=1
            else:
                levelIndex-=1
        elif levelIndex == 14:
            pygame.display.set_caption("This is the hardest prediction level.")
            if predictionLevel_Gravity([450,350], 5):
                levelIndex+=1
            else:
                levelIndex-=1
        elif levelIndex == 15:
            pygame.display.set_caption("Your arrow got switched to momentum arrows!")
            if target_Momentum([555,300], [300,300]):
                levelIndex+=1
            else:
                levelIndex-=1
        elif levelIndex == 16:
            pygame.display.set_caption("Ever heard of Napoleon's Cannon?")
            if target_Momentum([555,100], [100,500]):
                levelIndex+=1
            else:
                levelIndex-=1
        
        
        
        if levelIndex<0:
            levelIndex = 0
        time.sleep(0.4)
        
    
    
    pygame.quit()