# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:47:33 2019

@author: sefik
"""
import clingo

class Solver:

    def __init__(self):
        self.solution = []
        self.control_object = clingo.Control()
        self.control_object.add("check", ["k"], "#external query(k).")
        self.solver()
        
    def make_on_model(self):
        def on_model(m):
            for atom in m.symbols(atoms=True):
                if atom.name == "at" and len(atom.arguments) == 3:
                    s, x, y = [(n.number if n.type == clingo.SymbolType.Number else str(n)) for n in atom.arguments]
                    self.solution.append((s, x, y))
            return False
        return on_model
    
    def solver(self):
        self.control_object.load("../Encoding/robotknowledge.lp")
        self.control_object.load("../Encoding/planner.lp")
        self.control_object.ground([("base", [])])
        on_model = self.make_on_model()
        t = 0
        while True:
            t += 1
            self.control_object.ground([("step", [t])])
            self.control_object.ground([("check", [t])])
            self.control_object.release_external(clingo.Function("query", [t-1]))
            self.control_object.assign_external(clingo.Function("query", [t]), True)
            if self.control_object.solve(on_model=on_model).satisfiable:
                break
            
            