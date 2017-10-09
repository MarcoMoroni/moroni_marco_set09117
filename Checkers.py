############
# CHECKERS #
############



from enum import Enum
class PieceRank(Enum):
    MAN = 0
    KING = 1



# print board
def printBoard():
    
    # create the line for col number
    line = "    "
    for i in range(boardDimension):
        line += "  " + str(i) + " "
    # print the col number
    print(line + "\n")
    
    # create the line to visually divide the squares
    firstLine = "    ┌"
    line = "    ├"
    lastLine = "    └"
    for i in range(boardDimension):
        # different divider if last one
        if i < boardDimension - 1:
            firstLine += "───┬"
            line += "───┼"
            lastLine += "───┴"
        else:
            firstLine += "───┐"
            line += "───┤"
            lastLine += "───┘"

    # print the first line
    print(firstLine)
    
    # print everithing else
    for rowNo,row in enumerate(board):
        # print row number
        print(rowNo, end="   ")
        for square in row:
            if (type(square) is Piece):
                # print the symbol of the piece depending on the rank
                print("│ " + square.player.symbols[square.rank] + " ", end='')
            else:
                print("│   ", end='')
        # different divider if last divider line
        if rowNo < boardDimension - 1:
            print("│\n" + line)
        else:
            print("│\n" + lastLine)
            



# player class
class Player:

    def __init__(self, symbols, isFacingUp=False):
        # symbol[0] is for Man, [1] is for King
        self.symbols = {PieceRank.MAN: symbols[0], PieceRank.KING: symbols[1]}
        # remember the player side on the board
        self.isFacingUp = isFacingUp



# piece class
class Piece:
    
    rank = PieceRank.MAN

    def __init__(self, player):
        self.player = player
    
    def becomesKing(self):
        self.rank = PieceRank.KING



# turn class
class Move:

    def __init__(self, piece, displacement, doesBecomeKing=False):
        self.piece = piece
        self.displacement = displacement
        # note: if displacement is (+-2,+-2) it means the pieace eats
        self.doesBecomeKing = doesBecomeKing



# get x y coordinates from string
def coordinatesFromInput(text):
    # split
    coord = text.split()
    # convet to int
    coord = [int(i) for i in coord]
    return coord



# create board
boardDimension = 8
emptySquareChar = "e"
board = [[emptySquareChar for col in range(boardDimension)] for row in range(boardDimension)]

# create players
human = Player(["○", "□"], True)
cpu = Player(["●", "■"])
players = []
players.append(human)
players.append(cpu)

# pieces setup
for player in players:
    for row in range(3):
        for col in range(boardDimension):
            if (col + row) % 2 == 0:
                newPiece = Piece(player)
                if player.isFacingUp:
                    newPiece.initialPosition = (boardDimension - 1 - (boardDimension + row), boardDimension - 1 - (boardDimension + col))
                else:
                    newPiece.initialPosition = (row, col)
                board[newPiece.initialPosition[0]][newPiece.initialPosition[1]] = newPiece

# create a history of moves
moves = []

# game loop
someoneWins = False
while not someoneWins:
    for player in players:

        printBoard()

        doesBecomeKing = False # for storing move
    
        # select a piece in a square
        rowSelected = ""
        colSelected = ""
        while rowSelected == "" and colSelected == "":
            stringToPrintToUser = "Select piece " + player.symbols[PieceRank.MAN] + " > "
            textInput = input(stringToPrintToUser)
            tempRow, tempCol = coordinatesFromInput(textInput)
            # select it if there is a piece
            # and it belongs to the player
            # and it can be moved
            squareToCheck = board[tempRow][tempCol]
            if (type(squareToCheck) is Piece):
                if (squareToCheck.player == player): ## && it can be moved - TODO
                    rowSelected = tempRow
                    colSelected = tempCol
                else:
                    print("Not your piece.")
            else:
                print("No piece here.")

        # do a move - TODO must do at leat 1 move
        #           - TODO multiple moves!
        turnEnd = False
        while not turnEnd:
            textInput = input("Move to > ")
            newRow, newCol = coordinatesFromInput(textInput)
            # if its a legal move
            if True: # TODO
                board[newRow][newCol] = board[rowSelected][colSelected] # IS THIS A COPY?
                board[rowSelected][colSelected] = emptySquareChar
                turnEnd = True
                # become king
                if player.isFacingUp:
                    if (newRow == 0):
                        board[newRow][newCol].becomesKing()
                        doesBecomeKing = True
                else:
                    if (newRow == boardDimension - 1):
                        board[newRow][newCol].becomesKing()
                        doesBecomeKing = True

        # store move
        newMove = Move(board[newRow][newCol], (rowSelected - newRow, colSelected - newCol), doesBecomeKing)
        moves.append(newMove)
