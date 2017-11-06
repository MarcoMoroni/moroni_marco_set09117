############
# CHECKERS #
############


import time

from enum import Enum
class PieceRank(Enum):
    MAN = 0
    KING = 1
class ActionType(Enum):
    MOVE = 0
    UNDO = 1
    REDO = 2
    REPLAY = 3



# print board
def printBoard(board, selectedPieceHighlight=(-1, -1), legalMovesHighlights=[]):

    topMarginChars = 10
    leftMarginChars = 10
    bottomMarginChars = 5

    # top margin
    for l in range(topMarginChars):
        print()

    # left margin
    leftMargin = ""
    for l in range(leftMarginChars):
        leftMargin += " "

    # create the line for col number
    line = leftMargin + "    "
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
    print(leftMargin + firstLine)

    # print everithing else
    for rowNo, row in enumerate(board):
        # print row number
        print(leftMargin + str(rowNo), end="   ")
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
            print("│\n" + leftMargin + line)
        else:
            print("│\n" + leftMargin + lastLine)

    # bottom margin
    for l in range(bottomMarginChars):
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

    def __init__(self, originPosition, displacement, pieceEaten=None, doesBecomeKing=False):
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
def getLegalDisplacements(coordinates, mustEat=False):

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
    if not mustEat:
        possibleDisplacements.append((1 * mult, -1))
        possibleDisplacements.append((1 * mult, 1))
    possibleDisplacements.append((2 * mult, -2))
    possibleDisplacements.append((2 * mult, 2))
    if board[row][col].rank == PieceRank.KING:
        if not mustEat:
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
##def undo(move):
##
##    undoPosition = (move.originPosition[0] - move.displacement[0], move.originPosition[1] - move.displacement[1])
##
##    # undo position
##    board[move.originPosition[0]][move.originPosition[1]] = board[undoPosition[0]][undoPosition[1]]
##
##    # undo eat
##    if abs(move.displacement[0]) == 2 and abs(move.displacement[1]) == 2:
##        board[move.originPosition[0] - int(move.displacement[0] / 2)][move.originPosition[1] - int(move.displacement[1] / 2)] = pieceEaten
##
##    # undo becoming king
##    if move.doesBecomeKing:
##        board[undoPosition[0]][undoPosition[1]].undoBecomingKing()



# undo
def undo(movesNo):

    for moveNo in range(movesNo):

        move = moves.pop();

        # push move to redo
        redoMoves.append(move);

        undoPosition = (move.originPosition[0] + move.displacement[0], move.originPosition[1] + move.displacement[1])

        # undo position
        board[move.originPosition[0]][move.originPosition[1]] = board[undoPosition[0]][undoPosition[1]]

        # undo eat
        if abs(move.displacement[0]) == 2 and abs(move.displacement[1]) == 2:
            board[move.originPosition[0] + int(move.displacement[0] / 2)][move.originPosition[1] + int(move.displacement[1] / 2)] = pieceEaten

        # undo becoming king
        if move.doesBecomeKing:
            board[undoPosition[0]][undoPosition[1]].undoBecomingKing()

        # empty the "from" square
        board[move.originPosition[0] + move.displacement[0]][move.originPosition[1] + move.displacement[1]] = emptySquare



# redo
def redo(movesNo):

    for moveNo in range(movesNo):

        move = redoMoves.pop();

        # push move to undo
        moves.append(move);

        # redo position
        board[move.originPosition[0] + move.displacement[0]][move.originPosition[1] + move.displacement[1]] = board[move.originPosition[0]][move.originPosition[1]]

        # redo eat
        if abs(move.displacement[0]) == 2 and abs(move.displacement[1]) == 2:
           board[move.originPosition[0] + int(displacement[0] / 2)][move.originPosition[1] + int(displacement[1] / 2)] = emptySquare

        # redo becoming king
        if move.doesBecomeKing:
            board[move.originPosition[0] + move.displacement[0]][move.originPosition[1] + move.displacement[1]].becomesKing()

        # empty the "from" square
        board[move.originPosition[0]][move.originPosition[1]] = emptySquare



# check victory
def checkVictory(player):
    victory = True
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
def setupPieces(board):
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
def replay():

    timeToWait = 1.5

##    # board
##    board = [[emptySquare for col in range(boardDimention)] for row in range(boardDimention)]
##    setupPieces(board)
##
##    printBoard(board)
##    time.sleep(timeToWait)
##
##    # create a list of moves
##    movesToReplay = moves[:]
##
##    # replay
##    while not movesToReplay == []:
##        moveToReplay = movesToReplay.pop(0)
##
##        # move piece
##        #print("Moving " + str(moveToReplay.originPosition[0]), str(moveToReplay.originPosition[1]) + " by " + str(moveToReplay.displacement[0]), str(moveToReplay.displacement[1]))
##        board[moveToReplay.originPosition[0] + moveToReplay.displacement[0]][moveToReplay.originPosition[1] + moveToReplay.displacement[1]] = board[moveToReplay.originPosition[0]][moveToReplay.originPosition[1]]
##        board[moveToReplay.originPosition[0]][moveToReplay.originPosition[1]] = emptySquare
##
##        # eat
##        if abs(moveToReplay.displacement[0]) == 2 and abs(moveToReplay.displacement[1]) == 2:
##            board[moveToReplay.originPosition[0] + int(displacement[0] / 2)][moveToReplay.originPosition[0] + int(moveToReplay.displacement[1] / 2)] = moveToReplay.pieceEaten
##
##        # become king
##        if moveToReplay.doesBecomeKing:
##            board[moveToReplay.originPosition[0] + moveToReplay.displacement[0]][moveToReplay.originPosition[1] + moveToReplay.displacement[1]].becomesKing()
##
##        printBoard(board)
##        time.sleep(timeToWait)

    totalNumberOfMoves = len(moves)
    # need to use this, or I have problem in for loops

    # undo everything
    undo(totalNumberOfMoves)
    printBoard(board)
    time.sleep(timeToWait)
    print("Replay...")

    # redo eveything, but wait and show every moves
    for moveToRedo in range(totalNumberOfMoves):
        redo(1)
        printBoard(board)
        time.sleep(timeToWait)
        print("Replay...")

    print("Replay ended.")



# create board
boardDimention = 8
emptySquare = None
board = [[emptySquare for col in range(boardDimention)] for row in range(boardDimention)]

# create players
p1 = Player(["○", "□"], isFacingUp=True)
p2 = Player(["●", "■"])
players = []
players.append(p1)
players.append(p2)

# pieces setup
setupPieces(board)

# create a history of moves
moves = []

# create a history of undone moves
redoMoves = []

# game loop
winningPlayer = None
someoneWins = False
player = p1
while not someoneWins:

    printBoard(board=board)

    rowSelected = None
    colSelected = None
    movesToUndo = None
    movesToRedo = None

    # check if you must eat
    mustEat = False
    for rowNo, row in enumerate(board):
        for colNo, square in enumerate(row):
            if type(square) is Piece:
                if square.player == player:
                    legalDisplacements = getLegalDisplacements((rowNo, colNo), mustEat=False)
                    if (+2, +2) in legalDisplacements or (-2, -2) in legalDisplacements or (+2, -2) in legalDisplacements or (-2, +2) in legalDisplacements:
                        mustEat = True
            if mustEat:
                break
        if mustEat:
            break

    # SELECT AN ACTION (move, undo, etc.)
    actionSelected = None;
    while actionSelected == None:
        print()
        print("Player " + player.symbols[PieceRank.MAN])
        if mustEat:
            print("Note: you must eat")
        actionToChek = input("([m]ove r c / [u]ndo x / [r]edo x / [replay]) > ")
        # spilt actionToChek into arguments
        actionToChek = actionToChek.split()
        # check if the the input is valid
        if actionToChek[0] == "m" or actionToChek == "move":
            # Check if you can move
            if len(actionToChek) == 3:
                try:
                    tempRow, tempCol = int(actionToChek[1]), int(actionToChek[2])
                except ValueError:
                    print("Coordinates must be numbers.")
                    continue
                else:
                    tempRow, tempCol = int(actionToChek[1]), int(actionToChek[2])
                    squareToCheck = board[tempRow][tempCol]
                    if (type(squareToCheck) is Piece):
                        if (squareToCheck.player == player):
                            if not getLegalDisplacements((tempRow, tempCol), mustEat) == []:
                                rowSelected = tempRow
                                colSelected = tempCol
                                actionSelected = ActionType.MOVE
                            else:
                                print("This piece can't move.")
                        else:
                            print("Not your piece.")
                    else:
                        print("No piece here.")
            else:
                print("Wrong number of arguments.")
        elif actionToChek[0] == "u" or actionToChek == "undo":
            # Check if you can undo
            if len(actionToChek) == 1 and len(moves) > 0:
                movesToUndo = 1
                actionSelected = ActionType.UNDO
            elif len(actionToChek) == 2:
                try:
                    movesToUndo = int(actionToChek[1])
                except ValueError:
                    print("Number of moves must be a number.")
                    continue
                else:
                    movesToUndo = int(actionToChek[1])
                    if movesToUndo <= len(moves) and not movesToUndo == 0:
                        actionSelected = ActionType.UNDO
                    else:
                        print("Not a valid number of moves.")
            else:
                print("Undo not valid.")
        elif actionToChek[0] == "r" or actionToChek == "redo":
            # Check if you can redo
            if len(actionToChek) == 1 and len(redoMoves) > 0:
                movesToRedo = 1
                actionSelected = ActionType.REDO
            elif len(actionToChek) == 2:
                try:
                    movesToRedo = int(actionToChek[1])
                except ValueError:
                    print("Number of moves must be a number.")
                    continue
                else:
                    movesToRedo = int(actionToChek[1])
                    if movesToRedo <= len(redoMoves) and not movesToRedo == 0:
                        actionSelected = ActionType.REDO
                    else:
                        print("Not a valid number of moves.")
            else:
                print("Redo not valid.")
        elif actionToChek[0] == "replay":
            # Check if you can replay
            if len(actionToChek) == 1:
                actionSelected = ActionType.REPLAY
            else:
                print("Input not valid.")
        else:
            print("Input not valid.")

    # SELECT A PIECE
##        rowSelected = None
##        colSelected = None
##        while rowSelected == None and colSelected == None:
##            stringToPrintToUser = "Select piece " + player.symbols[PieceRank.MAN] + " > "
##            textInput = input(stringToPrintToUser)
##            tempRow, tempCol = coordinatesFromInput(textInput)
##            # select it if there is a piece
##            # and it belongs to the player
##            # and it can be moved
##            squareToCheck = board[tempRow][tempCol]
##            if (type(squareToCheck) is Piece):
##                if (squareToCheck.player == player):
##                    if not getLegalDisplacements((tempRow, tempCol)) == []:
##                        rowSelected = tempRow
##                        colSelected = tempCol
##                    else:
##                        print("This piece can't move.")
##                else:
##                    print("Not your piece.")
##            else:
##                print("No piece here.")

    # DO ACTION
    if actionSelected == ActionType.MOVE:


        # MOVES
        moveActionIsOver = False
        while not moveActionIsOver:

            # for storing move
            doesBecomeKing = False
            displacement = (0, 0)
            pieceEaten = None

            # print borard with selection and availale moves
            legalDisplacements = getLegalDisplacements((rowSelected, colSelected), mustEat)
            printBoard(board, (rowSelected, colSelected), [(rowSelected + d[0], colSelected + d[1]) for d in legalDisplacements])

            # DO A MOVE
            # Note: the piece to move is legal (already checked)
            newRow, newCol = -1, -1
            moveExecuted = False
            while not moveExecuted:
                textInput = input("Move to > ")
                try:
                    newRow, newCol = coordinatesFromInput(textInput)
                except ValueError:
                    print("Coordinates must be a numbers.")
                    continue
                else:
                    newRow, newCol = coordinatesFromInput(textInput)
                    temporaryDisplacement = (newRow - rowSelected, newCol - colSelected)
                    # if it's a legal move
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

            # next move you must eat
            mustEat = True

            # STORE MOVE
            newMove = Move((rowSelected, colSelected), displacement, pieceEaten, doesBecomeKing)
            moves.append(newMove)
            #print("Move " + str(len(moves) - 1) + " stored: from " + str((rowSelected, colSelected)) + " moved by " + str(displacement))
            # empty redoMoves
            redoMoves = []

            # check if you win (only if you eat)
            if abs(displacement[0]) == 2 and abs(displacement[1]) == 2:
                if checkVictory(player):
                    someoneWins = True
                    winningPlayer = player

            # check if turn is over
            #print("mustEat = False")
            mustEat = False
            # select next square and check if there are possible moves
            # but only if you have eaten
            if abs(displacement[0]) == 2 and abs(displacement[1]) == 2:
                rowSelected = newRow
                colSelected = newCol
                #print("This turn you have eaten a piece.")
                if getLegalDisplacements((rowSelected, colSelected), mustEat) == []:
                    #print("No more pieces to eat.")
                    moveActionIsOver = True
            else:
                #print("You did not eat this turn.")
                moveActionIsOver = True

        # CHANGE PLAYER
        # (other player)
        if player == players[0]:
            player = players[1]
        else:
            player = players[0]


    elif actionSelected == ActionType.UNDO:

        # UNDO
        # Note: movesToUndo is legal (already checked)
        undo(movesToUndo)

        # CHANGE PLAYER
        print("Changing player to player like the one in " + str(redoMoves[-1].originPosition[0]), str(redoMoves[-1].originPosition[1]))
        player = board[redoMoves[-1].originPosition[0]][redoMoves[-1].originPosition[1]].player

    elif actionSelected == ActionType.REDO:

        # REDO
        # Note: movesToRedo is legal (already checked)
        redo(movesToRedo)

        # CHANGE PLAYER
        print("Changing player to player like the one in " + str(moves[-1].originPosition[0] - moves[-1].displacement[0]), str(moves[-1].originPosition[1] - moves[-1].displacement[1]))
        player = board[moves[-1].originPosition[0] - moves[-1].displacement[0]][moves[-1].originPosition[1] - moves[-1].displacement[1]].player

    elif actionSelected == ActionType.REPLAY:

        # REPLAY
        replay()
        # (do not change player)



# someone wins
print()
print()
print(starred("Player " + winningPlayer.symbols[PieceRank.MAN] + " win!"))
print()

# ask for replay
replayRequested = input("Would you like to replay the game? (y/n)")
if (replayRequested == "y"):
    replay()
