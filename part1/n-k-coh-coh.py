"""
n-k-coh-coh is a popular childhood game in a certain rural midwestern town that requires just a board
consisting of a grid of n  n squares and some white and black marbles. Initially the board starts empty
and all marbles are in a pile beside the board. Player 1 picks up a white marble and places it in any square
of the board. Player 2 then picks up a black marble from the pile, and places it in any open square (i.e.
any square except the one selected by Player 1). Play continues back and forth, with Player 1 always using
white marbles and Player 2 always using black. A player loses the game as soon as they place a marble such
that there is a continuous line of k marbles of his or her color in the same row, column, or diagonal of the
board. (For example, note that 3-3-coh-coh is nearly the same as tic-tac-toe, except that players are trying
to avoid completing a row, column or diagonal instead of trying to complete one.)

Your task is to write a Python program that plays n-k-coh-coh well. Your program should accept a command
line argument that gives the current state of the board as a string of w's, b's, and .'s, which indicate which
squares are lled with a white, black, or no marble, respectively, in row-major order. For example, if n = 3
and the state of the board is:

then the encoding of the state would be:

.w......b

More precisely, your program will be called with four command line parameters: (1) the value of n, (2) the
value of k, (3) the state of the board, encoded as above, and (4) a time limit in seconds. Your program
should then decide a recommended move given the current board state, and display the new state of the
board after making that move, within the number of seconds specied. Displaying multiple lines of output is
ne as long as the last line has the recommended board state. For example, a sample run of your program
might look like:

[djcran@macbook]$ python nkcohcoh.py 3 3 .w......b 5
Thinking! Please wait...
Hmm, I'd recommend putting your marble at row 2, column 1.
New board:
.w.w....b
"""
import random
import sys
import copy
import re
import numpy as np
from math import log

# this function creates the initial board configuration and time limit from command line
def createBoard():
    n = int(sys.argv[1])  # board size is nxn
    k = int(sys.argv[2])  # value required to lose
    inputString = list(sys.argv[3])  # board configuration
    t = int(sys.argv[4])  # time limit in seconds
    curIndex = 0  # counter to track the character in the input
    board = [[0 for row in range(0, n)] for col in range(0, n)]
    #Test cases:-
    #1. k > n (winning condition is higher that the board order)
    #2. the given input is not in n^2 (positions missing or more than required)
    #3. input string contains garbled characters other than 'w','b','.'
    #4. black more than white
    #5. difference between black and white is more than 1
    #6. time given is less than one seconds
    flag, message = testInput(n, k, inputString, t)
    if (flag == True):
        for i in range(n):
            for j in range(n):
                board[i][j] = inputString[curIndex]
                curIndex += 1
        return board, n, k, t, flag, message
    else:
        return board, n, k, t, flag, message

def testInput(n, k, inputString, t):
    flag = True
    message = ""
    if k > n:
        #k > n (winning condition is higher that the board order)
        flag = False
        message += "k value higher than n"
    elif len(inputString) != (n*n):
        #the given input is not in n^2 (positions missing or more than required)
        flag = False
        message += "Input string is smaller than the board size"
    elif t<1:
        #time given is less than one seconds
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
    if (whiteCount - blackCount > 1):
        message += "White count is way more than the black count"
    elif (whiteCount + blackCount + dotCount) != len(inputString):
        message += "Board configuration does not seem correct"
    if (message == ""):
        return True, message
    else:
        return False, message

def possibleMoves(board):
    count = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] == '.':
                count += 1
    return count


# this function finds who plays next, the white or the black
def findTurn(board):
    whiteCount = 0  # counter to track white moves
    blackCount = 0  # counter to track black moves
    for i in range(n):
        for j in range(n):
            if board[i][j] == 'w':
                whiteCount += 1
            elif board[i][j] == 'b':
                blackCount += 1
    if whiteCount > blackCount:
        return 'b'
    else:
        return 'w'


def successors(board, turn):
    states = list()
    if isOver(board):
        return board
    for i in range(n):
        for j in range(n):
            cur_board = copy.deepcopy(board)
            if cur_board[i][j] == '.':
                cur_board[i][j] = turn
                states.append(cur_board)
    random.shuffle(states)
    return states


def isOver(board):
    for row in board:
        if '.' in row:
            return False
    return True

'''
def terminalTest(board, turn, count):
    resultOver = False
    resultLoss = False
    if isOver(board):
        resultOver = True
    if playerLost(board, turn, count):
        resultLoss = True
    return resultOver or resultLoss
'''


def playerLost(board, turn, count, initialTurn):
    # check the row for consecutive occurrences of k(count) of turn
    if isOver(board):
        return 10
    for i in range(n):
        temp_arr = board[i]
        occFound = countConsecutiveOccurrences(temp_arr, turn, count)
        if occFound[0]:
            if occFound[1] != initialTurn:
                return 1
            return -1
    # check the column for consecutive occurrences of k(count) of turn
    for i in range(n):
        temp_arr = [row[i] for row in board]
        occFound = countConsecutiveOccurrences(temp_arr, turn, count)
        if occFound[0]:
            if occFound[1] != initialTurn:
                return 1
            return -1
    # check all diagonals including primary and secondary diagonals
    diagonal_board = diagonals(board)
    for i in range(0, len(diagonal_board)):
        occFound = countConsecutiveOccurrences(diagonal_board[i], turn, count)
        if occFound[0]:
            if occFound[1] != initialTurn:
                return 1
            return -1
    return False


# function to get all diagonals in the board
def diagonals(board):
    # Based on the code to get diagonals in Python from
    # http://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
    a = np.array(board)
    diags = [a[::-1, :].diagonal(i) for i in range(-a.shape[0] + 1, a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1] - 1, -a.shape[0], -1))
    # Code from stackoverflow ends
    return diags


def countConsecutiveOccurrences(array, turn, count):
    if len(array) < count:
        return False, 0
    pattern = "b+|w+"
    occ = re.compile(pattern).findall(''.join(array))
    if len(occ) > 0:
        length = len(max(occ))
        if length >= count:
            if 'w' in max(occ):
                return True, 'w'
            else:
                return True, 'b'
        else:
            return False, 0
    return False, 0

'''
def utility(board, turn, count):
    result = playerLost(board, turn, count)
    return result
'''


def oppTurn(turn):
    if turn == 'w':
        return 'b'
    return 'w'


def minValue(state, turn, count, initialTurn, depth):
    if depth == 0:
        return state, evalFunc(state, n, count, turn, initialTurn)
    util = playerLost(state, turn, count, initialTurn)
    if util:
        return state, util
    minState = 0
    tempState = state
    for succ in successors(state, turn):
        tempMin = min(minState, maxValue(succ, oppTurn(turn), count, initialTurn, depth - 1)[1])
        if minState > tempMin:
            minState = tempMin
            tempState = succ
    if tempState == state:
        tempState = successors(state, turn)[0]
        minState = 1
    return tempState, minState


def maxValue(state, turn, count, initialTurn, depth):
    if depth == 0:
        return state, evalFunc(state, n, count, turn, initialTurn)
    util = playerLost(state, turn, count, initialTurn)
    if util:
        return state, util
    maxState = 0
    tempState = state
    for succ in successors(state, turn):
        tempMax = max(maxState, minValue(succ, oppTurn(turn), count, initialTurn, depth - 1)[1])
        if maxState < tempMax:
            maxState = tempMax
            tempState = succ
    if tempState == state:
        tempState = successors(state, turn)[0]
        maxState = -1
    return tempState, maxState


def evalFunc(state, n, count, turn, initialTurn):
    if turn != initialTurn:
        return evalPlayer(state, n, count, "w") - evalPlayer(state, n, count, "b")
    return evalPlayer(state, n, count, "b") - evalPlayer(state, n, count, "w")

def evalPlayer(state, n, count, player):
    score = 0
    pattern = "[" + player + "|\.]{"+str(count)+",}"
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


def miniMaxDecision(state, turn, count, depth):
    return maxValue(state, turn, count, turn, depth)


# The main function
if __name__ == "__main__":
    board, n, k, t, flag, message = createBoard()
    if (flag == False):
        print message
    else:
        d = possibleMoves(board)
        if d > 1:
            depth = int(log(500*t, d*d) + 0.5)
        else:
            depth = n*n
        turn = findTurn(board)
        s = miniMaxDecision(board, turn, k, depth)
        for i in range(9):
            print(s[0])
            turn = findTurn(s[0])
            s = miniMaxDecision(s[0], turn, k, depth)
