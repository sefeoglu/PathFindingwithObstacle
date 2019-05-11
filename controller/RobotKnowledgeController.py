# -*- coding: utf-8 -*-
"""
Created on Sun May  5 21:29:52 2019

@author: sefika
"""
import sys
sys.path.append("../model/")
import Solver
import Board
import RobotKnowledge
from math import sqrt

# =============================================================================
# Sefika's OOP
# =============================================================================
class RobotKnowledgeController:
    def __init__(self):
        self.frontier = []
        self.solverObject = Solver.Solver()
        self.robotKnowledgeObject = RobotKnowledge.RobotKnowledge()
        self.realEnvironment = Board.Board()
        self.robotKnowledgeObject.dimension =  sqrt(len(self.realEnvironment.field))
        
    def exploreEnvironment(self):
        
        self.robotKnowledgeObject.robot = self.realEnvironment.robot[0]
        
        robotKnowledge = self.knowledgetoString("robot", self.realEnvironment.robot)
        robotNeighbour = self.findNeighbour(self.robotKnowledgeObject.robot)
        robotKnowledge += self.knowledgetoString("field", robotNeighbour)
        robotKnowledge += self.knowledgetoString("field", self.realEnvironment.robot)
        self.addNewFrontier(self.robotKnowledgeObject.robot,robotNeighbour[0])
        
        while len(self.frontier) > 0:
            
            
            for goal in self.frontier:
                robotKnowledge += self.knowledgetoString("goal", [goal])
                robotKnowledge += self.knowledgetoString("field", [goal])
                self.robotKnowledgeObject.addKnowledge(robotKnowledge)
                self.solverObject.solver()
                
                if self.robotKnowledgeObject.robotField.count(goal) == 0:
                    if len(self.solverObject.solution)!=0:
                        self.robotKnowledgeObject.robotField.append(goal)
                        if self.realEnvironment.blocked.count(goal)!=0:
                            self.robotKnowledgeObject.robotObstacle.append(goal)
                        elif self.realEnvironment.goal.count(goal) != 0:
                            self.robotKnowledgeObject.robotgoal.append(goal)
            
        
                
            
        
    def addNewFrontier(self,robotPosition, neighbourPosition):
#         robotun öğrenecekleri
        if neighbourPosition[0]-1 > 0 and (robotPosition[0] != neighbourPosition[0]-1 or robotPosition[1] != neighbourPosition[1] ):
            self.frontier.append((neighbourPosition[0]-1, neighbourPosition[1]))
        if neighbourPosition[0]+1 <= self.robotKnowledgeObject.dimension and (robotPosition[0] != neighbourPosition[0]+1 or robotPosition[1] != neighbourPosition[1]) :
            self.frontier.append((neighbourPosition[0]+1, neighbourPosition[1]))
        if neighbourPosition[1]-1 > 0 and (robotPosition[0] != neighbourPosition[0] or (robotPosition[1] != neighbourPosition[1]-1)):
            self.frontier.append((neighbourPosition[0],neighbourPosition[1]-1))
        if neighbourPosition[1]+1 <= self.robotKnowledgeObject.dimension and (robotPosition[0] != neighbourPosition[0] or robotPosition[1] != neighbourPosition[1]+1):
            self.frontier.append((neighbourPosition[0],neighbourPosition[1]+1))
        

        
    def findNeighbour(self,robotPosition):
#        robotun bildikleri kendisi haric--- obstacle control yap
        robotNeighbour = []
        if robotPosition[0]-1 > 0 :
            robotNeighbour.append((robotPosition[0]-1,robotPosition[1]))
        if robotPosition[0]+1 <= self.robotKnowledgeObject.dimension:
            robotNeighbour.append((robotPosition[0]+1,robotPosition[1]))
        if robotPosition[1]-1 > 0:
            robotNeighbour.append((robotPosition[0],robotPosition[1]-1))
        if robotPosition[1]+1 <= self.robotKnowledgeObject.dimension:
            robotNeighbour.append((robotPosition[0],robotPosition[1]+1))
        return robotNeighbour
    
    def knowledgetoString(self, knowledgeType, knowledgelist):
        knowledgeString = ""
        for position in knowledgelist:
            knowledgeString += knowledgeType+"("+str(position[0])+","+str(position[1])+"). "
        return knowledgeString
    

rkc = RobotKnowledgeController()
rkc.exploreEnvironment()