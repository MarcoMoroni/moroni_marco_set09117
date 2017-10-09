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
    for i in range(boardDimention):
        line += "  " + str(i) + " "
    # print the col number
    print(line + "\n")
    
    # create the line to visually divide the squares
    firstLine = "    ┌"
    line = "    ├"
    lastLine = "    └"
    for i in range(boardDimention):
        # different divider if last one
        if i < boardDimention - 1:
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
        if rowNo < boardDimention - 1:
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



# move class
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



# return all available displacements
def legalDisplacements(coordinates):
    
    possibleDisplacements = []

    row = coordinates[0]
    col = coordinates[1]
    player = board[row][col].player

    # different if the player is facing up:
    # need to *-1 the row if facing up
    mult = 1
    if player.isFacingUp:
        mult = -1
    possibleDisplacements.append((1 * mult, -1))
    possibleDisplacements.append((1 * mult, 1))
    possibleDisplacements.append((2 * mult, -2))
    possibleDisplacements.append((2 * mult, 2))
    if board[row][col].rank == PieceRank.KING:
        possibleDisplacements.append((-1 * mult, -1))
        possibleDisplacements.append((-1 * mult, 1))
        possibleDisplacements.append((-2 * mult, -2))
        possibleDisplacements.append((-2 * mult, 2))

    # keep the legal moves only
    legalDisplacements = possibleDisplacements[:]
    #print("  possibleDisplacements =", possibleDisplacements)
    for d in possibleDisplacements:
        #print("  checking", d, row + d[0], col + d[1], "...")
        # check if it's inside the board
        if not (0 <= row + d[0] < boardDimention and 0 <= col + d[1] < boardDimention):
            #print("    out of board")
            legalDisplacements.remove(d)
        else:
            # check if it's occupied
            if type(board[row + d[0]][col + d[1]]) is Piece:
                #print("    occupied")
                legalDisplacements.remove(d)
            else:
                # if it is (+2, +-2) is valid only if it eats an opponent piece
                middleSquare = board[row + (int(d[0] / 2))][col + (int(d[1] / 2))]
                if abs(d[0]) == 2 and abs(d[1]) == 2:
                    if type(middleSquare) is Piece:
                        if middleSquare.player == player:
                            #print("    can't eat yourself")
                            legalDisplacements.remove(d)
                    else:
                        #print("    nothing to eat")
                        legalDisplacements.remove(d)

    #print("  legalDisplacements =", legalDisplacements)   
    return legalDisplacements



# create board
boardDimention = 8
emptySquare = "empty"
board = [[emptySquare for col in range(boardDimention)] for row in range(boardDimention)]

# create players
human = Player(["○", "□"], True)
cpu = Player(["●", "■"])
players = []
players.append(human)
players.append(cpu)

# pieces setup
for player in players:
    for row in range(3):
        for col in range(boardDimention):
            if (col + row) % 2 == 0:
                newPiece = Piece(player)
                if player.isFacingUp:
                    newPiece.initialPosition = (boardDimention - 1 - (boardDimention + row), boardDimention - 1 - (boardDimention + col))
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

        # for storing move
        doesBecomeKing = False
        displacement = (0, 0)
    
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
                if (squareToCheck.player == player):
                    if not legalDisplacements((tempRow, tempCol)) == []:
                        rowSelected = tempRow
                        colSelected = tempCol
                    else:
                        print("This piece can't move.")
                else:
                    print("Not your piece.")
            else:
                print("No piece here.")
        
        # do a move - TODO must do at leat 1 move
        #           - TODO multiple moves!
        # Note: the move is legal (already checked)
        turnEnd = False
        while not turnEnd:
            textInput = input("Move to > ")
            newRow, newCol = coordinatesFromInput(textInput)
            temporaryDisplacement = (newRow - rowSelected, newCol - colSelected)
            # if its a legal move
            if temporaryDisplacement in legalDisplacements((tempRow, tempCol)):
                displacement = temporaryDisplacement
                board[newRow][newCol] = board[rowSelected][colSelected]
                board[rowSelected][colSelected] = emptySquare
                # eat NOT WORKING
                # if the displacement is (+-2, +-2)
                if abs(displacement[0]) == 2 and abs(displacement[1]) == 2:
                    board[rowSelected + int(displacement[0] / 2)][colSelected + int(displacement[1] / 2)] = emptySquare
                # become king
                if player.isFacingUp and newRow == 0:
                    board[newRow][newCol].becomesKing()
                    doesBecomeKing = True
                elif newRow == boardDimention - 1:
                    board[newRow][newCol].becomesKing()
                    doesBecomeKing = True
                turnEnd = True
            else:
                print("Not a legal move.")

        # store move
        newMove = Move(board[newRow][newCol], (rowSelected - newRow, colSelected - newCol), doesBecomeKing)
        moves.append(newMove)
