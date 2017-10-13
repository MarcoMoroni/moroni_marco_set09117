############
# CHECKERS #
############


import time

from enum import Enum
class PieceRank(Enum):
    MAN = 0
    KING = 1



# print board
def printBoard(selectedPieceHighlight=(-1, -1), legalMovesHighlights=[]):

    print()
    print()
    
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
    for rowNo, row in enumerate(board):
        # print row number
        print(rowNo, end="   ")
        for colNo, square in enumerate(row):
            if (type(square) is Piece):
                # print the symbol of the piece depending on the rank
                # also show if it is selected
                if (rowNo, colNo) == selectedPieceHighlight:
                    print("│(" + square.player.symbols[square.rank] + ")", end='')
                else:
                    print("│ " + square.player.symbols[square.rank] + " ", end='')
            elif (rowNo, colNo) in legalMovesHighlights:
                # highlight legal moves
                print("│▐█▌", end='')
            else:
                print("│   ", end='')
        # different divider if last divider line
        if rowNo < boardDimention - 1:
            print("│\n" + line)
        else:
            print("│\n" + lastLine)

    print()
            



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

    def undoBecomingKing(self):
        self.rank = PieceRank.MAN



# move class
class Move:

    def __init__(self, originPosition, displacement, pieceEaten="", doesBecomeKing=False):
        self.originPosition = originPosition
        self.displacement = displacement
        # note: if displacement is (+-2,+-2) it means the pieace eats
        self.pieceEaten = pieceEaten
        self.doesBecomeKing = doesBecomeKing



# get x y coordinates from string
def coordinatesFromInput(text):
    # split
    coord = text.split()
    # convet to int
    coord = [int(i) for i in coord]
    return coord



# return all available displacements
def getLegalDisplacements(coordinates, isFirstMove=True):
    
    possibleDisplacements = []

    row = coordinates[0]
    col = coordinates[1]
    player = board[row][col].player

    # different if the player is facing up:
    # need to *-1 the row if facing up
    mult = 1
    if player.isFacingUp:
        mult = -1
    # if it's not first move you can only move by (+-2, +-2)
    if isFirstMove:
        possibleDisplacements.append((1 * mult, -1))
        possibleDisplacements.append((1 * mult, 1))
    possibleDisplacements.append((2 * mult, -2))
    possibleDisplacements.append((2 * mult, 2))
    if board[row][col].rank == PieceRank.KING:
        if isFirstMove:
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



# undo
def undo(move):

    undoPosition = (move.originPosition[0] - move.displacement[0], move.originPosition[1] - move.displacement[1])
    
    # undo position
    board[move.originPosition[0]][move.originPosition[1]] = board[undoPosition[0]][undoPosition[1]]

    # undo eat
    if abs(move.displacement[0]) == 2 and abs(move.displacement[1]) == 2:
        board[move.originPosition[0] - int(move.displacement[0] / 2)][move.originPosition[1] - int(move.displacement[1] / 2)] = pieceEaten

    # undo becoming king
    if move.doesBecomeKing:
        board[undoPosition[0]][undoPosition[1]].undoBecomingKing()



# check victory
def checkVictory(player):
    virctory = True
    for row in board:
        for square in row:
            if type(square) is Piece:
                if not square.player == player:
                    victory = False
    return victory



# starred string
def starred(message):
    starLine = "****"
    for i in message:
        starLine += "*"
    return(starLine + "\n" + "* " + message + " *\n" +starLine)



# setup pieces
def setupPieces():
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



# replay
def replay(moves):

    timeToWait = 1.5

    # board     
    board = [[emptySquare for col in range(boardDimention)] for row in range(boardDimention)]
    # ...

    printBoard()
    time.sleep(timeToWait)

    # create a list of moves
    movesToReplay = moves[:]
    
    # invert moves list
    movesToReplay.reverse()

    # replay
    while not movesToReplay == []:
        moveToReplay = movesToReplay.pop()

        # move piece
        board[movesToReplay.originPosition[0] + movesToReplay.displacement[0]][movesToReplay.originPosition[1] + movesToReplay.displacement[1]] = board[movesToReplay.originPosition[0]][movesToReplay.originPosition[1]]
        board[movesToReplay.originPosition[0]][movesToReplay.originPosition[1]] = emptySquare

        # eat
        if abs(movesToReplay.displacement[0]) == 2 and abs(movesToReplay.displacement[1]) == 2:
            board[movesToReplay.originPosition[0] + int(displacement[0] / 2)][movesToReplay.originPosition[0] + int(movesToReplay.displacement[1] / 2)] = movesToReplay.pieceEaten

        # become king
        if movesToReplay.doesBecomeKing:
            board[movesToReplay.originPosition[0] + movesToReplay.displacement[0]][movesToReplay.originPosition[1] + movesToReplay.displacement[1]].becomesKing()

        time.sleep(timeToWait)

    print("Replay ended.")



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
setupPieces()

# create a history of moves
moves = []

# game loop
winningPlayer = ""
someoneWins = False
while not someoneWins:
    for player in players:

        printBoard()   
    
        # SELECT A PIECE
        rowSelected = ""
        colSelected = ""
        while rowSelected == "" and colSelected == "":
            stringToPrintToUser = "Select piece " + player.symbols[PieceRank.MAN] + " > "
            textInput = input(stringToPrintToUser)
            # TEST - replay ##############################################################
            if textInput == "r" or textInput == "replay":
                replay(moves)
            ##############################################################################
            tempRow, tempCol = coordinatesFromInput(textInput)
            # select it if there is a piece
            # and it belongs to the player
            # and it can be moved
            squareToCheck = board[tempRow][tempCol]
            if (type(squareToCheck) is Piece):
                if (squareToCheck.player == player):
                    if not getLegalDisplacements((tempRow, tempCol)) == []:
                        rowSelected = tempRow
                        colSelected = tempCol
                    else:
                        print("This piece can't move.")
                else:
                    print("Not your piece.")
            else:
                print("No piece here.")

        # TURN (multiple moves)
        isFirstMove = True
        turnIsOver = False
        while not turnIsOver:

            # for storing move
            doesBecomeKing = False
            displacement = (0, 0)
            pieceEaten = ""

            # print borard with selection and availale moves
            legalDisplacements = getLegalDisplacements((rowSelected, colSelected), isFirstMove)
            printBoard((rowSelected, colSelected), [(rowSelected + d[0], colSelected + d[1]) for d in legalDisplacements])
                
            # DO A MOVE
            # Note: the move is legal (already checked)
            newRow, newCol = -1, -1
            moveExecuted = False
            while not moveExecuted:
                textInput = input("Move to > ")
                newRow, newCol = coordinatesFromInput(textInput)
                temporaryDisplacement = (newRow - rowSelected, newCol - colSelected)
                # if its a legal move
                if temporaryDisplacement in legalDisplacements:
                    displacement = temporaryDisplacement
                    board[newRow][newCol] = board[rowSelected][colSelected]
                    board[rowSelected][colSelected] = emptySquare
                    # eat
                    # if the displacement is (+-2, +-2)
                    if abs(displacement[0]) == 2 and abs(displacement[1]) == 2:
                        pieceEaten = board[rowSelected + int(displacement[0] / 2)][colSelected + int(displacement[1] / 2)]
                        board[rowSelected + int(displacement[0] / 2)][colSelected + int(displacement[1] / 2)] = emptySquare
                    # become king
                    if player.isFacingUp and newRow == 0:
                        board[newRow][newCol].becomesKing()
                        doesBecomeKing = True
                    elif newRow == boardDimention - 1:
                        board[newRow][newCol].becomesKing()
                        doesBecomeKing = True
                    moveExecuted = True
                else:
                    print("Not a legal move.")

            # STORE MOVE
            newMove = Move((rowSelected, colSelected), displacement, pieceEaten, doesBecomeKing)
            moves.append(newMove)
            #print("Move " + str(len(moves) - 1) + " stored: from " + str((rowSelected, colSelected)) + " moved by " + str(displacement))

            # check if you win (only if you eat)
            if abs(displacement[0]) == 2 and abs(displacement[1]) == 2:
                if checkVictory(player):
                    someoneWins = True
                    winningPlayer = player

            # check if turn is over
            #print("isFirstMove = False")
            isFirstMove = False
            # select next square and check if there are possible moves
            # but only if you have eaten
            if abs(displacement[0]) == 2 and abs(displacement[1]) == 2:
                rowSelected = newRow
                colSelected = newCol
                #print("This turn you have eaten a piece.")
                if getLegalDisplacements((rowSelected, colSelected), isFirstMove) == []:
                    #print("No more pieces to eat.")
                    turnIsOver = True
            else:
                #print("You did not eat this turn.")
                turnIsOver = True

# someone wins
print()
print()
print(starred("Player " + winningPlayer.symbols[PieceRank.MAN] + " win!"))
print()

# ask for replay
replayRequested = input("Would you like to replay the game? (y/n)")
if (replayRequested == "y"):
    replay(moves)
