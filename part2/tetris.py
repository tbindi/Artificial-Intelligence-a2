# Simple tetris program! v0.1
# D. Crandall, Sept 2016

from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys
from copy import deepcopy


class HumanPlayer:

    def get_moves(self, piece, board):
        print "Type a sequence of moves using: \n  b for move left \n  m for " \
              "move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands = {"b": tetris.left, "n": tetris.rotate,
                        "m": tetris.right, " ": tetris.down}
            commands[c]()


#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#####
class ComputerPlayer:
    # Given a new piece (encoded as a list of strings) and a board (also
    # list of strings), this function should generate a series of commands to
    #  move the piece into the "optimal" position. The commands are a string
    #  of letters, where b and m represent left and right, respectively,
    # and n rotates.
    def get_moves(self, piece, board):
        # super simple current algorithm: just randomly move left, right,
        # and rotate a few times
        return random.choice("mnb") * random.randint(1, 10)
       
    # This is the version that's used by the animted version.  This is really
    #  similar to get_moves,
    # except that it runs as a separate thread and you should access various
    #  methods and data in
    # the "tetris" object to control the movement. In particular:
    #   - tetris.col, tetris.row have the current column and row  of the
    # upper-left corner of the falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece()
    # is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate()
    # can be called to actually issue game commands
    #   - tetris.get_board() returns the current state of the board,
    # as a list of strings.
    #
    def control_game(self, tetris):
        # another super simple algorithm: just move piece to the least-full
        # column
        while 1:
            time.sleep(0.1)
            board = tetris.get_board()
            column, rotation = self.gen_states(board, tetris)
            self.simulate_move(column, rotation, tetris)

    def simulate_move(self, column, rotation, tetris):
        new_position = column - tetris.col
        while new_position > 0:
            tetris.right()
            new_position -= 1
        while new_position < 0:
            tetris.left()
            new_position += 1
        tetris.piece = tetris.rotate_piece(tetris.piece, rotation)
        tetris.down()

    def go_down(self, temp_board, tetris, c, piece):
        r = 0
        for r in range(0, len(temp_board)):
            if not tetris.check_collision((temp_board, 0), piece, r, c):
                continue
            else:
                break
        if r == 0:
            try:
                temp_board = tetris.place_piece((temp_board, 0), piece, 0, c)[0]
            except:
                temp_board = tetris.place_piece((temp_board, 0), piece, 0,
                                                c-1)[0]
            return temp_board
        return tetris.place_piece((temp_board, 0), piece, r-1, c)[0]

    def get_rotations(self, piece, tetris):
        result = [[piece, 0]]
        for j in [90, 180, 270]:
            i = tetris.rotate_piece(piece, j)
            if i not in result:
                result.append([i, j])
        return result

    def first_piece(self, board, cur_pieces, tetris):
        fringe = []
        for c in range(0, len(board[0]) - 1):
            temp = deepcopy(board)
            for cur_piece, rotation in cur_pieces:
                temp = self.go_down(temp, tetris, c, cur_piece)
                fringe.append([temp, c, rotation])
        return fringe

    def gen_boards(self, board, next_pieces, tetris, max_score,
                  max_board):
        for c in range(0, len(board[0]) - 1):
            temp = deepcopy(board)
            for cur_piece, rotation in next_pieces:
                temp = self.go_down(temp, tetris, c, cur_piece)
                param = self.get_param(temp)
                new_score = self.get_value(param)
                if max_score < new_score or max_score == 0:
                    max_score = new_score
                    max_board = temp
        return max_board, max_score

    def gen_states(self, board, tetris):
        cur_pieces = self.get_rotations(tetris.get_piece()[0], tetris)
        next_pieces = self.get_rotations(tetris.get_next_piece()[0], tetris)
        fringe = self.first_piece(board, cur_pieces, tetris)
        max_score = 0
        max_board = None
        max_column = -1
        max_rotation = -1
        while len(fringe) > 0:
            temp = fringe.pop(0)
            temp_board = temp[0]
            new_board, new_score = self.gen_boards(temp_board, next_pieces,
                                                   tetris, max_score, max_board)
            if max_score == 0 or max_score < new_score:
                max_score = new_score
                max_board = new_board
                max_column = temp[1]
                max_rotation = temp[2]
        return max_column, max_rotation

    def get_value(self, params):
        return (-0.510066 * params[0]) + (0.760666 * params[1]) + (
            -0.35663 * params[2]) + (-0.184483 * params[3])

    def get_param(self, board):
        col_heights = [0 for i in range(0, len(board[0]) + 1)]
        complete = 0
        holes = 0
        height = len(board)
        for r in range(0, len(board)):
            for c in range(0, len(board[r])):
                if board[r][c] == 'x' and col_heights[c] == 0:
                    col_heights[c] = height - r
                if board[r][c] == ' ' and board[r-1][c] == 'x' and r > 1:
                    holes += 1
            if all('x' == i for i in board[r]):
                complete += 1
        bump = sum(
            [abs(col_heights[i] - col_heights[i+1])
              for i in range(0, len(col_heights)-1)]
            )
        return [sum(col_heights), complete, holes, bump]


###################
# main program
###################
(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print "unknown player!"

    if interface_opt == "simple":
        tetris = SimpleTetris()
    elif interface_opt == "animated":
        tetris = AnimatedTetris()
    else:
        print "unknown interface!"

    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s
