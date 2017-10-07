############
# CHECKERS #
############

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

printBoard()
