"""Robot Knowledge Controller"""
import sys
sys.path.append("../model/")
import Solver
import Board
import RobotKnowledge

# =============================================================================
# Sefika's OOP
# =============================================================================
class RobotKnowledgeController:
    """RobotKnowledgeController provides robot to search and find obstacle/s"""
    def __init__(self):
        self.frontier = []
        self.robot_knowledge = ""
        self.robot_knowledge_object = RobotKnowledge.RobotKnowledge()
        self.real_environment = Board.Board()
        self.robot_knowledge_object.dimension = Board.Board().dimension
    def explore_environment(self):
        paths = []
        robot_position = [] 
        robot_position.append(self.real_environment.robot)
        field_list= self.real_environment.field
        self.robot_knowledge_object.robotField.append(field_list)
        self.robot_knowledge_object.robotgoal.append(self.real_environment.goal)
        access_flag= 0
        self.robot_knowledge = self.knowledge_string("field", self.
                                                 robot_knowledge_object.
                                                 robotField)
        self.robot_knowledge += self.knowledge_string("goal", self.robot_knowledge_object.robotgoal)
        temp_str = ""
        while access_flag == 0 :
            
            temp_str= self.knowledge_string("robot",robot_position)
            self.robot_knowledge += temp_str
            self.robot_knowledge_object.addKnowledge(self.robot_knowledge)
            solver_object = Solver.Solver()
            solver_object.solver()
            path = solver_object.solution
            if(solver_object.solution.__len__() != 0):
                check = self.check_obstacle(solver_object.solution)
                
                if check == -1:
                    paths.append((path,robot_position))
                    access_flag = -1
                else:
                    robot_position.clear()
                    robot_position.append([solver_object.solution[check]])
                    paths.append((path[:check+2],path[check+1]))
                    self.robot_knowledge = self.robot_knowledge.replace(temp_str, "")
              
            else:
                paths.append(((-1,-1,-1),(-1,-1,-1)))
                break
        robot_position.clear()
        robot_position.append(self.real_environment.robot)
        real_robot_position = self.knowledge_string("robot",robot_position)
        self.robot_knowledge = self.robot_knowledge.replace(temp_str,real_robot_position)
        self.robot_knowledge_object.addKnowledge(self.robot_knowledge)
        
        if(solver_object.solution.__len__() != 0):
            solver_object = Solver.Solver()
            solver_object.solver()   
            path = solver_object.solution
            paths.append((path,(0,0,0)))
        else:
            paths.append(((-1,-1,-1),(-1,-1,-1)))
            print("unsatisfied")
        return paths
    def check_obstacle(self, solution):
        obstacle_list = []
        t = 0;
        for field in solution:
            if self.real_environment.blocked.count((field[0],field[1])) != 0:
                obstacle_list.append((field[0],field[1]))
                break;
            t += 1
        if obstacle_list.__len__() != 0:
            self.robot_knowledge += self.knowledge_string("obstacle",[obstacle_list])
            self.robot_knowledge_object.robotObstacle.append(obstacle_list)
            return t-1
        else :
            return -1
    def knowledge_string(self, knowledge_type, knowledgelist):
        knowledge_string = ""
        for position in knowledgelist[0]:
            knowledge_string += knowledge_type+"("+str(position[0])+","+str(position[1])+"). "
        return knowledge_string

cntrl = RobotKnowledgeController()
cntrl.explore_environment()
