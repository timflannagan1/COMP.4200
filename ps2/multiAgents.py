# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

        # Extract information from the GameState (initially not used in starter code)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"

        """
        Current problems/To-Do:
        [x] pacman constantly stopping in-place
        [x] use manhattanDistance instead of manual abs
        [ ] implement linear evaluation function
        [ ] implement capsules
        [ ] stop pacman bounces around in the same spot when food is near walls
        [ ] discourage going opposite direction from far away food
        [ ] fix returning only calculated_score without constantly losing
        """

        calculated_score = 0
        closest_food = None

        # iterate through the list of food to determine the closest food position
        for food in newFood.asList():
            distance_to_food = abs(newPos[0] - food[0]) + abs(newPos[1] - food[1])

            if not closest_food:
                closest_food = distance_to_food
            elif (distance_to_food < closest_food):
                closest_food = distance_to_food

        # play around with weights
        if (closest_food < 1):
            calculated_score += 35
        elif (closest_food < 5):
            calculated_score += 25
        else:
            calculated_score += 10

        # had a problem where pacman would constantly stop in place
        if action == Directions.STOP:
            calculated_score -= 20

        # discourage going to the same location as the ghost
        if (newPos[0] == newGhostStates[0].getPosition() and action == newGhostStates[0].getDirection()):
            calculated_score -= 50
        elif (newPos[0] == newGhostStates[0].getPosition()):
            calculated_score -= 30

        return calculated_score + successorGameState.getScore()

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
        """
        "*** YOUR CODE HERE ***"


        """
        Note: should use self.depth, self.evaluationFunction
        """

        def min_value(game_state, agent_index):
            # check if state is terminal
            if game_state.isWin() or game_state.isLose() or self.depth == 0:
                return self.evaluationFunction(game_state)

            # assign the value to be the worst possible case for MIN
            v = float('inf')
            best_move = None
            # print('>> Min from driver: {}'.format(game_state.state))
            #
            # print('Min was passed index {}\n'.format(agent_index))

            for move in game_state.getLegalActions(agent_index):
                # print('MIN: Currently looking at {} in min: '.format(move))
                # print('MIN: Current agent index {}'.format(agent_index))
                current_successor = game_state.generateSuccessor(agent_index, move)
                # print('min: {}'.format(current_successor.state))
                current_score = max_value(current_successor, agent_index + 1)

                if not best_move:
                    best_move = move

                # print('MIN: Current v is {}'.format(v))

                # check if there's a smaller value returned from MAX
                if current_score < v:
                    # print("MIN: Update min v ({}) with {}".format(v, current_score))
                    v = current_score
                    best_move = move

            # print('MIN: Returning V: {}'.format(v))
            return v

        def max_value(game_state, agent_index):
            # check if state is terminal
            if game_state.isWin() or game_state.isLose() or self.depth == 0:
                return self.evaluationFunction(game_state)

            # assign the value to be the worst possible case for MAX
            v = float('-inf')
            best_move = None

            # print('Max was passed index {}\n'.format(agent_index))
            # print('Max was passed the legal moves: {}'.format(game_state.getLegalActions()))
            # print('Max Current depth {}'.format(self.depth))


            for move in game_state.getLegalActions():
                # print('>> Currently looking at {} in max: '.format(move))
                # print('>> Current agent {}'.format(agent_index))

                current_successor = game_state.generateSuccessor(0, move)
                # print('max: {}'.format(current_successor.state))
                current_score = min_value(current_successor, agent_index + 1)

                if not best_move:
                    best_move = move

                if current_score > v:
                    # print("Update max v ({}) with {}".format(v, current_score))
                    v = current_score
                    best_move = move

            return v

        """ We want to find the maximum scored state return by MIN"""
        available_moves = gameState.getLegalActions()
        v = float("-inf")
        best_move = available_moves[0]
        # print('>>>>> Number of agents {}'.format(gameState.getNumAgents()))

        # iterate throughout the list of available moves
        for move in available_moves:
            print('>>>> Before v: {}'.format(v))

            current_successor = gameState.generateSuccessor(0, move)
            print('DRIVER: {}'.format(current_successor.state))
            current_score = min_value(current_successor, 1)

            if current_score > v:
                v = current_score
                best_move = move

            print('>>>> After v: {}'.format(v))


        print('>> Returning {}'.format(best_move))
        return best_move




        # start at depth 0 and pacman index (0)
        # return minimax(gameState, 0, 0)

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
