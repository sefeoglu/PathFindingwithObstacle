# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:31:46 2019

@author: sefik
"""
import clingo


class Board:
    def __init__(self):
        self.size           = 1
        self.blocked        = set()
        self.target        = set()
        self.pos            = dict()
        self.robot         = [{}]
        self.moves          = []
        self.solution       = None

        control_object = clingo.Control()
        control_object.load("../Encoding/environment.lp")
        control_object.ground([("base", [])])
        control_object.solve(on_model=self.__on_model) 
    def __on_model(self, m):
        for atom in m.symbols(atoms=True):
            if atom.name == "obstacle" and len(atom.arguments) == 2:
                y_o,x_o= [n.number for n in atom.arguments]
                self.blocked.add((x_o, y_o))
            elif atom.name == "field" and len(atom.arguments) == 2:
                self.size = max(self.size, atom.arguments[0].number)
            elif atom.name == "goal" and len(atom.arguments) == 2:
                y_g,x_g= [n.number for n in atom.arguments]
                self.target.add((x_g, y_g))
            elif atom.name == "robot" and len(atom.arguments) == 2:
                y_r,x_r= [n.number for n in atom.arguments]
                self.target.add((x_r, y_r))
                
board = Board()