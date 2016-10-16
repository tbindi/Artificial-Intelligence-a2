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
    j = 0
    while j < len(inputString):
        board.append(inputString[j:j+n])
        j += n
    return board, n, k, t, findTurn(board)


def testInput(n, k, inputString, t):
    message = ""
    if (k <= 0) or (n <= 0) or (t <= 0):
        # negative inputs given
        message = "One or more input is less than or equal to 0"
    if k > n:
        # k > n (winning condition is higher that the board order)
        message = "k value higher than n"
    elif len(inputString) != (n*n):
        # the given input is not in n^2 (positions missing or more than
        # required)
        message = "Input string is smaller than the board size"
    elif t < 0:
        # time given is less than zero seconds
        message = "Time is less than zero seconds"
    if not all(['w', 'b', '.'] in i for i in inputString):
        print message
        exit(0)
    return True


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
#### WORKING CODE
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


def minValue(state, turn, count, initialTurn, depth, alpha, beta):
    if depth == 0:
        return state, evalFunc(state, n, count, turn, initialTurn)
    util = playerLost(state, turn, count, initialTurn)
    if util is not False:
        return state, util
    minState = sys.maxint
    tempState = state
    for succ in successors(state, turn, count, initialTurn):
        tempMin = min(minState, maxValue(succ, oppTurn(turn), count, initialTurn, depth - 1, alpha, beta)[1])
        tempState = succ
        if tempMin <= alpha:
            return tempState, tempMin
        beta = min(beta, tempMin)
    return tempState, minState


def maxValue(state, turn, count, initialTurn, depth, alpha, beta):
    if depth == 0:
        return state, evalFunc(state, n, count, turn, initialTurn)
    util = playerLost(state, turn, count, initialTurn)
    if util is not False:
        return state, util
    maxState = -sys.maxint
    tempState = state
    for succ in successors(state, turn, count, initialTurn):
        tempMax = max(maxState, minValue(succ, oppTurn(turn), count, initialTurn, depth - 1, alpha, beta)[1])
        tempState = succ
        if tempMax >= beta:
            return tempState, tempMax
        alpha = max(alpha, tempMax)
    return tempState, maxState


def miniMaxDecision(state, turn, count, depth):
    return maxValue(state, turn, count, turn, depth, -sys.maxint, sys.maxint)

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
    for i in board:
        print " ".join(j for j in i)

def busyWaiting(t):
    print "Thinking..."
    time.sleep(t - 0.6)

def playGame(board, n , k , t, turn):
    d = possibleMoves(board)
    if d > 1:
        depth = int(log(10000000000 * t, d * d) + 0.5)
    else:
        depth = n * n
    # depth = 1
    s = miniMaxDecision(board, turn, k, depth)
    for i in range(29):
        # for row in s[0]:
        #     # print "".join(row),
        #
        #     sys.stdout.softspace = False
        # print ""
        print "----- Turn: ", turn
        display(s[0])
        turn = findTurn(s[0])
        s = miniMaxDecision(s[0], turn, k, depth)

# The main function
if __name__ == "__main__":
    board, n, k, t, turn = createBoard()
    Thread(target=busyWaiting(t)).start()
    Thread(target=playGame(board, n , k , t, turn)).start()
