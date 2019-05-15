"""Robot Knowledge Controller"""
import sys
from math import sqrt
sys.path.append("../model/")
import Solver
import Board
import RobotKnowledge

# =============================================================================
# Sefika's OOP
# =============================================================================
class RobotKnowledgeController:
    """Sefikanın programı """
    def __init__(self):
        self.frontier = []
        self.robot_knowledge_object = RobotKnowledge.RobotKnowledge()
        self.real_environment = Board.Board()
        self.robot_knowledge_object.dimension = sqrt(len(self.real_environment.field))
    def explore_environment(self):
        """Explore the environment"""
        self.robot_knowledge_object.robot.append(self.real_environment.robot[0])
        self.robot_knowledge_object.robotField.append(self.real_environment.robot[0])
        robot_neighbour_list = self.find_neighbour(self.robot_knowledge_object.robot[0])
        self.robot_knowledge_object.robotField += robot_neighbour_list
        for neighbour in robot_neighbour_list:
            if self.real_environment.blocked.count(neighbour) != 0:
                self.robot_knowledge_object.robotObstacle.append(neighbour)
        new_neighbour_list = []
        while self.real_environment.goal != self.robot_knowledge_object.robotgoal:
            for neighbour in robot_neighbour_list:
                if all(elem in self.real_environment.blocked for elem in robot_neighbour_list):
                    return "There is no way to goal from robot because of the blocks"

                if  self.real_environment.blocked.count(neighbour) == 0:
                    self.add_new_frontier(self.robot_knowledge_object.robot[0], neighbour)
                    robot_knowledge = self.knowledge_string("robot", self.
                                                            robot_knowledge_object.
                                                            robot)
                    robot_knowledge += self.knowledge_string("field", self.
                                                             robot_knowledge_object.
                                                             robotField)
                    robot_knowledge += self.knowledge_string("obstacle", self.
                                                             robot_knowledge_object.
                                                             robotObstacle)
                    self.explore_frontierlist(robot_knowledge, new_neighbour_list)

            robot_neighbour_list = []
            robot_neighbour_list = new_neighbour_list
        robot_knowledge = self.knowledge_string("robot", self.robot_knowledge_object.robot)
        robot_knowledge += self.knowledge_string("field", self.robot_knowledge_object.robotField)
        robot_knowledge += self.knowledge_string("obstacle", self.
                                                 robot_knowledge_object.robotObstacle)
        robot_knowledge += self.knowledge_string("goal", self.robot_knowledge_object.robotgoal)
        self.robot_knowledge_object.addKnowledge(robot_knowledge)
        solver_object = Solver.Solver()
        solver_object.solver()

    def add_new_frontier(self, robot_position, neighbour_position):
        """Find the nodes for exploring"""
        self.frontier = []
        if neighbour_position[0]-1 > 0 and (robot_position[0] != neighbour_position[0]-1 or \
                             robot_position[1] != neighbour_position[1]):
            self.frontier.append((neighbour_position[0]-1, neighbour_position[1]))
        if neighbour_position[0]+1 <= self.robot_knowledge_object.dimension and \
        (robot_position[0] != neighbour_position[0]+1 or \
         robot_position[1] != neighbour_position[1]):
            self.frontier.append((neighbour_position[0]+1, neighbour_position[1]))
        if neighbour_position[1]-1 > 0 and (robot_position[0] != neighbour_position[0] or \
                             robot_position[1] != neighbour_position[1]-1):
            self.frontier.append((neighbour_position[0], neighbour_position[1]-1))
        if neighbour_position[1]+1 <= self.robot_knowledge_object.dimension and \
        (robot_position[0] != neighbour_position[0] or \
         robot_position[1] != neighbour_position[1]+1):
            self.frontier.append((neighbour_position[0], neighbour_position[1]+1))
    def find_neighbour(self, robot_position):
        """Find neighbour of robot"""
        robot_neighbour_list = []
        if robot_position[0]-1 > 0:
            robot_neighbour_list.append((robot_position[0]-1, robot_position[1]))
        if robot_position[0]+1 <= self.robot_knowledge_object.dimension:
            robot_neighbour_list.append((robot_position[0]+1, robot_position[1]))
        if robot_position[1]-1 > 0:
            robot_neighbour_list.append((robot_position[0], robot_position[1]-1))
        if robot_position[1]+1 <= self.robot_knowledge_object.dimension:
            robot_neighbour_list.append((robot_position[0], robot_position[1]+1))
        return robot_neighbour_list
    def knowledge_string(self, knowledge_type, knowledgelist):
        """Convert to String"""
        knowledge_string = ""
        for position in knowledgelist:
            knowledge_string += knowledge_type+"("+str(position[0])+","+str(position[1])+"). "
        return knowledge_string
    def replace_goal(self, robot_knowledge, goal, temporary_goalstr):
        """Replace custom"""
        if self.real_environment.blocked.count(goal) != 0:
            self.robot_knowledge_object.robotObstacle.append(goal)
            obstaclestr = self.knowledge_string("obstacle", [goal])
            robot_knowledge = robot_knowledge.replace(temporary_goalstr,
                                                      obstaclestr)
        if self.real_environment.goal.count(goal) != 0:
            self.robot_knowledge_object.robotgoal.append(goal)
        if self.real_environment.goal.count(goal) == 0 and  \
        self.real_environment.blocked.count(goal) == 0:
            robot_knowledge = robot_knowledge.replace(temporary_goalstr, "")
        return robot_knowledge
    def explore_frontierlist(self, robot_knowledge, new_neighbour_list):
        """Explore"""
        for goal in self.frontier:
            if new_neighbour_list.count(goal) == 0 and \
            self.robot_knowledge_object.robotObstacle.count(goal) == 0 and \
            self.robot_knowledge_object.robotgoal.count(goal) == 0 and \
            self.robot_knowledge_object.robotField.count(goal) == 0:
                new_neighbour_list.append(goal)
                temporary_goalstr = self.knowledge_string("goal", [goal])
                robot_knowledge += self.knowledge_string("field", [goal])
                robot_knowledge += temporary_goalstr
                self.robot_knowledge_object.addKnowledge(robot_knowledge)
                solver_object = Solver.Solver()
                solver_object.solver()
                if self.robot_knowledge_object.robotField.count(goal) == 0 and \
                solver_object.solution.__len__() != 0:
                    self.robot_knowledge_object.robotField.append(goal)
                    robot_knowledge = self.replace_goal(robot_knowledge,
                                                        goal,
                                                        temporary_goalstr)
            if self.real_environment.goal == self.robot_knowledge_object.robotgoal:
                break
