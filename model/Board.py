# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:31:46 2019

@author: sefika
"""
import clingo

# =============================================================================
# Sefika's OOP
# =============================================================================
class Board:
    def __init__(self):
        
        self.blocked      = []
        self.goal         = []
        self.robot        = []
        self.field        = []

        control_object = clingo.Control()
        control_object.load("../Encoding/environment.lp")
        control_object.ground([("base", [])])
        control_object.solve(on_model=self.__on_model) 
    
    def __on_model(self, m):
        for atom in m.symbols(atoms=True):
            if atom.name == "obstacle" and len(atom.arguments) == 2:
                y_o,x_o= [n.number for n in atom.arguments]
                self.blocked.append((x_o, y_o))
            elif atom.name == "field" and len(atom.arguments) == 2:
                y_f,x_f= [n.number for n in atom.arguments]
                self.field.append((x_f, y_f))
            elif atom.name == "goal" and len(atom.arguments) == 2:
                y_g,x_g= [n.number for n in atom.arguments]
                self.goal.append((x_g, y_g))
            elif atom.name == "robot" and len(atom.arguments) == 2:
                y_r,x_r= [n.number for n in atom.arguments]
                self.robot.append((x_r, y_r))
                