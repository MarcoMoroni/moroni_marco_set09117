############
# CHECKERS #
############

from enum import Enum
class PieceRank(Enum):
    MAN = 0
    KING = 1

# board
boardDimension = 8
emptySquareChar = 'e'
board = [[emptySquareChar for col in range(boardDimension)] for row in range(boardDimension)]

# print board
def printBoard():
    # create the line used to divide the squares
    line = "."
    for i in range(boardDimension):
        line += "   ."
    # print the first line
    print(line)
    # print everithing else
    for row in board:
        for col in row:
            print("  " + col + " ", end='')s
        print()
        print(line)


# player class
class Player:
    def __init__(self, symbol):
        self.symbol = symbol


# Piece
class Piece:
    rank = PieceRank.MAN
    
    def __init__(self, player):
        self.player = player
    
    def becomesKing(self):
        self.rank = PieceRank.KING
