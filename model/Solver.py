# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:47:33 2019

@author: sefika
"""
import clingo
# =============================================================================
# Sefika's OOP
# =============================================================================
class Solver:

    def __init__(self):
        
        self.solution = []
        self.control_object = clingo.Control()
        
        
    def make_on_model(self):
        def on_model(m):
            for atom in m.symbols(atoms=True):
                if atom.name == "at" and len(atom.arguments) == 3:
                    x, y, s = [(n.number if n.type == clingo.SymbolType.Number else str(n)) for n in atom.arguments]
                    self.solution.append((x, y, s))
            return False
        return on_model
    
    def solver(self,knowledgeFile = "../Encoding/robotknowledge.lp", plannerFile = "../Encoding/planner.lp"):
        
        self.control_object.add("check", ["k"], "#external query(k).")
        self.control_object.load(knowledgeFile)
        self.control_object.load(plannerFile)
        self.control_object.ground([("base", [])])
        on_model = self.make_on_model()

        t = 0
        self.solution = []
        while True:
            t += 1
            self.control_object.ground([("step", [t])])
            self.control_object.ground([("check", [t])])
            self.control_object.release_external(clingo.Function("query", [t-1]))
            self.control_object.assign_external(clingo.Function("query", [t]), True)
            if self.control_object.solve(on_model=on_model).satisfiable:
                break
