# -*- coding: utf-8 -*-
"""
Created on Thu May  9 20:15:31 2019

@author: sefika
"""

import sys
sys.path.append('../controller/')
import RobotKnowledgeController
sys.path.append("../model/")
import Board
try:
    import Tkinter
except ImportError:
    import tkinter as Tkinter
#
# =============================================================================
# Sefika's OOP
# =============================================================================

class Visualization:
    def __init__(self):
        self.__board =  Board.Board()
        self.__margin           = 20
        self.__tile_size        = 40
        self.__canvas_width     = None
        self.__canvas_height    = None
        rbtc = RobotKnowledgeController.RobotKnowledgeController()
        self.paths = rbtc.explore_environment()
       
    def simulation(self):

        obstacle_list = []
        for line in self.paths:
            root = Tkinter.Tk()
            root.grid()
            height = int(self.__board.dimension)
            width = int(self.__board.dimension)
            path = line[0]
            obstacle = line[1]
            if (obstacle[1]!=1 or obstacle[2]!=1) or (obstacle[1]!=0 or obstacle[2]!=1):
                obstacle_list.append((obstacle[0],obstacle[1]))
            if obstacle[1]== -1 and obstacle[2] == -1:
                break
            path_t = []
            for field in path:
                if path[0][0] != field[0] or path[0][1] != field[1] :
                    path_t.append((field[0],field[1]))

            for i in range(height):
                for j in range(width):
                    button = Tkinter.Button(root, text=str(i+1)+str(j+1))
                    button.grid(row=i,column=j)
                    if obstacle_list.count((i+1,j+1)) !=0:
                        button['bg'] = "red"
                    if path[0][0]-1 == i and path[0][1]-1 == j:
                        button['bg'] = "pink"
                    if path_t.count((i+1,j+1)) !=0:
                        button['bg'] = "blue"
                    if self.__board.goal[0][0] == i+1 and self.__board.goal[0][1] == j+1:
                        button['bg'] = "green"
                    
            root.mainloop()
                

            

view = Visualization()
view.simulation()


