'''
PONG NN TRAINER

This program trains a neural network to play pong. The network is trained using a custom genetic algorithm
Refer to the README for more information
'''

from tkinter import *
from modules.classes import *
from termcolor import colored, cprint


def init():
    # Initialize the gameConfig dictionary
    # Can be adjusted - will affect network performance
    gameConfig = {}
    gameConfig['pop'] = 50
    gameConfig['depth'] = 25
    gameConfig['mutation'] = 0.04
    
    # Initialize the window
    root = Tk()
    root.attributes("-topmost", True)
    title = "Pong NN Pop: {0} Depth: {1} Mutation: {2}".format(
            gameConfig['pop'], gameConfig['depth'], gameConfig['mutation'])
    cprint('\n'+title+'\n', 'cyan', attrs=['bold', 'underline'])
    root.title(title)
    root.resizable(width=False, height=False)
    root.after(1, lambda: root.focus_force())
    win = Window(root, gameConfig)
    time.sleep(1)
    
    # return the window
    return win

def update_loop(win):
    # Loops until window is closed
    # Calls the window update function
    while True:
        try:
            win.update()
        except TclError:
            cprint('\n\nLeft early did ya??', 'cyan', attrs=['bold', 'underline'])
            break

if __name__ == '__main__':
    # Initialize the Game
    win = init()
    # Call update loop
    update_loop(win)