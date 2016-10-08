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
import sys
import copy

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

def evaluationCalculation(board, turn):
    #TODO: write the evaluation function for the current board configuration
    evaluation = 0
    whiteMoves = 0
    blackMoves = 0
    return evaluation

def successors(board, turn):
    states = list()
    if isOver(board):
        return states
    for i in range(n):
        for j in range(n):
            cur_board = copy.deepcopy(board)
            if cur_board[i][j] == '.':
                cur_board[i][j] = turn
            states.append(cur_board)
    return states

def isOver(board):
    return True

def playerLost(board):
    #TODO write code for condition where a player lost
    return False

def minMax(board):
    #TODO: write the min-max algorithm here
    return False

#the main function
if __name__ == "__main__":
    board, n, k, t = createBoard()
    print board
    turn = findTurn(board)
    print turn
    valid_moves = successors(board, turn)
    print valid_moves