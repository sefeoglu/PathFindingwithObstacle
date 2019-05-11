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
        
        self.robotKnowledgeObject = RobotKnowledge.RobotKnowledge()
        self.realEnvironment = Board.Board()
        self.robotKnowledgeObject.dimension =  sqrt(len(self.realEnvironment.field))
        
    def exploreEnvironment(self):
        
#        get robot position from the environment
        self.robotKnowledgeObject.robot.append(self.realEnvironment.robot[0])
        self.robotKnowledgeObject.robotField.append(self.realEnvironment.robot[0])
        robotNeighbour = self.findNeighbour(self.robotKnowledgeObject.robot[0]) 
        self.robotKnowledgeObject.robotField += robotNeighbour

        newNeighbour = []
        while len(self.realEnvironment.field) != len(self.robotKnowledgeObject.robotField):
            for neighbour in robotNeighbour:
                 
                if  self.realEnvironment.blocked  != neighbour:
                     
                    self.addNewFrontier(self.robotKnowledgeObject.robot[0],neighbour)

                   
                    if len(self.frontier) > 0:
                       
                        robotKnowledge = self.knowledgetoString("robot", self.robotKnowledgeObject.robot)
                        robotKnowledge += self.knowledgetoString("field", robotNeighbour)
                        robotKnowledge += self.knowledgetoString("field", self.robotKnowledgeObject.robot)
                        if len(self.robotKnowledgeObject.robotObstacle) > 0 :
                             robotKnowledge += self.knowledgetoString("obstacle", self.robotKnowledgeObject.robotObstacle)
                        for goal in self.frontier:
                            
                            if newNeighbour.count(goal)== 0:
                                newNeighbour.append(goal)
                                goalstr= self.knowledgetoString("goal", [goal])
    
                                robotKnowledge += self.knowledgetoString("field", [goal])
                                robotKnowledge += goalstr
                                self.robotKnowledgeObject.addKnowledge(robotKnowledge)
                            
                                solverObject = Solver.Solver()
                                solverObject.solver()
                            
    
                                if self.robotKnowledgeObject.robotField.count(goal) == 0:
                                    if len(solverObject.solution)!=0:
                                        self.robotKnowledgeObject.robotField.append(goal)
                                        if self.realEnvironment.blocked.count(goal)!=0:
                                            self.robotKnowledgeObject.robotObstacle.append(goal)
                                            obstaclestr = self.knowledgetoString("obstacle",[goal])
                                            robotKnowledge = robotKnowledge.replace(goalstr,obstaclestr)

                                        if self.realEnvironment.goal.count(goal) != 0:
                                            self.robotKnowledgeObject.robotgoal.append(goal)
                                        if self.realEnvironment.goal.count(goal) == 0 and  self.realEnvironment.blocked.count(goal) == 0:
                                            robotKnowledge = robotKnowledge.replace(goalstr,"")
        
            robotNeighbour= []
            robotNeighbour = newNeighbour
        solverObject = Solver.Solver()
        solverObject.solver()
        print(solverObject.solution)
           

        
    def addNewFrontier(self,robotPosition, neighbourPosition):
#         robotun öğrenecekleri
        self.frontier = []
        if neighbourPosition[0]-1 > 0 and (robotPosition[0] != neighbourPosition[0]-1 or robotPosition[1] != neighbourPosition[1] ):
            self.frontier.append((neighbourPosition[0]-1, neighbourPosition[1]))
        if neighbourPosition[0]+1 <= self.robotKnowledgeObject.dimension and (robotPosition[0] != neighbourPosition[0]+1 or robotPosition[1] != neighbourPosition[1]) :
            self.frontier.append((neighbourPosition[0]+1, neighbourPosition[1]))
        if neighbourPosition[1]-1 > 0 and (robotPosition[0] != neighbourPosition[0] or robotPosition[1] != neighbourPosition[1]-1):
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