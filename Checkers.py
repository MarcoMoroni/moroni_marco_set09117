############
# CHECKERS #
############

from enum import Enum
class PieceRank(Enum):
    MAN = 0
    KING = 1

# board
boardDimension = 8
emptySquareChar = '.'
board = [[emptySquareChar for col in range(boardDimension)] for row in range(boardDimension)]

# print board
def printBoard():
    for row in board:
        for col in row:
            print(col, end='')
        print()


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


p = Piece("A")
print(p.rank)
p.becomesKing()
print(p.rank)
