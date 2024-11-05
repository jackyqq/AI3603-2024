"""
This module defines various agent classes for a game, including random agents, greedy agents.
You need to implement your own agent in the YourAgent class using minimax algorithms.

Classes:
    Agent: Base class for all agents.
    RandomAgent: Agent that selects actions randomly.
    SimpleGreedyAgent: Greedy agent that selects actions based on maximum vertical advance.
    YourAgent: Placeholder for user-defined agent.

Class Agent:
    Methods:
        __init__(self, game): Initializes the agent with the game instance.
        getAction(self, state): Abstract method to get the action for the current state.
        oppAction(self, state): Abstract method to get the opponent's action for the current state.

Class RandomAgent(Agent):
    Methods:
        getAction(self, state): Selects a random legal action.
        oppAction(self, state): Selects a random legal action for the opponent.

Class SimpleGreedyAgent(Agent):
    Methods:
        getAction(self, state): Selects an action with the maximum vertical advance.
        oppAction(self, state): Selects an action with the minimum vertical advance for the opponent.

Class YourAgent(Agent):
    Methods:
        getAction(self, state): Placeholder for user-defined action selection.
        oppAction(self, state): Placeholder for user-defined opponent action selection.
"""

import random, re, datetime
import board
from queue import PriorityQueue


class Agent(object):
    def __init__(self, game):
        self.game = game
        self.action = None

    def getAction(self, state):
        raise Exception("Not implemented yet")

    def oppAction(self, state):
        raise Exception("Not implemented yet")


class RandomAgent(Agent):

    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)

    def oppAction(self, state):
        legal_actions = self.game.actions(state)
        self.opp_action = random.choice(legal_actions)


class SimpleGreedyAgent(Agent):
    # a one-step-lookahead greedy agent that returns action with max vertical advance

    def getAction(self, state):

        legal_actions = self.game.actions(state)

        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        if player == 1:
            max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if action[0][0] - action[1][0] == max_vertical_advance_one_step]
        else:
            max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if action[1][0] - action[0][0] == max_vertical_advance_one_step]
        self.action = random.choice(max_actions)

    def oppAction(self, state):
        legal_actions = self.game.actions(state)

        self.opp_action = random.choice(legal_actions)

        player = self.game.player(state)
        if player == 1:
            min_vertical_advance_one_step = min([action[0][0] - action[1][0] for action in legal_actions])
            min_actions = [action for action in legal_actions if action[0][0] - action[1][0] == min_vertical_advance_one_step]
        else:
            min_vertical_advance_one_step = min([action[1][0] - action[0][0] for action in legal_actions])
            min_actions = [action for action in legal_actions if action[1][0] - action[0][0] == min_vertical_advance_one_step]

        self.opp_action = random.choice(min_actions)


class YourAgent(Agent):
    def getAction(self, state):
        depth = 2
        alpha = float('-inf')
        beta = float('inf')
        self.action = random.choice(self.max_action(state, depth, alpha, beta)[1])
        # self.action = self.max_action(state, depth, alpha, beta)[1][0]

    def oppAction(self, state):
        depth = 2
        alpha = float('-inf')
        beta = float('inf')
        # self.opp_action = random.choice(self.min_action(state, depth, alpha, beta)[1])
        self.opp_action = self.min_action(state, depth, alpha, beta)[1][0]

    def if_Win(self, player):
        piece_rows = self.game.board.piece_rows
        size = self.game.board.size
        if player == 1:
            for row in range(1, piece_rows + 1):
                for col in range(1, self.game.board.getColNum(row) + 1):
                    if row == 2 and self.game.board.board_status[(row, col)] == 3:
                        continue
                    elif self.game.board.board_status[(row, col)] == 1:
                        continue
                    else:
                        return False
            return True

        else:
            for row in range(size * 2 - piece_rows, size * 2):
                for col in range(1, self.game.board.getColNum(row) + 1):
                    if row == size * 2 - piece_rows + 2 and self.game.board.board_status[(row, col)] == 4:
                        continue
                    elif self.game.board.board_status[(row, col)] == 2:
                        continue
                    else:
                        return False
            return True

    def max_action(self, state, depth, alpha, beta, action = None):
        if depth == 0:
            return self.evaluate_state(state, action), []

        legal_actions = self.game.actions(state)
        value = float('-inf')
        best_action = []
        priority_queue = PriorityQueue()

        for action in legal_actions:
            new_state = self.game.succ(state, action)
            new_value, _ = self.min_action(new_state, depth - 1, alpha, beta, action)
            priority_queue.put((-new_value, action))

        while not priority_queue.empty():
            new_value, action = priority_queue.get()
            new_value = -new_value

            if new_value > value:
                value = new_value
                best_action = [action]
            if new_value == value:
                best_action.append(action)

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return value, best_action

    def min_action(self, state, depth, alpha, beta, action = None):
        if depth == 0:
            return self.evaluate_state(state, action), []

        legal_actions = self.game.actions(state)
        # print(legal_actions[0:5])
        value = float('inf')
        best_action = []
        priority_queue = PriorityQueue()

        for action in legal_actions:
            new_state = self.game.succ(state, action)
            new_value, _ = self.max_action(new_state, depth - 1, alpha, beta, action)
            priority_queue.put((new_value, action))

        while not priority_queue.empty():
            new_value, action = priority_queue.get()

            if new_value < value:
                value = new_value
                best_action = [action]
            if new_value == value:
                best_action.append(action)

            beta = min(beta, value)
            if beta <= alpha:
                break

        return value, best_action

    def evaluate_state(self, state, action):

        player = self.game.player(state)
        board = state[1]
        size = board.size
        piece_rows = board.piece_rows
        special_rows = [2, size * 2 - piece_rows + 2]
        my_piece_pos = board.getPlayerPiecePositions(player)
        opp_piece_pos = board.getPlayerPiecePositions(3 - player)

        # r_1 = 25
        # r_2 = 9
        # r_3, r_4 = 3, 1
        # r_5 = 50

        r_1 = 21
        r_2 = 7
        r_3, r_4 = 8, 3
        r_5 = 50

        my_sum, opp_sum = 0, 0 

        
        for pos in my_piece_pos:
            if player == 1:
                # First consider the rows with special pieces
                if board.board_status[pos] == 3:
                    my_sum += -abs(special_rows[0] - pos[0]) * r_1
                else:
                    my_sum += -pos[0] * r_2

                # Then consider the columns, hope to get the pieces to the center
                if board.board_status[pos] == 3:
                    my_sum -= abs((self.game.board.getColNum(pos[0])+1)/2 - pos[1]) * r_3
                else:
                    my_sum -= abs((self.game.board.getColNum(pos[0])+1)/2 - pos[1]) * r_4

                # When other pieces occupy the position of special pieces, the value should be decreased
                if board.board_status[(special_rows[0], 1)] == 1:
                    my_sum -= 100
                if board.board_status[(special_rows[0], 2)] == 1:
                    my_sum -= 100

                # When the oppent's pieces block mine, we can choose to move them
                if pos[0] <= 2*size - 1 and pos[0] >= 2*size - piece_rows + 1:
                    my_sum -= 10 * (pos[0] - 2*size + piece_rows)
                    
            else:
                if board.board_status[pos] == 4:
                    my_sum += -abs(special_rows[1] - pos[0]) * r_1
                else:
                    my_sum += pos[0] * r_2
                
                if board.board_status[pos] == 4:
                    my_sum -= abs((self.game.board.getColNum(pos[0])+1)/2 - pos[1]) * r_3
                else:
                    my_sum -= abs((self.game.board.getColNum(pos[0])+1)/2 - pos[1]) * r_4

                if board.board_status[(special_rows[1], 1)] == 2:
                    my_sum -= 100
                if board.board_status[(special_rows[1], 2)] == 2: 
                    my_sum -= 100

                if pos[0] <= piece_rows and pos[0] >= 1:
                    my_sum -= 10 * (piece_rows - pos[0] + 1)
        
        for pos in opp_piece_pos:
            if player == 1:
                if board.board_status[pos] == 4:
                    opp_sum += -abs(special_rows[1] - pos[0]) * r_1
                else:
                    opp_sum += pos[0] * r_2

                if board.board_status[pos] == 4:
                    opp_sum -= abs(self.game.board.getColNum(pos[0])//2 - pos[1]) * r_3
                else:
                    opp_sum -= abs(self.game.board.getColNum(pos[0])//2 - pos[1]) * r_4

            else:
                if board.board_status[pos] == 3:
                    opp_sum += -abs(special_rows[0] - pos[0]) * r_1
                else:
                    opp_sum += -pos[0] * r_2

                if board.board_status[pos] == 3:
                    opp_sum -= abs(self.game.board.getColNum(pos[0])//2 - pos[1]) * r_3
                else:
                    opp_sum -= abs(self.game.board.getColNum(pos[0])//2 - pos[1]) * r_4

        
        # for pos in my_piece_pos:
        #     if player == 1:
        #         if board.board_status[pos] == 3:
        #             my_sum -= abs(self.game.board.getColNum(pos[0])//2 - pos[1]) * r_3
        #         else:
        #             my_sum -= abs(self.game.board.getColNum(pos[0])//2 - pos[1]) * r_4
        #     else:
        #         if board.board_status[pos] == 4:
        #             my_sum -= abs(self.game.board.getColNum(pos[0])//2 - pos[1]) * r_3
        #         else:
        #             my_sum -= abs(self.game.board.getColNum(pos[0])//2 - pos[1]) * r_4

        # for pos in opp_piece_pos:
        #     if player == 1:
        #         if board.board_status[pos] == 4:
        #             opp_sum -= abs(self.game.board.getColNum(pos[0])//2 - pos[1]) * r_3
        #         else:
        #             opp_sum -= abs(self.game.board.getColNum(pos[0])//2 - pos[1]) * r_4
        #     else:
        #         if board.board_status[pos] == 3:
        #             opp_sum -= abs(self.game.board.getColNum(pos[0])//2 - pos[1]) * r_3
        #         else:
        #             opp_sum -= abs(self.game.board.getColNum(pos[0])//2 - pos[1]) * r_4
        
        
        # for pos in my_piece_pos:
        #     if player == 1:
        #         if board.board_status[(special_rows[0], 1)] == 1:
        #             my_sum -= 100
        #         if board.board_status[(special_rows[0], 2)] == 1:
        #             my_sum -= 100
        #     else:
        #         if board.board_status[(special_rows[1], 1)] == 2:
        #             my_sum -= 100
        #         if board.board_status[(special_rows[1], 2)] == 2: 
        #             my_sum -= 100
        
        # Solution to the stuck situation, 
        if action != None:
            board_count = {}
            for row in range(1, size * 2 + 1):
                for col in range(1, board.getColNum(row) + 1):
                    if (row, col) in board.board_status:
                        if board.board_status[(row, col)] in board_count:
                            board_count[action[1]] += 1
                        else:
                            board_count[action[1]] = 1
            
            if board_count[action[1]] > 3:
                my_sum -= r_5 * (board_count[pos]-3)

        if self.if_Win(player):
            return 66666
        elif self.if_Win(3-player):
            return -66666
        else:
            return my_sum - opp_sum

    