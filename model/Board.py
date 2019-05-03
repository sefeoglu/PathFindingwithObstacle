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
        
           
    def _on_model(self):
        
        
        
    def move(self):
        
        
        
    def won(self):