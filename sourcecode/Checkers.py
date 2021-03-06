############
# CHECKERS #
############


import time
import random

from enum import Enum
class PieceRank(Enum):
    MAN = 0
    KING = 1
class ActionType(Enum):
    MOVE = 0
    UNDO = 1
    REDO = 2
    REPLAY = 3
    NONE = 4



# print board
def printBoard(board, piecesHighlights=[], legalMovesHighlights=[]):

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
                if (rowNo, colNo) in piecesHighlights:
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

    def __init__(self, symbols, isFacingUp=False, cpu=True):
        # symbol[0] is for Man, [1] is for King
        self.symbols = {PieceRank.MAN: symbols[0], PieceRank.KING: symbols[1]}
        # remember the player side on the board
        self.isFacingUp = isFacingUp
        self.cpu = cpu

    def cpuSelectPiece(self, mustEat):
        coordinatesThatCanBeSelected = []
        for rowNo, row in enumerate(board):
            for colNo, square in enumerate(row):
                if type(square) is Piece:
                    if square.player == self and not getLegalDisplacements((rowNo, colNo), mustEat) == []:
                        coordinatesThatCanBeSelected.append(((rowNo, colNo)))
        #print("coordinatesThatCanBeSelected = " + str(coordinatesThatCanBeSelected))
        return random.choice(coordinatesThatCanBeSelected)

    def cpuSelectDisplacement(self, displacements):
        return random.choice(displacements)
        



# piece class
class Piece:

    def __init__(self, player):
        self.player = player
        self.rank = PieceRank.MAN

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
def undo(movesNo=1):

    for moveNo in range(movesNo):

        move = moves.pop();

        # push move to redo
        redoMoves.append(move);

        undoDisplacement = (move.displacement[0] * -1, move.displacement[1] * -1)
        undoFrom = (move.originPosition[0] + move.displacement[0], move.originPosition[1] + move.displacement[1])
        undoTo = (move.originPosition[0], move.originPosition[1])

        # undo position
        board[undoTo[0]][undoTo[1]] = board[undoFrom[0]][undoFrom[1]]
        board[undoFrom[0]][undoFrom[1]] = emptySquare

        # undo eat
        if abs(move.displacement[0]) == 2 and abs(move.displacement[1]) == 2:
            board[undoFrom[0] + int(undoDisplacement[0] / 2)][undoFrom[1] + int(undoDisplacement[1] / 2)] = move.pieceEaten

        # undo become king
        if move.doesBecomeKing:
            board[undoTo[0]][undoTo[1]].undoBecomingKing()



# redo
def redo(movesNo=1):

    for moveNo in range(movesNo):

        move = redoMoves.pop();

        # push move to undo
        moves.append(move);

        redoFrom = (move.originPosition[0], move.originPosition[1])
        redoTo = (move.originPosition[0] + move.displacement[0], move.originPosition[1] + move.displacement[1])

        # redo position
        board[redoTo[0]][redoTo[1]] = board[redoFrom[0]][redoFrom[1]]
        board[redoFrom[0]][redoFrom[1]] = emptySquare

        # redo eat
        if abs(move.displacement[0]) == 2 and abs(move.displacement[1]) == 2:
            board[redoFrom[0] + int(move.displacement[0] / 2)][redoFrom[1] + int(move.displacement[1] / 2)] = emptySquare

        # redo becoming king
        if move.doesBecomeKing:
            board[redoTo[0]][redoTo[1]].becomesKing();



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
    leftMargin = "                       "
    starLine = "****"
    for i in message:
        starLine += "*"
    return(leftMargin + starLine + "\n" + leftMargin +  "* " + message + " *\n" + leftMargin + starLine)



# setup pieces
def setupPieces(board):
    for player in players:
        for row in range(3):
            for col in range(boardDimention):
                if (col + row) % 2 == 0:
                    newPiece = Piece(player)
                    if player.isFacingUp:
                        initialPosition = (boardDimention - 1 - (boardDimention + row), boardDimention - 1 - (boardDimention + col))
                    else:
                        initialPosition = (row, col)
                    board[initialPosition[0]][initialPosition[1]] = newPiece



# replay
def replay():

    timeToWait = 1.5

    totalNumberOfMoves = len(moves)

    # undo everything
    undo(totalNumberOfMoves)
    printBoard(board)
    time.sleep(timeToWait)
    print("Replay...")

    # redo eveything, but wait and show every moves
    for moveToRedo in range(totalNumberOfMoves):
        redo()
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
timeToWait = 1.5

for player in players:
    validInput = False
    while not validInput:
        i = input("Is player " + player.symbols[PieceRank.MAN] + " [h]uman or [c]pu? > ")
        if i == "h" or i == "human":
            player.cpu = False
            validInput = True
        elif i == "c" or i == "cpu":
            player.cpu = True
            validInput = True
        else:
            print("Input not valid.")

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

    pieceSelected = None # (piece coord, [displacements])
    movesToUndo = None
    movesToRedo = None
    
    actionSelected = None;

    # get list of all movable pieces with respective displacements
    # + check if you must eat
    # + check if player can move
    mustEat = False
    canMove = False
    movablePieces = [] # [(piece coord, [displacements])]
    for rowNo, row in enumerate(board):
        for colNo, square in enumerate(row):
            if type(square) is Piece:
                if square.player == player:
                    displacements = getLegalDisplacements((rowNo, colNo))
                    if not displacements == []:
                        movablePieces.append(((rowNo, colNo), displacements))
                        canMove = True
                        if (+2, +2) in displacements or (-2, -2) in displacements or (+2, -2) in displacements or (-2, +2) in displacements:
                            mustEat = True
    # if player must eat keep only pieces that eat
    if mustEat and canMove:
        newListOfPieces = []
        for p in movablePieces:
            if (+2, +2) in p[1] or (-2, -2) in p[1] or (+2, -2) in p[1] or (-2, +2) in p[1]:
                newListOfPieces.append((p[0], getLegalDisplacements((p[0][0], p[0][1]), mustEat=mustEat)))
        movablePieces = newListOfPieces
    
    printBoard(board, piecesHighlights=[p[0] for p in movablePieces])

    # SELECT AN ACTION (move, undo, etc.)
    # if human, select action
    if player.cpu == False:
        while actionSelected == None:
            print()
            print("Player " + player.symbols[PieceRank.MAN])
            if mustEat:
                print("Note: you must eat")
            if not canMove:
                print("Note: you cannot move this turn")
            actionToChek = input("([m]ove r c / [u]ndo x / [r]edo x / [replay] / [n]one) > ")
            # spilt actionToChek into arguments
            actionToChek = actionToChek.split()
            # check if the the input is valid
            
            if actionToChek[0] == "n" or actionToChek == "none":
                # check if you can skip this turn
                if len(actionToChek) == 1:
                    if not canMove:
                        actionSelected = ActionType.NONE
                    else:
                        print("You can skip your turn only if you can't move.")
                else:
                    print("Wrong number of arguments.")
                    
            elif actionToChek[0] == "m" or actionToChek == "move":
                # Check if you can move
                if canMove:
                    if len(actionToChek) == 3:
                        try:
                            tempRow, tempCol = int(actionToChek[1]), int(actionToChek[2])
                        except ValueError:
                            print("Coordinates must be numbers.")
                            continue
                        else:
                            tempRow, tempCol = int(actionToChek[1]), int(actionToChek[2])
                            if (tempRow, tempCol) in [p[0] for p in movablePieces]:
                                pieceSelected = ((tempRow, tempCol), getLegalDisplacements((tempRow, tempCol), mustEat))
                                actionSelected = ActionType.MOVE
                            else:
                                print("Coordinates not valid")
                    else:
                        print("Wrong number of arguments.")
                else:
                    print("You cannot move this turn")
                    
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
                
    # else if cpu, can only move
    else:
        print("Player " + player.symbols[PieceRank.MAN] + " is thinking...")
        if canMove:
            pieceCoord = player.cpuSelectPiece(mustEat)
            pieceSelected = (pieceCoord, getLegalDisplacements(pieceCoord, mustEat))
            actionSelected = ActionType.MOVE
        else:
            actionSelected = ActionType.NONE
        time.sleep(timeToWait)


    # DO ACTION
    if actionSelected == ActionType.MOVE:


        # MOVES
        rowSelected, colSelected = pieceSelected[0][0], pieceSelected[0][1]
        moveActionIsOver = False
        while not moveActionIsOver:

            # for storing move
            doesBecomeKing = False
            displacement = None
            pieceEaten = None

            # must recalculate legal displacements, because it has to change on every loop
            legalDisplacements = getLegalDisplacements((rowSelected, colSelected), mustEat)

            # print borard with selection and availale moves
            squaresPlayerCanMoveTo = [(rowSelected + d[0], colSelected + d[1]) for d in legalDisplacements]
            printBoard(board, [(rowSelected, colSelected)], squaresPlayerCanMoveTo)

            # SELECT WHERE TO MOVE
            # Note: the piece to move is legal (already checked)
            newRow, newCol = None, None
            moveIsSelected = False
            temporaryDisplacement = None
            while not moveIsSelected:
                
                # if human select where to move to
                if player.cpu == False:
                    textInput = input("Move to > ")
                    textInput = textInput.split()
                    if len(textInput) == 2:
                        try:
                            newRow, newCol = int(textInput[0]), int(textInput[1])
                        except ValueError:
                            print("Coordinates must be a numbers.")
                            continue
                        else:
                            newRow, newCol = int(textInput[0]), int(textInput[1])
                            temporaryDisplacement = (newRow - rowSelected, newCol - colSelected)
                            if temporaryDisplacement in legalDisplacements:
                                moveIsSelected = True
                            else:
                                print("Not a legal move.")
                    else:
                        print ("Wrong number of arguments")
                # else if cpu, choose a displacement
                else:
                    print("Player " + player.symbols[PieceRank.MAN] + " is thinking...")
                    temporaryDisplacement = player.cpuSelectDisplacement(legalDisplacements)
                    newRow, newCol = (rowSelected + temporaryDisplacement[0], colSelected + temporaryDisplacement[1])
                    time.sleep(timeToWait)
                    moveIsSelected = True
                    
            # DO THE MOVE
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

            # next move you must eat
            mustEat = True

            # STORE MOVE
            newMove = Move((rowSelected, colSelected), displacement, pieceEaten, doesBecomeKing)
            moves.append(newMove)
            # empty redoMoves
            redoMoves = []

            # check if you win (only if you eat)
            if abs(displacement[0]) == 2 and abs(displacement[1]) == 2:
                if checkVictory(player):
                    someoneWins = True
                    winningPlayer = player

            # check if turn is over
            mustEat = True
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


    elif actionSelected == ActionType.NONE:

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
        player = board[redoMoves[-1].originPosition[0]][redoMoves[-1].originPosition[1]].player

    elif actionSelected == ActionType.REDO:

        # REDO
        # Note: movesToRedo is legal (already checked)
        redo(movesToRedo)

        # CHANGE PLAYER
        player = board[moves[-1].originPosition[0] - moves[-1].displacement[0]][moves[-1].originPosition[1] - moves[-1].displacement[1]].player

    elif actionSelected == ActionType.REPLAY:

        # REPLAY
        replay()
        # (do not change player)



# someone wins
printBoard(board)
print(starred("Player " + winningPlayer.symbols[PieceRank.MAN] + " win!"))
print()

# ask for replay
replayRequested = input("Would you like to replay the game? (y/n) > ")
if replayRequested == "y":
    replay()

stop = input()
