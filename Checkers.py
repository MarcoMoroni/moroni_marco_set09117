############
# CHECKERS #
############



from enum import Enum
class PieceRank(Enum):
    MAN = 0
    KING = 1



# print board
def printBoard():
    # create the line to visually divide the squares
    line = "."
    for i in range(boardDimension):
        line += "   ."
    # print the first line
    print(line)
    # print everithing else
    for row in board:
        for square in row:
            if (type(square) is Piece):
                print("  " + square.player.symbol + " ", end='')
            else:
                print("    ", end='')
        print()
        print(line)



# player class
class Player:
    def __init__(self, symbol):
        self.symbol = symbol



# piece class
class Piece:
    
    rank = PieceRank.MAN
    
    def __init__(self, player, initialPosition):
        self.player = player
        self.initialPosition = initialPosition

    def __init__(self, player):
        self.player = player
    
    def becomesKing(self):
        self.rank = PieceRank.KING



# create board
boardDimension = 8
emptySquareChar = "e"
board = [[emptySquareChar for col in range(boardDimension)] for row in range(boardDimension)]

# create players
human = Player("o")
cpu = Player("x")
players = []
players.append(human)
players.append(cpu)

# pieces setup
for player in players:
    for row in range(3):
        for col in range(boardDimension):
            if (col + row) % 2 == 0:
                newPiece = Piece(player)
                if player == human:
                    newPiece.initialPosition = (boardDimension - 1 - (boardDimension + row), boardDimension - 1 - (boardDimension + col))
                else:
                    newPiece.initialPosition = (row, col)
                board[newPiece.initialPosition[0]][newPiece.initialPosition[1]] = newPiece
