from tkinter import *
import numpy as np
import time
import random
import math
from .network import Network
from termcolor import colored, cprint

class Paddle:
    def __init__(self, cElem, scoreElem):
        self.dY = 0
        self.cElem = cElem
        self.hit = 0
        self.miss = 0
        self.scoreElem = scoreElem


class Ball:
    def __init__(self, cElem):
            self.cElem = cElem
            self.dX = 5
            self.dXS = 5
            self.dY = random.randrange(10, 400)/100 - 2
            self.dXCap = 15
            self.spin = 1.7


class Window:
    def __init__(self, master, depth, weights=[]):
        self.paddleSpd = 7
        self.master = master
        self.width = 600
        self.height = 400
        self.startW = 600
        self.startH = 400
        self.master.title = "Pong vs AI"
        self.master.bind("<KeyRelease>", self.keyup)
        self.master.bind("<KeyPress>", self.keydown)
        self.canvas = Canvas(self.master, width=self.width,
                             height=self.height)
        self.canvas.pack(fill='both')
        self.canvas.configure(background='black')
        self.canvas.focus_set()
        self.depth = depth
        self.net = Network(self.depth)
        if len(weights) == 0:
            self.net.randomizeWeights()
        else:
            self.net.setWeights(weights)
        
        # Create mid line
        self.midLine = self.canvas.create_line(self.width/2, 5,
                                               self.width/2, self.height,
                                               dash=(10, 5), width=10,
                                               fill='grey')
        # Create Roof
        self.roof = self.canvas.create_rectangle(0, 0, self.width, 10,
                                                 fill='grey')
        # Create Floor
        self.floor = self.canvas.create_rectangle(0, self.height-10, self.width,
                                                  self.height, fill='grey')
        
        # Create Paddle 1
        self.paddle1 = Paddle(
                self.canvas.create_rectangle(self.width*0.05,
                                             self.height*0.47,
                                             self.width*0.068,
                                             self.height*0.64,
                                             fill='white'),
                self.canvas.create_text(self.width/2-50, 50, fill='grey',
                                        text='0', font=("Times New Roman", 45, "bold")))
        # Create Paddle 2
        self.paddle2 = Paddle(
                self.canvas.create_rectangle(self.width*0.95,
                                             self.height*0.47,
                                             self.width*0.932,
                                             self.height*0.64,
                                             fill='white'),
                self.canvas.create_text(self.width/2 + 50, 50, fill='grey',
                                        text='0', font=("Times New Roman", 45, "bold")))
        # Create Ball
        self.ball = Ball(self.canvas.create_rectangle(self.width/2 - 6,
                                                      self.height/2 - 6,
                                                      self.width/2 + 6,
                                                      self.height/2 + 6,
                                                      fill='white'))

    def keydown(self, e):
        if e.keycode == 87:  # W pressed
            self.paddle1.dY = -1

        if e.keycode == 83:  # S pressed
            self.paddle1.dY = 1

    def keyup(self, e):
        if (e.keycode == 38 and self.paddle2.dY == -1) or (e.keycode == 40 and
           self.paddle2.dY == 1):  # up or down released
           self.paddle2.dY = 0

        if (e.keycode == 87 and self.paddle1.dY == -1) or (e.keycode == 83 and
           self.paddle1.dY == 1):  # up or down released
           self.paddle1.dY = 0

    def update(self):
        # Get Roof And Ceiling
        roofCoords = self.canvas.coords(self.roof)
        floorCoords = self.canvas.coords(self.floor)
        ballCoords = self.canvas.coords(self.ball.cElem)
        pad1Coords = self.canvas.coords(self.paddle1.cElem)
        pad2Coords = self.canvas.coords(self.paddle2.cElem)
        ballCenter = [(ballCoords[0]+ballCoords[2])/2,
                      (ballCoords[1]+ballCoords[3])/2]
        nextBallCenter = [ballCenter[0]+self.ball.dX,
                          ballCenter[1]+self.ball.dY]
        pad2Center = (pad2Coords[1]+pad2Coords[3])/2

        # Determine Move For Paddle 2
        net_inputs = [ballCenter[0], ballCenter[1], nextBallCenter[0],
                       nextBallCenter[1], pad2Center]
        up_prob = self.net.run(net_inputs)
        if up_prob >= 0.5:  # High probability of moving up
            self.paddle2.dY = -1
        else:  # Low probability of moving up
            self.paddle2.dY = 1

        # Move Paddle 1
        self.canvas.move(self.paddle1.cElem, 0, self.paddleSpd*self.paddle1.dY)
        pad1Coords = self.canvas.coords(self.paddle1.cElem)

        # Paddle 1 Col
        if pad1Coords[1] < roofCoords[3]:
            self.canvas.coords(self.paddle1.cElem, [pad1Coords[0],
                               roofCoords[3], pad1Coords[2],
                               pad1Coords[3]+(roofCoords[3]-pad1Coords[1])])
            pad1Coords = self.canvas.coords(self.paddle1.cElem)
            
        elif pad1Coords[3] > floorCoords[1]:
            self.canvas.coords(self.paddle1.cElem, [pad1Coords[0],
                               pad1Coords[1]-(pad1Coords[3]-floorCoords[1]),
                               pad1Coords[2], floorCoords[1]])
            pad1Coords = self.canvas.coords(self.paddle1.cElem)

        # Move Paddle 2
        self.canvas.move(self.paddle2.cElem, 0, self.paddleSpd*self.paddle2.dY)
        
        # Paddle 2 Col
        pad2Coords = self.canvas.coords(self.paddle2.cElem)
        if pad2Coords[1] < roofCoords[3]:
            self.canvas.coords(self.paddle2.cElem, [pad2Coords[0],
                               roofCoords[3], pad2Coords[2],
                               pad2Coords[3] + (roofCoords[3]-pad2Coords[1])])
            pad2Coords = self.canvas.coords(self.paddle2.cElem)
    
             
        elif pad2Coords[3] > floorCoords[1]:
            self.canvas.coords(self.paddle2.cElem, [pad2Coords[0],
                               pad2Coords[1]-(pad2Coords[3]-floorCoords[1]),
                               pad2Coords[2], floorCoords[1]])
            pad2Coords = self.canvas.coords(self.paddle2.cElem)
            
        # Move Ball
        self.canvas.move(self.ball.cElem, self.ball.dX, self.ball.dY)
        
        # Ball col with wall (top and bottom)
        ballCoords = self.canvas.coords(self.ball.cElem)
        if ballCoords[1] < roofCoords[3]:
            self.ball.dY = math.fabs(self.ball.dY)

        elif ballCoords[3] > floorCoords[1]:
            self.ball.dY = -1 * math.fabs(self.ball.dY)

        # Ball col with Paddle 1
        if ballCoords[0]<=pad1Coords[2] and ballCoords[3]>=pad1Coords[1] and \
           ballCoords[1]<=pad1Coords[3]:
               self.ball.dX = math.fabs(self.ball.dX)
               if math.fabs(self.ball.dX) < self.ball.dXCap:
                   self.ball.dX *= 1.05
               # Spin
               if self.paddle1.dY == -1:
                  self.ball.dY -= self.ball.spin
               elif self.paddle1.dY == 1:
                   self.ball.dY += self.ball.spin

               self.canvas.coords(self.ball.cElem, [pad1Coords[2],
                                                    ballCoords[1],
                                                    pad1Coords[2]+12,
                                                    ballCoords[3]])

        # Ball col with Paddle 2
        if ballCoords[2]>=pad2Coords[0] and ballCoords[3]>=pad2Coords[1] and \
           ballCoords[1]<=pad2Coords[3]:
               self.ball.dX = -1 * math.fabs(self.ball.dX)
               if math.fabs(self.ball.dX) < self.ball.dXCap:
                   self.ball.dX *= 1.05
               # Spin
               if self.paddle2.dY == -1:
                  self.ball.dY -= self.ball.spin
               elif self.paddle2.dY == 1:
                   self.ball.dY += self.ball.spin

               self.canvas.coords(self.ball.cElem, [pad2Coords[0]-12,
                                                    ballCoords[1],
                                                    pad2Coords[0],
                                                    ballCoords[3]])

        # Ball Col with left side (point by paddle 2)
        scored = False
        if ballCoords[2] <= pad1Coords[0]:
            self.paddle2.hit += 1
            self.paddle1.miss += 1
            self.ball.dXS = math.fabs(self.ball.dXS)
            self.canvas.itemconfig(self.paddle2.scoreElem, text=self.paddle2.hit)
            scored = True

        # Ball Col with Right Side (point by paddle 1)
        if ballCoords[0] >= pad2Coords[2]:
            self.paddle1.hit += 1
            self.paddle1.miss += 1
            self.ball.dXS = -1 * math.fabs(self.ball.dXS)
            self.canvas.itemconfig(self.paddle1.scoreElem, text=self.paddle1.hit)
            scored = True
        
        if scored:
            self.ball.dX = 0
            self.ball.dY = 0
            self.canvas.coords(self.ball.cElem, [self.width/2-6, self.height/2-6,
                               self.width/2+6, self.height/2+6])
            self.canvas.update()
            time.sleep(0.5)
            self.ball.dX = self.ball.dXS
            self.ball.dY = random.randrange(10, 400)/100 - 2
        else:
            # Update canvas
            self.canvas.update()
            time.sleep(1/60)



if __name__ == '__main__':
    win = Window(Tk())
    print('This cannot be run without main.py')

