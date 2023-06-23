# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import copy as cp

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


from game import Directions

s = Directions.SOUTH
w = Directions.WEST
e = Directions.EAST
n = Directions.NORTH

Dict = {"South": s, "West": w, "East": e, "North": n}

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def test(problem):
    st = problem.getStartState()
    print("expand:", problem.expand(st))
    print("getaction:", problem.getActions(st))
    #print("getActionCost:", problem.getActionCost(st, w, (st[0] - 1, st[1])))
    print("getNextState:", problem.getNextState(st, w))
    print("getCostOfActionSequence:", [s, s, w, s, w, w, s, w])

best_cost = 38 * 38
move_list = []
ans = []
val = []

def Init():
    ans.clear()
    val.clear()
    move_list.clear()
    for i in range(38 * 38):
        val.append(38 * 38)

def Dfs(pb, pos, cost):
    (x, y) = pos
    if(val[x * 37 + y] < cost):
        return 
    val[x * 37 + y] = cost
    if(pb.isGoalState(pos)):
        if(cost < best_cost):
            ans.insert(0, cp.copy(move_list))
        return 
    act_list = pb.expand(pos)
    for act in act_list:
        move_list.append(act[1])
        Dfs(pb, act[0], cost + act[2])
        move_list.pop()
    return 

def depthFirstSearch(problem):
    # Init()
    # Dfs(problem, problem.getStartState(), 0)
    # ans_Dfs = []
    # for act in ans[0]:
    #     ans_Dfs.append(Dict[act])
    # return ans_Dfs
    # util.raiseNotDefined()
    stk = util.Stack()
    pb = problem
    fst = pb.getStartState()
    stk.push((fst, []))# 位置坐标，路径
    vis = set()#记录状态是否重复
    vis.add(fst)
    while stk.isEmpty() == False:
        now, actions = stk.pop()
        if pb.isGoalState(now):
            return actions
        act_list = pb.expand(now)
        for act in act_list:
            if act[0] in vis:
                continue
            stk.push((act[0], actions + [Dict[act[1]]]))
            vis.add(act[0])

#dfs-test-2 code:
def stack_dfs(problem):
    stk = util.Stack()
    pb = problem
    fst = pb.getStartState()
    stk.push((fst, [])) 
    vis = set()
    vis.add(fst)
    while stk.isEmpty() == False:
        now, actions = stk.pop()
        if pb.isGoalState(now):
            return actions
        act_list = pb.expand(now)
        for act in act_list:
            if act[0] in vis:
                continue
            stk.push((act[0], actions + [Dict[act[1]]]))
            vis.add(act[0])

def Ori(pos):
    return pos[0] * 38 + pos[1]

def breadthFirstSearch(problem):
    Init()
    pb = problem
    q = util.Queue()
    fst = pb.getStartState()
    q.push((fst, [], 0))  # 位置，路径，步数
    vis = set()
    vis.add(fst)
    while q.isEmpty() != True:
        st = q.pop()
        if(pb.isGoalState(st[0])):
            return st[1]
        act_list = pb.expand(st[0])
        for act in act_list:
            if act[0] in vis:
                continue
            vis.add(act[0])
            K = cp.copy(st[1])
            K.append(Dict[act[1]])
            q.push((act[0], cp.copy(K), st[2] + act[2]))
        
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    Init()
    pb = problem
    q = util.PriorityQueue()
    fst = pb.getStartState()
    #print("goal = ", pb.goal)
    q.push((fst, [], 0), heuristic(fst, pb))
    vis = set()
    vis.add(fst)
    # while q.isEmpty() != True:
    #     st = q.pop()
    #     if(pb.isGoalState(st[0])):
    #         return st[1]
    #     act_list = pb.expand(st[0])
    #     for act in act_list:
    #         if val[Ori(act[0])] == 1:
    #             continue
    #         val[Ori(act[0])] = 1
    #         K = cp.copy(st[1])
    #         K.append(Dict[act[1]])
    #         q.push((act[0], cp.copy(K)), Dis(act[0]))#dmd#

    while q.isEmpty() == False:
        st = q.pop()
        if(pb.isGoalState(st[0])):
            return st[1]
        act_list = pb.expand(st[0])
        for act in act_list:
            if act[0] in vis:
                continue
            vis.add(act[0])
            K = cp.copy(st[1])
            K.append(Dict[act[1]])
            q.push((act[0], cp.copy(K), st[2] + act[2]), st[2] + act[2] + heuristic(act[0], pb))
        

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
