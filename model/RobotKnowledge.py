# -*- coding: utf-8 -*-
"""
Created on Sun May  5 20:55:38 2019

@author: sefika
"""
# =============================================================================
#Sefika's OOP
# =============================================================================
class RobotKnowledge:
    def __init__(self):
        self.robotKnowledge = []
        self.robotField = []
        self.robotObstacle = []
        self.robotgoal = []
        self.robot = []
        self.dimension =  0
        
    def addKnowledge(self, robotKnowledgeAtoms):
        f = open("../Encoding/robotknowledge.lp", "w")
        f.write(robotKnowledgeAtoms)
        f.close()
        
    def addGoalforExplore(self):
        print("---")
    def updateRobotKnowledge(self):
        print("---")
        