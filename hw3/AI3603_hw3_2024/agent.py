# -*- coding:utf-8 -*-
import math, os, time, sys
import numpy as np
import gym
##### START CODING HERE #####
# This code block is optional. You can import other libraries or define your utility functions if necessary.

##### END CODING HERE #####

# ------------------------------------------------------------------------------------------- #

class SarsaAgent(object):
    ##### START CODING HERE #####
    def __init__(self, all_actions):
        """initialize the agent. Maybe more function inputs are needed."""
        self.all_actions = all_actions
        self.epsilon = 1.0
        self.alpha = 0.1
        self.gamma = 0.9
        self.q_table = np.zeros((48, 4)) # 48 states, 4 actions

    def choose_action(self, observation):
        """choose action with epsilon-greedy algorithm."""
        if np.random.rand() < self.epsilon:
            action = np.random.choice(self.all_actions)
        else:
            action = np.argmax(self.q_table[observation])
        return action
    
    def learn(self, s, a, r, s_, a_):
        """learn from experience"""

        predict = self.q_table[s][a]
        target = r + self.gamma * self.q_table[s_][a_]
        self.q_table[s][a] += self.alpha * (target - predict)

        # time.sleep(0.5)
        print("(ﾉ｀⊿´)ﾉ")
        return False
    
    def your_function(self, params):
        """You can add other functions as you wish."""
        return None

    ##### END CODING HERE #####


class QLearningAgent(object):
    ##### START CODING HERE #####
    def __init__(self, all_actions):
        """initialize the agent. Maybe more function inputs are needed."""
        self.all_actions = all_actions
        self.epsilon = 1.0
        self.alpha = 0.1
        self.gamma = 0.9
        self.q_table = np.zeros((48, 4)) # 48 states, 4 actions

    def choose_action(self, observation):
        """choose action with epsilon-greedy algorithm."""
        if np.random.rand() < self.epsilon:
            action = np.random.choice(self.all_actions)
        else:
            action = np.argmax(self.q_table[observation])
        return action
    
    def learn(self, s, a, r, s_):
        """learn from experience"""
        predict = self.q_table[s][a]
        target = r + self.gamma * np.max(self.q_table[s_])
        self.q_table[s][a] += self.alpha * (target - predict)

        # time.sleep(0.5)
        print("(ﾉ｀⊿´)ﾉ")
        return False
    
    def your_function(self, params):
        """You can add other functions as you wish."""
        return None

    ##### END CODING HERE #####
    
    

class Dyna_QAgent(object):
    ##### START CODING HERE #####
    def __init__(self, all_actions):
        """initialize the agent. Maybe more function inputs are needed."""
        self.all_actions = all_actions
        self.epsilon = 1.0
        self.alpha = 0.1
        self.gamma = 0.9
        self.q_table = np.zeros((48, 4))
        self.model = {}

    def choose_action(self, observation):
        """choose action with epsilon-greedy algorithm."""
        if np.random.rand() < self.epsilon:
            action = np.random.choice(self.all_actions)
        else:
            action = np.argmax(self.q_table[observation])
        return action
    
    def learn(self, s, a, r, s_):
        """learn from experience"""
        predict = self.q_table[s][a]
        target = r + self.gamma * np.max(self.q_table[s_])
        self.q_table[s][a] += self.alpha * (target - predict)
        self.model[(s, a)] = (r, s_)

        # time.sleep(0.5)
        print("(ﾉ｀⊿´)ﾉ")
        return False
    
    def planning(self, s, a):
        """You can add other functions as you wish."""
        r, s_ = self.model[(s, a)]
        predict = self.q_table[s][a]
        target = r + self.gamma * np.max(self.q_table[s_])
        self.q_table[s][a] += self.alpha * (target - predict)

        return False

    def random_get(self):
        s = np.random.randint(48)
        a = np.random.choice(self.all_actions)
        return s, a
    ##### END CODING HERE #####
