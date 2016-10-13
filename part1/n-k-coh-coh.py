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

#this function creates the initial board configuration and time limit from command line
def createBoard():
    n = int(sys.argv[1])  #board size is nxn
    k = int(sys.argv[2])  # value required to lose
    inputString = list(sys.argv[3])    #board configuration
    t = int(sys.argv[4])  # time limit in seconds
    curIndex = 0    #counter to track the character in the input
    board = [[0 for row in range(0, n)] for col in range(0, n)]
    for i in range(n):
        for j in range(n):
            board[i][j] = inputString[curIndex]
            curIndex +=1
    return board, n, k, t

#this function finds who plays next, the white or the black
def findTurn(board):
    whiteCount = 0  #counter to track white moves
    blackCount = 0  #counter to track black moves
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
    for i in range(n):
        if '.' in board[i]:
            return False
    return True

def terminalTest(board, turn, count):
    resultOver = False
    resultLoss = False
    if isOver(board):
        resultOver = True
    if playerLost(board, turn, count):
        resultLoss = True
    return (resultOver or resultLoss)

def playerLost(board, turn, count, initialTurn):
    #check the row for consecutive occurrences of k(count) of turn
    if isOver(board):
        return 10
    for i in range(n):
        temp_arr = board[i]
        if(countConsecutiveOccurences(temp_arr, turn, count)):
            if turn == initialTurn:
                return 1
            return -1
    #check the column for consecutive occurrences of k(count) of turn
    for i in range(n):
        temp_arr = [row[i] for row in board]
        if(countConsecutiveOccurences(temp_arr, turn, count)):
            if turn == initialTurn:
                return 1
            return -1
    #check all diagonals including primary and secondary diagonals
    diagonal_board = diagonals(board)
    for i in range(0, len(diagonal_board)):
        if (countConsecutiveOccurences(diagonal_board[i], turn, count)):
            if turn == initialTurn:
                return 1
            return -1
    return False

#function to get all diagonals in the board
def diagonals(board):
    #Based on the code to get diagonals in Python from http://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
    a = np.array(board)
    diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
    #Code from stackoverflow ends
    return diags

def countConsecutiveOccurences(array, turn, count):
    if len(array) < count:
        return False
    if turn == 'w':
        opponent = 'b'
    else:
        opponent = 'w'
    pattern = opponent+"+"
    occ = re.compile(pattern).findall(''.join(array))
    if len(occ) > 0:
        length = len(max(occ))
        if length >= count:
            return True
        else:
            return False
    return False

def utility(board, turn, count):
    result = playerLost(board, turn, count)
    return result


def oppTurn(turn):
    if turn == 'w':
        return 'b'
    return 'w'

def minValue(state, turn, count, initialTurn):
    util = playerLost(state, turn, count, initialTurn)
    if (util != False):
        return state, util
    minState = 0
    tempState = state
    for s in successors(state, turn):
        tempMin = min(minState, maxValue(s, oppTurn(turn), count, initialTurn)[1])
        if minState > tempMin:
            minState = tempMin
            tempState = s
    if tempState == state:
        tempState = successors(state,turn)
        minState = 1
    return tempState, minState


def maxValue(state, turn, count, initialTurn):
    util = playerLost(state, turn, count, initialTurn)
    if (util != False):
        return state, util
    maxState = 0
    tempState = state
    for s in successors(state, turn):
        tempMax = max(maxState, minValue(s, oppTurn(turn), count, initialTurn)[1])
        if maxState < tempMax:
            maxState = tempMax
            tempState = s
    if tempState == state:
        tempState = successors(state,turn)[0]
        maxState = -1
    return tempState, maxState

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

def miniMaxDecision(state, turn, count):
    return maxValue(state, turn, count, turn)

#the main function
if __name__ == "__main__":
    board, n, k, t = createBoard()
    print board
    turn = findTurn(board)
    s = miniMaxDecision(board, turn, k)
    for i in range(9):
        print(s[0])
        turn = findTurn(s[0])
        s = miniMaxDecision(s[0], turn, k)