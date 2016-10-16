import random
import sys
import copy
import re
from math import log
import time
from threading import Thread


# this function creates the initial board configuration and time limit from
# command line
def createBoard():
    if len(sys.argv) < 5:
        print "Too few arguments!"
        exit(0)
    if len(sys.argv) > 5:
        print "Too many arguments!"
        exit(0)
    n = int(sys.argv[1])  # board size is nxn
    k = int(sys.argv[2])  # value required to lose
    inputString = list(sys.argv[3])  # board configuration
    t = int(sys.argv[4])  # time limit in seconds
    board = []
    # Test cases:-
    # 1. k > n (winning condition is higher that the board order)
    # 2. the given input is not in n^2 (positions missing or more than required)
    # 3. input string contains garbled characters other than 'w','b','.'
    # 4. black more than white
    # 5. difference between black and white is more than 1
    # 6. time given is less than one seconds
    flag, message = testInput(n, k, inputString, t)
    if flag is False:
        print message
        exit(0)
    else:
        j = 0
        while j < len(inputString):
            board.append(inputString[j:j+n])
            j += n
        return board, n, k, t, findTurn(board)


def testInput(n, k, inputString, t):
    flag = True
    message = ""
    if k > n:
        # k > n (winning condition is higher that the board order)
        flag = False
        message += "k value higher than n"
    elif len(inputString) != (n * n):
        # the given input is not in n^2 (positions missing or more than required)
        flag = False
        message += "Input string is smaller than the board size"
    elif t < 1:
        # time given is less than one seconds
        flag = False
    testRes, testMessage = checkInputString(inputString)
    if (flag == False) or (testRes == False):
        return False, message + "\n" + testMessage
    else:
        return True, ""


def checkInputString(inputString):
    message = ""
    whiteCount = 0  # counter to track white moves
    blackCount = 0  # counter to track black moves
    dotCount = 0
    for i in range(len(inputString)):
        if inputString[i] == 'w':
            whiteCount += 1
        elif inputString[i] == 'b':
            blackCount += 1
        elif inputString[i] == '.':
            dotCount += 1
        elif inputString[i] != 'w' or inputString[i] != 'b' or inputString[i] != '.':
            message += "Contains characters other than 'w', 'b', '.'\n"
    if (abs(whiteCount - blackCount) > 1):
        message += "Inconsistent white and black count"
    elif (whiteCount + blackCount + dotCount) != len(inputString):
        message += "Board configuration does not seem correct"
    if message == "":
        return True, message
    else:
        return False, message


def possibleMoves(board):
    return sum([i.count('.') for i in board])


# this function finds who plays next, the white or the black
def findTurn(board):
    if sum([i.count('w') for i in board]) > sum([i.count('b') for i in board]):
        return 'b'
    return 'w'


def successors(board, turn, count, initialTurn):
    states = list()
    if isOver(board):
        return board
    for i in range(n):
        for j in range(n):
            cur_board = copy.deepcopy(board)
            if cur_board[i][j] == '.':
                cur_board[i][j] = turn
                val = playerLost(cur_board, turn, count, initialTurn)
                if not val:
                    states.append(cur_board)
    random.shuffle(states)
    if len(states) == 0:
        for i in range(n):
            if '.' in cur_board[i]:
                j = cur_board[i].index('.')
                cur_board[i][j] = turn
                break
        return [cur_board]
    return states


def isOver(board):
    for row in board:
        if '.' in row:
            return False
    return True


def countConsecutiveOccurrences(array, count):
    if len(array) < count:
        return False, 0
    pattern = "b+|w+"
    occ = re.compile(pattern).findall(''.join(array))
    if len(occ) > 0:
        length = len(max(occ, key=len))
        if length >= count:
            if 'w' in max(occ, key=len):
                return True, 'w'
            else:
                return True, 'b'
        else:
            return False, 0
    return False, 0


def diagonals(board):
    list1 = []
    N = len(board)
    for c in range(N):
        i = 0
        j = c
        list2 = []
        while j <= c and N > i >= 0 and j >= 0:
            list2.append(board[i][j])
            i += 1
            j -= 1
        if len(list2) != 1:
            list1.append(list2)
    for c in range(1, N):
        i = N - 1
        j = c
        list2 = []
        while j < N and N > i > 0 and j > 0:
            list2.append(board[i][j])
            i -= 1
            j += 1
        if len(list2) != 1:
            list1.append(list2)
    for c in range(N):
        i = 0
        j = c
        list2 = []
        while j < N and N > i >= 0 and j >= 0:
            list2.append(board[i][j])
            i += 1
            j += 1
        if len(list2) != 1:
            list1.append(list2)
    for c in range(1, N):
        i = c
        j = 0
        list2 = []
        while j < N and N > i > 0 and j >= 0:
            list2.append(board[i][j])
            i += 1
            j += 1
        if len(list2) != 1:
            list1.append(list2)
    return list1


def check_row(board, turn, count, initialTurn):
    for i in range(len(board)):
        temp_arr = board[i]
        occFound = countConsecutiveOccurrences(temp_arr, count)
        if occFound[0]:
            if occFound[1] != initialTurn:
                return 1
            return -1
    return False


def check_col(board, turn, count, initialTurn):
    for i in range(n):
        temp_arr = [row[i] for row in board]
        occFound = countConsecutiveOccurrences(temp_arr, count)
        if occFound[0]:
            if occFound[1] != initialTurn:
                return 1
            return -1
    return False


def check_diag(board, turn, count, initialTurn):
    for i in range(0, len(board)):
        occFound = countConsecutiveOccurrences(board[i], count)
        if occFound[0]:
            if occFound[1] != initialTurn:
                return 1
            return -1
    return False


def playerLost(board, turn, count, initialTurn):
    # check the row for consecutive occurrences of k(count) of turn
    x = check_row(board, turn, count, initialTurn)
    if x == 1 or x == -1:
        return x
    # check the column for consecutive occurrences of k(count) of turn
    x = check_col(board, turn, count, initialTurn)
    if x == 1 or x == -1:
        return x
    # check all diagonals including primary and secondary diagonals
    diag_board = diagonals(board)
    x = check_diag(diag_board, turn, count, initialTurn)
    if x == 1 or x == -1:
        return x
    if isOver(board):
        return 0
    return False


def oppTurn(turn):
    if turn == 'w':
        return 'b'
    return 'w'

'''
#### WORKING Minimax CODE
def minValue(state, turn, count, initialTurn, depth):
    if depth == 0:
        return state, evalFunc(state, n, count, turn, initialTurn)
    util = playerLost(state, turn, count, initialTurn)
    if util:
        return state, util
    minState = sys.maxint
    tempState = state
    for succ in successors(state, turn, count, initialTurn):
        tempMin = min(minState, maxValue(succ, oppTurn(turn), count, initialTurn, depth - 1)[1])
        if minState > tempMin:
            minState = tempMin
            tempState = succ
    # if tempState == state:
    #     s1 = successors(state, turn, count, initialTurn)
    #     tempState = random.choice(s1)
    #     while len(s1) > 1 and isOver(tempState):
    #         s1.remove(tempState)
    #         tempState = random.choice(s1)
    return tempState, minState


def maxValue(state, turn, count, initialTurn, depth):
    if depth == 0:
        return state, evalFunc(state, n, count, turn, initialTurn)
    util = playerLost(state, turn, count, initialTurn)
    if util:
        return state, util
    maxState = -sys.maxint
    tempState = state
    for succ in successors(state, turn, count, initialTurn):
        tempMax = max(maxState, minValue(succ, oppTurn(turn), count, initialTurn, depth - 1)[1])
        if maxState < tempMax:
            maxState = tempMax
            tempState = succ
    # if tempState == state:
    #     s1 = successors(state, turn, initialTurn)
    #     tempState = random.choice(s1)
    #     while len(s1) > 1 and isOver(tempState):
    #         s1.remove(tempState)
    #         tempState = random.choice(s1)
    return tempState, maxState


def miniMaxDecision(state, turn, count, depth):
    return maxValue(state, turn, count, turn, depth)
'''


def minValue(state, turn, count, initialTurn, depth, alpha, beta, initialDepth):
    if depth == 0:
        return state, evalFunc(state, n, count, turn, initialTurn)
    util = playerLost(state, turn, count, initialTurn)
    if util is not False:
        return state, util
    minState = sys.maxint
    tempState = state
    for succ in successors(state, turn, count, initialTurn):
        tempMin = min(minState, maxValue(succ, oppTurn(turn), count, initialTurn, depth - 1, alpha, beta, initialDepth)[1])
        tempState = succ
        if tempMin <= alpha:
            return tempState, tempMin
        beta = min(beta, tempMin)
    return tempState, minState


def maxValue(state, turn, count, initialTurn, depth, alpha, beta, initialDepth):
    if depth == 0:
        return state, evalFunc(state, n, count, turn, initialTurn)
    util = playerLost(state, turn, count, initialTurn)
    if util is not False:
        return state, util
    maxState = -sys.maxint
    tempState = state
    for succ in successors(state, turn, count, initialTurn):
        tempMax = max(maxState, minValue(succ, oppTurn(turn), count, initialTurn, depth - 1, alpha, beta, initialDepth)[1])
        tempState = succ
        if depth == initialDepth:
            display(succ)   # print current succ
        if tempMax >= beta:
            return tempState, tempMax
        alpha = max(alpha, tempMax)
    return tempState, maxState


def miniMaxDecision(state, turn, count, depth):
    return maxValue(state, turn, count, turn, depth, -sys.maxint, sys.maxint, depth)


def evalFunc(state, n, count, turn, initialTurn):
    return abs(evalPlayer(state, n, count, oppTurn(initialTurn)) -
               evalPlayer(state, n, count, initialTurn))

def evalPlayer(state, n, count, player):
    score = 0
    pattern = "(?=([" + player + "|\.]{"+str(count)+"}))"
    for row in state:
        occ = re.compile(pattern).findall(''.join(row))
        score += len(occ)
    for i in range(n):
        temp_arr = [row[i] for row in state]
        occ = re.compile(pattern).findall(''.join(temp_arr))
        score += len(occ)
    # check all diagonals including primary and secondary diagonals
    diagonal_board = diagonals(state)
    for i in range(0, len(diagonal_board)):
        occ = re.compile(pattern).findall(''.join(diagonal_board[i]))
        score += len(occ)
    return score


'''
def terminalTest(board, turn, count):
    resultOver = False
    resultLoss = False
    if isOver(board):
        resultOver = True
    if playerLost(board, turn, count):
        resultLoss = True
    return resultOver or resultLoss


def utility(board, turn, count):
    result = playerLost(board, turn, count)
    return result

def minValue(state, turn, count, alpha, beta):
    if (terminalTest(state, turn, count)):
        return state, utility(state, turn, count)
    minState = -float('inf')
    tempState = state
    for s in successors(state, turn):
        tempState = s
        beta = min(minState, maxValue(s, turn, count, alpha, beta)[1])
        if alpha >= beta:
            return tempState, beta
    return tempState, beta


def maxValue(state, turn, count, alpha, beta):
    if (terminalTest(state, turn, count)):
        return state, utility(state, turn, count)
    maxState = -float('inf')
    tempState = state
    for s in successors(state, turn):
        tempState = s
        alpha = max(alpha, minValue(s, turn, count, alpha, beta)[1])
        if alpha >= beta:
            return tempState, alpha
    return tempState, alpha
'''


def display(board):
    output = ""
    for row in board:
        output = output + "".join(row)
    print output


def busyWaiting(t):
    print "Thinking..."
    time.sleep(t - 0.6)
    print "Recommended configuration of new board:-"


def playGame(board, n , k , t, turn):
    d = possibleMoves(board)
    if d > 1:
        depth = int(log(1000000 * t, d) + 0.5)
    else:
        depth = n * n
    s = miniMaxDecision(board, turn, k, depth)
    display(s[0])


# The main function
if __name__ == "__main__":
    board, n, k, t, turn = createBoard()
    # Thread(target=busyWaiting(t)).start()
    # Thread(target=playGame(board, n , k , t, turn)).start()
    playGame(board, n, k, t, turn)
