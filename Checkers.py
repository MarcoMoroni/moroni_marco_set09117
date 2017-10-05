############
# CHECKERS #
############

boardDimension = 8
emptySquareChar = '.'

board = [[emptySquareChar for col in range(boardDimension)] for row in range(boardDimension)]

def printBoard(board):
    for row in board:
        for col in row:
            print(col, end='')
        print()

printBoard(board)
