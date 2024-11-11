'''
classes.py

Contains the classes used (except the network class)

Classes:
    Paddle: Used to create a paddle object
    Ball: Used to create a ball object
    Window: Used to create the window object

'''

from tkinter import *
import numpy as np
import time
import random
import math
from termcolor import colored, cprint
from .network import Network
parents1 = []  # Used to record the best parent genomes
parents2 = []  # Used to record the best parent genomes

class Paddle:
    def __init__(self, cElem):
        # Vars:
        #   cElem: Canvas Element
        #   dY: Direction of movement
        #   hit: Number of times the paddle has hit the ball
        #   miss: Number of times the paddle has missed the ball
        self.dY = 0
        self.cElem = cElem
        self.hit = 0
        self.miss = 0


class Ball:
    def __init__(self, cElem, dY):
        # Vars:
        #   cElem: Canvas Element
        #   dX: Direction of movement on the x-axis
        #   dXS: Direction of movement on the x-axis (starting direction)
        #   dY: Direction of movement on the y-axis
        #   dXCap: Maximum speed of the ball
        #   spin: Amount of spin on the ball
        self.cElem = cElem
        self.dX = 5
        self.dXS = 5
        self.dY = dY
        self.dXCap = 15
        self.spin = 1.7


class Window:
    def __init__(self, master, gameConfig):
        # Vars:
        #   master: Tkinter master object
        #   width: Width of the window
        #   height: Height of the window
        #   pop: Population size
        #   canvas: Canvas object
        #   defColors: Default colors for the paddles
        #   hidden_layers: Number of hidden layers in the network
        #   mutation_rate: Mutation rate of the network
        #   net1, net2: List of network objects
        #   finishedNets1, finishedNets2: List of network objects that have finished playing
        #   duration: Duration of the game
        #   bestFitness1, bestFitness2: Best fitness of the generation for net 1 and net 2
        #   prevGenomes1, prevGenomes2: Last set of genomes that resulted in a better fitness
        #   Also contains the vars for the game ui
        
        np.random.seed(None)
        self.limit_speed = False # limits the frame rate of the game if True (faster if kept False)
        self.paddleSpd = 10 # Speed of paddle
        self.paddleHeight = 68 # Height of paddle
        self.master = master 
        # Set window size
        self.width = 600
        self.height = 400
        self.pop = gameConfig['pop'] # Population size
        
        # Create canvas
        self.canvas = Canvas(self.master, width=self.width,
                             height=self.height)
        self.canvas.pack(fill='both')
        self.canvas.configure(background='black')
        self.canvas.focus_set()
        self.defColors = {'random':'white', 'father':'red', 'mother':'green',
                          'child':'yellow'}
        # Create NN
        self.hidden_layers = gameConfig['depth']
        self.mutation_rate = gameConfig['mutation']
        # Net 1
        self.net1 = self.configureNets()
        self.finishedNets1 = []
        # Net 2
        self.net2 = self.configureNets()
        self.finishedNets2 = []
        # Used to determine the duration - portion of the fitness
#        self.startTime = time.clock()
        self.duration = 0
        self.bestFitness1 = 0  # Used to determine best fitness of generation for net 1
        self.bestFitness2 = 0  # Used to determine best fitness of generation for net 2
        # Last set of genomes that resulted in a better fitness
        self.prevGenomes1 = []
        self.prevGenomes2 = []
        self.gen = 1  # Current Generation

        # Create mid line
        self.midLine = self.canvas.create_line(self.width/2, 5,
                                               self.width/2, self.height,
                                               dash=(10, 5), width=10,
                                               fill='grey')
        # Create Roof
        self.roof = self.canvas.create_rectangle(0, 0, self.width, 10,
                                                 fill='grey')
        # Create Floor
        self.floor = self.canvas.create_rectangle(0, self.height-10,
                                                  self.width, self.height,
                                                  fill='grey')

        # Create Texts
        self.genText = self.canvas.create_text(80, 50, fill='grey',
                                               text='Generation: 1',
                                               font=("Times New Roman", 16,
                                                     "bold"), anchor='w')
        self.fit1Text = self.canvas.create_text(80, 75, fill='grey',
                                               text='Best Fitness: 0',
                                               font=("Times New Roman", 16,
                                                     "bold"), anchor='w')
        self.alive1Text = self.canvas.create_text(80, 100, fill='grey',
                                               text='Alive: {0}'.format(self.pop),
                                               font=("Times New Roman", 16,
                                                     "bold"), anchor='w')
        
        self.net1Score = self.canvas.create_text(250, 300, fill='grey',
                                               text='0',
                                               font=("Times New Roman", 50,
                                                     "bold"), anchor='e')
        
        self.fit2Text = self.canvas.create_text(350, 75, fill='grey',
                                               text='Best Fitness: 0',
                                               font=("Times New Roman", 16,
                                                     "bold"), anchor='w')
        
        self.alive2Text = self.canvas.create_text(350, 100, fill='grey',
                                               text='Alive: {0}'.format(self.pop),
                                               font=("Times New Roman", 16,
                                                     "bold"), anchor='w')
        
        self.net2Score = self.canvas.create_text(350, 300, fill='grey',
                                               text='0',
                                               font=("Times New Roman", 50,
                                                     "bold"), anchor='w')

        # Create colors
        self.colors = []
        # Create Paddle
        self.paddle1 = []
        self.pad1HitCap = 3#11
        # Create Paddle
        self.paddle2 = []
        self.pad2HitCap = 3#11
        # Create Ball
        self.ball = []

        # Configure each population
        self.configurePop(True)

    def configurePop(self, init=False):
        cprint('Starting New Gen', 'yellow', attrs=['bold'])
        if init:
            # Ran on initial configuration
            self.configureColors()

        for i in range(0, self.pop):
            self.paddle1.append(self.configurePaddle('left', self.defColors[self.colors[i]]))
            self.paddle2.append(self.configurePaddle('right', self.defColors[self.colors[i]]))
            self.ball.append(self.configureBall(random.randrange(10, 400)/100 -
                                                2, self.defColors[self.colors[i]]))

    def configureColors(self):
        self.colors = []
        for i in range(0, self.pop):
            self.colors.append('random')

    def configureNets(self):
        # Inital config for networks
        # Sets weights randomly
        net = []
        for i in range(0, self.pop):
            net.append(Network(self.hidden_layers, self.mutation_rate))
            net[i].randomizeWeights()
        return net

    def configurePaddle(self, side, col):
        if side == 'left':  # Left Net
            return Paddle(
                self.canvas.create_rectangle(self.width*0.05, self.height/2-self.paddleHeight/2,
                                             self.width*0.06,
                                             self.height/2+self.paddleHeight/2, fill=col))
        else:  # Right Net
            return Paddle(
                self.canvas.create_rectangle(self.width*0.95, self.height/2-self.paddleHeight/2,
                                             self.width*0.94,
                                             self.height/2+self.paddleHeight/2, fill=col))

    def configureBall(self, random_start, col):
        return Ball(self.canvas.create_rectangle(self.width/2 - 6,
                                                 self.height/2 - 6,
                                                 self.width/2 + 6,
                                                 self.height/2 + 6,
                                                 fill=col), random_start)

    def update(self):
        np.random.seed(None)
        if len(self.net1) > 0 and len(self.net2) > 0:
            best_score1 = [-1, 'grey']
            best_score2 = [-1, 'grey']
            # Get Roof And Floor
            roofCoords = self.canvas.coords(self.roof)
            floorCoords = self.canvas.coords(self.floor)
            i = 0
            self.duration += 1
            while i < len(self.net1) and i < len(self.net2):
                # Game is ongoing
                # Iterate through the population
                ballCoords = self.canvas.coords(self.ball[i].cElem)
                pad1Coords = self.canvas.coords(self.paddle1[i].cElem)
                pad2Coords = self.canvas.coords(self.paddle2[i].cElem)
                ballCenter = [(ballCoords[0]+ballCoords[2])/2,
                           (ballCoords[1]+ballCoords[3])/2]
                nextBallCenter = [ballCenter[0]+self.ball[i].dX,
                               ballCenter[1]+self.ball[i].dY]
                pad1Center = (pad1Coords[1]+pad1Coords[3])/2
                pad2Center = (pad2Coords[1]+pad2Coords[3])/2

                # Determine Move For Paddle 1
                net_inputs1 = [ballCenter[0], ballCenter[1], nextBallCenter[0],
                              nextBallCenter[1], pad1Center]
                up_prob1 = self.net1[i].run(net_inputs1)
                if up_prob1 >= 0.5:  # High probability of moving up
                    self.paddle1[i].dY = -1
                else:  # Low probability of moving up
                    self.paddle1[i].dY = 1
                
                # Determine Move For Paddle 2
                net_inputs2 = [ballCenter[0], ballCenter[1], nextBallCenter[0],
                              nextBallCenter[1], pad2Center]
                up_prob2 = self.net2[i].run(net_inputs2)
                if up_prob2 >= 0.5:
                    self.paddle2[i].dY = -1
                else:
                    self.paddle2[i].dY = 1

                # Move Paddle 1
                self.canvas.move(self.paddle1[i].cElem, 0,
                                 self.paddleSpd*self.paddle1[i].dY)
                pad1Coords = self.canvas.coords(self.paddle1[i].cElem)

                # Paddle 1 Col
                pad1Coords = self.canvas.coords(self.paddle1[i].cElem)
                if pad1Coords[1] < roofCoords[3]:
                    self.canvas.coords(self.paddle1[i].cElem, [pad1Coords[0],
                                       roofCoords[3], pad1Coords[2],
                                       pad1Coords[3] +
                                       (roofCoords[3] - pad1Coords[1])])
                    pad1Coords = self.canvas.coords(self.paddle1[i].cElem)

                elif pad1Coords[3] > floorCoords[1]:
                    self.canvas.coords(self.paddle1[i].cElem, [pad1Coords[0],
                                       pad1Coords[1] -
                                       (pad1Coords[3]-floorCoords[1]),
                                       pad1Coords[2], floorCoords[1]])
                    pad1Coords = self.canvas.coords(self.paddle1[i].cElem)

                # Move Paddle 2
                self.canvas.move(self.paddle2[i].cElem, 0,
                                 self.paddleSpd*self.paddle2[i].dY)

                # Paddle 2 Col
                pad2Coords = self.canvas.coords(self.paddle2[i].cElem)
                if pad2Coords[1] < roofCoords[3]:
                    self.canvas.coords(self.paddle2[i].cElem, [pad2Coords[0],
                                       roofCoords[3], pad2Coords[2],
                                       pad2Coords[3] +
                                       (roofCoords[3]-pad2Coords[1])])
                    pad2Coords = self.canvas.coords(self.paddle2[i].cElem)

                elif pad2Coords[3] > floorCoords[1]:
                    self.canvas.coords(self.paddle2[i].cElem, [pad2Coords[0],
                                       pad2Coords[1] -
                                       (pad2Coords[3]-floorCoords[1]),
                                       pad2Coords[2], floorCoords[1]])
                    pad2Coords = self.canvas.coords(self.paddle2[i].cElem)

                # Move Ball
                self.canvas.move(self.ball[i].cElem, self.ball[i].dX,
                                 self.ball[i].dY)

                # Ball col with wall (top and bottom)
                ballCoords = self.canvas.coords(self.ball[i].cElem)
                if ballCoords[1] < roofCoords[3]:
                    self.ball[i].dY = math.fabs(self.ball[i].dY)

                elif ballCoords[3] > floorCoords[1]:
                    self.ball[i].dY = -1 * math.fabs(self.ball[i].dY)

                # Ball col with Paddle 1
                if ballCoords[0] <= pad1Coords[2] and ballCoords[3] >=\
                   pad1Coords[1] and ballCoords[1] <= pad1Coords[3]:
                        self.ball[i].dX = math.fabs(self.ball[i].dX)
                        if math.fabs(self.ball[i].dX) < self.ball[i].dXCap:
                            self.ball[i].dX *= 1.02
                        # Spin
                        if self.paddle1[i].dY == -1:
                            self.ball[i].dY -= self.ball[i].spin
                        elif self.paddle1[i].dY == 1:
                            self.ball[i].dY += self.ball[i].spin

                        self.canvas.coords(self.ball[i].cElem,
                                           [pad1Coords[2], ballCoords[1],
                                            pad1Coords[2]+12, ballCoords[3]])

                # Ball col with Paddle 2
                if ballCoords[2] >= pad2Coords[0] and ballCoords[3] >=\
                   pad2Coords[1] and ballCoords[1] <= pad2Coords[3]:
                        self.ball[i].dX = -1 * math.fabs(self.ball[i].dX)
                        if math.fabs(self.ball[i].dX) < self.ball[i].dXCap:
                            self.ball[i].dX *= 1.02

                        # Spin
                        if self.paddle2[i].dY == -1:
                            self.ball[i].dY -= self.ball[i].spin
                        elif self.paddle2[i].dY == 1:
                            self.ball[i].dY += self.ball[i].spin

                        self.canvas.coords(self.ball[i].cElem,
                                           [pad2Coords[0]-12, ballCoords[1],
                                            pad2Coords[0], ballCoords[3]])

                # Ball Col with left side (point by paddle 2)
                scored = False
                if ballCoords[2] <= pad1Coords[0]:
                    self.paddle2[i].hit += 1
                    self.paddle1[i].miss += 1
                    self.ball[i].dXS = math.fabs(self.ball[i].dXS)
                    scored = True

                # Ball Col with Right Side (point by paddle 1)
                if ballCoords[0] >= pad2Coords[2]:
                    self.paddle1[i].hit += 1
                    self.paddle2[i].miss += 1
                    self.ball[i].dXS = -1 * math.fabs(self.ball[i].dXS)
                    scored = True
                
                # Update Highest Score
                if self.paddle1[i].hit > best_score1[0]:
                    best_score1[0] = self.paddle1[i].hit
                    best_score1[1] = self.defColors[self.colors[i]]
                if self.paddle2[i].hit > best_score2[0]:
                    best_score2[0] = self.paddle2[i].hit
                    best_score2[1] = self.defColors[self.colors[i]]
                
                if scored:
                    # Reset Ball
                    self.canvas.coords(self.ball[i].cElem, [self.width/2-6,
                                       self.height/2-6, self.width/2+6,
                                       self.height/2+6])
                    self.ball[i].dX = self.ball[i].dXS
                    self.ball[i].dY = random.randrange(10, 400)/100 - 2

                if self.paddle1[i].hit == self.pad1HitCap or\
                    self.paddle2[i].hit == self.pad2HitCap:
                    # Game over, stopping play
                    
                    # Calculate Fitness For Net 1
                    fitness1 = self.duration/60 + self.paddle1[i].hit*50 -\
                        self.paddle1[i].miss*50
                    # Set fitness for net 1
                    self.net1[i].fitness = fitness1
                    # Move Net 1 to the finished list
                    self.finishedNets1.append(self.net1.pop(i))

                    # Calculate Fitness For Net 2
                    fitness2 = self.duration/60 + self.paddle2[i].hit*50 -\
                        self.paddle2[i].miss*50
                    # Set fitness for net 2
                    self.net2[i].fitness = fitness2
                    # Move Net 2 to the finished list
                    self.finishedNets2.append(self.net2.pop(i))
                    
                    # Remove elems from canvas
                    self.canvas.delete(self.ball[i].cElem)
                    del self.ball[i]
                    self.canvas.delete(self.paddle1[i].cElem)
                    del self.paddle1[i]
                    self.canvas.delete(self.paddle2[i].cElem)
                    del self.paddle2[i]
                else:
                    # Iterate if game isn't over
                    i += 1
            # Set Score
            self.canvas.itemconfig(self.net1Score, text=best_score1[0],
                                   fill=best_score1[1])
            self.canvas.itemconfig(self.net2Score, text=best_score2[0],
                                   fill=best_score2[1])
            # Set alive text
            self.canvas.itemconfig(self.alive1Text,
                                   text='Alive: {0}'.format(len(self.net1)))
            self.canvas.itemconfig(self.alive2Text,
                                   text='Alive: {0}'.format(len(self.net2)))
            self.canvas.update()
            if self.limit_speed:
                time.sleep(1/60)

        else:  # Games are over
            # Start new Generation
            cprint('Games Are Over', 'blue', attrs=['bold'])
            print('Finding Best Nets')
            best_nets1, highest_fitness1 = self.findBestNets(self.finishedNets1)
            best_nets2, highest_fitness2 = self.findBestNets(self.finishedNets2)
            
            # Reproduce Net 1
            if highest_fitness1 > self.bestFitness1 or len(self.prevGenomes1)<2:  # Reproduce
                cprint('Gen {0}: Improvement for Net 1. Fitness: {1}'.format(
                        self.gen, round(self.bestFitness1, 2)), 'green',
                        attrs=['bold'])
                self.bestFitness1 = highest_fitness1
                father1 = best_nets1[0].getGenome()
                mother1 = best_nets1[1].getGenome()
                self.prevGenomes1 = [father1, mother1]
                parents1.append(['Generation: {0}, Depth: {1}, Mutation Rate: \
                                 {2}'.format(self.gen, self.hidden_layers,
                                             self.mutation_rate),
                                father1, mother1])
            else:
                cprint('Generation {0}: Failure for Net 1'.format(self.gen),
                       'red', attrs=['bold'])
                father1 = self.prevGenomes1[0]
                mother1 = self.prevGenomes1[1]

            # Reproduce Net 2
            if highest_fitness2 > self.bestFitness2 or len(self.prevGenomes2)<2:  # Reproduce
                cprint('Gen {0}: Improvement for Net 2. Fitness: {1}'.format(
                        self.gen, round(self.bestFitness2, 2)), 'green',
                        attrs=['bold'])
                self.bestFitness2 = highest_fitness2
                father2 = best_nets2[0].getGenome()
                mother2 = best_nets2[1].getGenome()
                self.prevGenomes2 = [father2, mother2]
                parents2.append(['Generation: {0}, Depth: {1}, Mutation Rate: \
                                 {2}'.format(self.gen, self.hidden_layers,
                                             self.mutation_rate),
                                father2, mother2])

            else:
                cprint('Generation {0}: Failure for Net 2'.format(self.gen),
                       'red', attrs=['bold'])
                father2 = self.prevGenomes2[0]
                mother2 = self.prevGenomes2[1]


            # Update Both Nets
            self.updateNets(father1, mother1, father2, mother2)
            self.gen += 1
            # Update Text Info
            self.canvas.itemconfig(self.genText, text='Generation: {0}'.format(self.gen))
            self.canvas.itemconfig(self.fit1Text, text='Best Fitness: {0}'.format(round(self.bestFitness1, 2)))
            self.canvas.itemconfig(self.fit2Text, text='Best Fitness: {0}'.format(round(self.bestFitness2, 2)))
            self.resetGame()
    
    def findBestNets(self, nets):
        # Finds the best two nets of curr gen
        # Returns the best two nets and the best fitness
        best_fit_of_two = -100
        best_nets = []
        last_index = -1
        while len(best_nets) < 2:
            highest_fitness = -100
            fitness_index = -1
            for j in range(0, len(nets)):
                if (nets[j].fitness > highest_fitness):
                    highest_fitness = nets[j].fitness
                    fitness_index = j
            best_nets.append(nets.pop(fitness_index))
            if highest_fitness > best_fit_of_two:
                best_fit_of_two = highest_fitness
        return best_nets, best_fit_of_two

    def createChild(self, father, mother):
        # Creates a child from two parents
        # Randomly selects a portion of the father and mother
        random_low = np.random.randint(0, len(father))
        random_high = np.random.randint(0, len(father))
        while random_low == random_high:
            random_high = np.random.randint(0, len(father))

        if random_low > random_high:
            random_low, random_high = random_high, random_low

        child = father[0:random_low] + mother[random_low:random_high] +\
            father[random_high:]
        return child

    def updateNets(self, father1, mother1, father2, mother2):
        # Updates the nets based on the parents
        print('Updating Nets')
        child_nets = self.pop*0.25  # Make 25% of nets based off of child
        father_nets = child_nets + self.pop*0.25 # Make 25% of nets based off of father
        mother_nets = father_nets + self.pop*0.25  # Make 25% of nets based off of mother
        self.net1 = []
        self.net2 = []
        self.colors = []
        j = 0
        while j < child_nets:
            self.net1.append(self.finishedNets1[j])
            self.net1[j].setWeights(self.createChild(father1, mother1))
            self.net2.append(self.finishedNets2[j])
            self.net2[j].setWeights(self.createChild(father2, mother2))
            self.colors.append('child')
            j += 1
        while j < father_nets:
            self.net1.append(self.finishedNets1[j])
            self.net1[j].updateWeights(father1)
            self.net2.append(self.finishedNets2[j])
            self.net2[j].updateWeights(father2)
            self.colors.append('father')
            j += 1
        while j < mother_nets:
            self.net1.append(self.finishedNets1[j])
            self.net1[j].updateWeights(mother1)
            self.net2.append(self.finishedNets2[j])
            self.net2[j].updateWeights(mother2)
            self.colors.append('mother')
            j += 1
        while j < self.pop:
            self.net1.append(Network(self.hidden_layers, self.mutation_rate))
            self.net1[j].randomizeWeights()
            self.net2.append(Network(self.hidden_layers, self.mutation_rate))
            self.net2[j].randomizeWeights()
            self.colors.append('random')
            j += 1
        self.finishedNets1 = []
        self.finishedNets2 = []

    def resetGame(self):
        cprint('Resetting Game\n\n', 'yellow', attrs=['bold'])
        # Create Paddle
        self.paddle1 = []
        # Create Paddle
        self.paddle2 = []
        # Create Ball
        self.ball = []
        # Reset Duration
        self.duration = 0
        # Configure each population
        self.configurePop()


if __name__ == '__main__':
    cprint('This cannot be run without main.py', 'red')
