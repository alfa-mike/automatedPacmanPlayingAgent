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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        """
        print(newFood)
        print(newPos)
        print(newGhostStates)
        print(newScaredTimes)
        """
        "*** YOUR CODE HERE ***"
        foodPos = newFood.asList()
        ghostPos = successorGameState.getGhostPositions()
        food_dist_arr = []
        ghost_dist_arr = []
        cnt = 0
        score = successorGameState.getScore()

        for ele in foodPos:
            dist = manhattanDistance(newPos,ele)
            food_dist_arr.append(dist)

        if len(food_dist_arr)!=0:
            score -= min(food_dist_arr)
        
        for d in food_dist_arr:
                if d<=6:
                    cnt += 1/d
        for ele in ghostPos:
            dist = manhattanDistance(newPos,ele)
            ghost_dist_arr.append(dist)
        
        for d in ghost_dist_arr:
            if d<=2 and d>0:
                cnt-=1/d

        return cnt + score    
        #return score                                      

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def miniMax(state,depth,agentidx):
            if state.getLegalActions(agentidx)==0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state),0
            if self.depth==depth:
                return self.evaluationFunction(state),0
            
            #pacman
            ninfval = float("-inf")
            maxval = ninfval
            if agentidx==0:
                for action in state.getLegalActions(agentidx):
                    nextagentidx = (agentidx+1) % state.getNumAgents()
                    v , a = miniMax(state.generateSuccessor(agentidx,action),depth,nextagentidx)
                    
                    if v>maxval:
                        maxval = v
                        maxaction = action
            if maxval!=ninfval:
                return maxval,maxaction

            #ghosts
            pinfval = float("inf")
            minval = pinfval
            if agentidx!=0:
                for action in state.getLegalActions(agentidx):
                    nextagentidx = (agentidx+1) % state.getNumAgents()
                    if nextagentidx!=0:
                        v , a = miniMax(state.generateSuccessor(agentidx,action),depth,nextagentidx)
                    else:
                        v , a = miniMax(state.generateSuccessor(agentidx,action),depth+1,nextagentidx)

                    if v<minval:
                        minval = v
                        minaction = action
            if minval!=pinfval:
                return minval,minaction

        result = miniMax(gameState,self.index,0)[1]                        
        return result

        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabetaPruning(state,depth,agentidx,a,b):
            if state.getLegalActions(agentidx)==0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state),0
            if self.depth==depth:
                return self.evaluationFunction(state),0
            
            #pacman
            ninfval = float("-inf")
            maxval = ninfval
            if agentidx==0:
                for action in state.getLegalActions(agentidx):
                    nextagentidx = (agentidx+1) % state.getNumAgents()
                    v , act = alphabetaPruning(state.generateSuccessor(agentidx,action),depth,nextagentidx,a,b)
                    
                    if v>maxval:
                        maxval = v
                        maxaction = action
                    if maxval>b:
                        return maxval,maxaction
                    a = max(a,maxval)
            if maxval!=ninfval:
                return maxval,maxaction

            #ghosts
            pinfval = float("inf")
            minval = pinfval
            if agentidx!=0:
                for action in state.getLegalActions(agentidx):
                    nextagentidx = (agentidx+1) % state.getNumAgents()
                    if nextagentidx!=0:
                        v , act = alphabetaPruning(state.generateSuccessor(agentidx,action),depth,nextagentidx,a,b)
                    else:
                        v , act = alphabetaPruning(state.generateSuccessor(agentidx,action),depth+1,nextagentidx,a,b)

                    if v<minval:
                        minval = v
                        minaction = action
                    if minval<a:
                        return minval,minaction
                    b = min(b,minval)
            if minval!=pinfval:
                return minval,minaction

        result = alphabetaPruning(gameState,self.index,0,float("-inf"),float("inf"))[1]                        
        return result
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectiMax(state,depth,agentidx):
            if state.getLegalActions(agentidx)==0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            if self.depth==depth:
                return self.evaluationFunction(state)
            
            #pacman
            ninfval = float("-inf")
            maxval = ninfval
            if agentidx==0:
                for action in state.getLegalActions(agentidx):
                    nextagentidx = (agentidx+1) % state.getNumAgents()
                    v = expectiMax(state.generateSuccessor(agentidx,action),depth,nextagentidx)
                    
                    if v>maxval:
                        maxval = v
                        #maxaction = action
            if maxval!=ninfval:
                return maxval

            #ghosts
            pinfval = float("inf")
            minval = pinfval
            if agentidx!=0:
                sm=0
                for action in state.getLegalActions(agentidx):
                    nextagentidx = (agentidx+1) % state.getNumAgents()
                    if nextagentidx!=0:
                        v  = expectiMax(state.generateSuccessor(agentidx,action),depth,nextagentidx)
                        sm+=v
                    else:
                        v  = expectiMax(state.generateSuccessor(agentidx,action),depth+1,nextagentidx)
                        sm+=v
                minval=float(sm/len(state.getLegalActions(agentidx)))    
            if minval!=pinfval:
                return minval

        ans = []
        
        for move in gameState.getLegalActions(self.index):
            ans.append(expectiMax(gameState.generateSuccessor(self.index,move),self.index,1))                       
        result = gameState.getLegalActions(self.index)[ans.index(max(ans))]
        return result
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    """ YOUR CODE HERE "
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]"""

    extra = 0
    if currentGameState.isWin() :
        extra = 5000
    elif currentGameState.isLose():
        extra =  -5000

    pacmanPosition = currentGameState.getPacmanPosition()

    foodPos = currentGameState.getFood().asList()
    food_dist_arr = []
    for food in foodPos:
        dist = manhattanDistance(pacmanPosition,food)
        food_dist_arr.append(dist)

    food_w = 0
    for dist in food_dist_arr:
        if dist<=2:
            food_w += 20/dist
        elif dist<=6:
            food_w += 10/dist
        else:
            food_w+= 5/dist

    capsulePos = currentGameState.getCapsules()
    capsule_dist_arr = []
    for capsule in capsulePos:
        dist = manhattanDistance(pacmanPosition,capsule)
        capsule_dist_arr.append(dist)
    capsule_w = 0
    for dist in capsule_dist_arr:
        if dist<=2:
            capsule_w+=40/dist
        elif dist<=6:
            capsule_w+=20/dist
        else:
            capsule_w+=4/dist

    ghoststates = currentGameState.getGhostStates()
    activeghost_arr = [] 
    scaredghost_arr = [] 
    for ghost in ghoststates:
        if ghost.scaredTimer==0:
            activeghost_arr.append(ghost)
        else:
            scaredghost_arr.append(ghost) 
    
    activeghost_dist_arr=[]
    for ghost in activeghost_arr:
        dist = manhattanDistance(pacmanPosition,ghost.getPosition())
        activeghost_dist_arr.append(dist)
    activeghost_w=0
    for dist in activeghost_dist_arr:
        if dist == 0:
            return -999
        elif dist<=2:
            activeghost_w+=50/dist
        elif dist<=6:
            activeghost_w+=30/dist
        else:
            activeghost_w+=5/dist
            
    scaredghost_dist_arr=[]
    for ghost in scaredghost_arr:
        dist = manhattanDistance(pacmanPosition,ghost.getPosition())
        scaredghost_dist_arr.append(dist)
    scaredghost_w=0
    for dist in scaredghost_dist_arr:
        if dist<=2:
            scaredghost_w+=100/dist
        elif dist<=6:
            scaredghost_w+=50/dist
        else:
            scaredghost_w+=2/dist
    
    total_w = (food_w + capsule_w + scaredghost_w - activeghost_w + extra)
    result = currentGameState.getScore()
    #if len(food_dist_arr)!=0:
     #   result-=50*min(food_dist_arr)
    result-= 20*len(foodPos)
    result-=10*len(currentGameState.getCapsules())
    result+=total_w
    return result
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
