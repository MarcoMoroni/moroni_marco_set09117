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
                # print the symbol of the piece depending on the rank
                print("  " + square.player.symbols[square.rank] + " ", end='')
            else:
                print("    ", end='')
        print()
        print(line)



# player class
class Player:

    def __init__(self, symbols, facingUp=False):
        # symbol[0] is for Man, [1] is for King
        self.symbols = {PieceRank.MAN: symbols[0], PieceRank.KING: symbols[1]}
        # remember the player side on the board
        self.facingUp = facingUp



# piece class
class Piece:
    
    rank = PieceRank.MAN

    def __init__(self, player):
        self.player = player
    
    def becomesKing(self):
        self.rank = PieceRank.KING



# turn class
class Move:

    def __init__(self, piece, direction, doesEat=False, doesBecomeKing=False):
        self.piece = piece
        self.direction = direction
        self.doesEat = doesEat
        self.doesBecomeKing = doesBecomeKing



# create board
boardDimension = 8
emptySquareChar = "e"
board = [[emptySquareChar for col in range(boardDimension)] for row in range(boardDimension)]

# create players
human = Player(["o", "O"], True)
cpu = Player(["x", "X"])
players = []
players.append(human)
players.append(cpu)

# pieces setup
for player in players:
    for row in range(3):
        for col in range(boardDimension):
            if (col + row) % 2 == 0:
                newPiece = Piece(player)
                if player.facingUp:
                    newPiece.initialPosition = (boardDimension - 1 - (boardDimension + row), boardDimension - 1 - (boardDimension + col))
                else:
                    newPiece.initialPosition = (row, col)
                board[newPiece.initialPosition[0]][newPiece.initialPosition[1]] = newPiece
