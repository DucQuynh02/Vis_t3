import numpy as np
import random as rd
from numba import njit, jit
from numba.typed import List
import sys, os
from setup import SHORT_PATH
import importlib.util
game_name = sys.argv[1]

def setup_game(game_name):
    spec = importlib.util.spec_from_file_location('env', f"{SHORT_PATH}Base/{game_name}/env.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

env = setup_game(game_name)

getActionSize = env.getActionSize
getStateSize = env.getStateSize
getAgentSize = env.getAgentSize

getValidActions = env.getValidActions
getReward = env.getReward

def DataAgent():
    return List([np.zeros((1,1))])


@njit()
def Test(state, per):
    ValidActions = getValidActions(state)
    ValidActions = np.where(ValidActions==1)[0]
    returnAction = -1

   
    if state[26] > 1:
        if (state[11] > 0 or state[25] / (state[26] - 1) > 4.4) and (state[25] / (state[26] - 1) > 2.2):
            if 6 in ValidActions:
                returnAction = 6
    
    if returnAction == -1:
        if ValidActions[0] in range(15,27):
            for i in [6,7,8,9,10,3,4,5,0,1,2,11] :
                if i +15 in ValidActions:
                    returnAction = i+15
                    break
        elif ValidActions[0] in range(39,51):
            for i in [6,7,8,9,10,3,4,5,0,1,2,11] :
                if i +39 in ValidActions:
                    returnAction = i+39
        elif ValidActions[0] in range(27,39):
            for i in [6,7,8,9,10,3,4,5,0,1,2,11] :
                if i +27 in ValidActions:
                    returnAction = i+27
        elif ValidActions[0] in range(11,15):
            idx = np.argmax(state[87:91])
            if idx + 11 in ValidActions:
                returnAction = idx + 11         
        elif ValidActions[0] in range(1,10):
            for i in [5,3,2,1]:
                if i in ValidActions:
                    returnAction = i
                    break
        elif 0 in ValidActions:
            nopeCard = np.where(state[72:82]== 1)[0][0]
            if (nopeCard == 1 and state[26] <= 3 and state[25] <= 11) :
                returnAction = 0
            elif 10 in ValidActions:
                returnAction = 10


    if len(np.where(state[28:41] == 1)[0]) > 0:
        if np.where(state[28:41] == 1)[0][0] == 12:
            if 1 in ValidActions:
                returnAction = 1
            elif 2 in ValidActions:
                returnAction = 2
            elif 4 in ValidActions:
                returnAction = 4
            else: returnAction = -1

        elif 6 in ValidActions:
            returnAction = 6

    DiffCards = np.sum(np.where(state[6:11] > 0,1,0))
    DiffCards2 = DiffCards
    for i in [0, 2, 3, 4]:
        if state[i] > 0:
            DiffCards2 += 1
    # print(DiffCards)
    if DiffCards >= 5 and 9 in ValidActions and state[23] > 0 and state[25] < 20:
        returnAction = 9
    elif 8 in ValidActions and np.max(state[6:11]) + state[6] >= 3 and state[25] < 20:
        returnAction = 8
    elif np.max(state[6:11]) >= 2 and 7 in ValidActions and state[25] < 20:
        returnAction = 7
    elif 9 in ValidActions and state[23] > 0 and state[11] == 0 and DiffCards2 >= 5:
        returnAction = 9

    if returnAction == -1:
        returnAction = ValidActions[np.random.randint(len(ValidActions))]
    #     print("random")

    # print("My cards: ", state[0:12])
    # print("Discard Pile's cards and num remain: ", state[12:25], state[25])
    # print("num Player: ", state[26])
    # print("See the future:", np.where(state[28:41]==1), np.where(state[41:54]==1), np.where(state[54:67]==1))
    # print(state[28:41])
    # print(state[41:54])
    # print(state[54:67])
    # print("num Card to draw: ", state[71])
    # print("Main player previous action: ",np.where(state[72:82]== 1))
    # print("Num other cards: ", state[87:91])
    # print("Action: ", ValidActions, returnAction)
    # print()
    # print()

    return returnAction, per