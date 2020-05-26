import numpy as np
import math

class SmallBoard:
    def __init__(self):
        self.winner = None
        self.board = np.zeros((3,3))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            otherboard = other.board
            for i in range(3):
                for j in range(3):
                    if otherboard[i,j] != self.board[i,j]:
                        return False
            return True
        else:
            return False

    def checkWinner(self):
        if self.winner is None:
            self.checkRows()
            self.checkCols()
            self.checkDiags()

    def checkRows(self):
        if any(np.sum(self.board, axis=1)==3):
            self.winner = 'x'
        elif any(np.sum(self.board, axis=1)==-3):
            self.winner = 'o'

    def checkCols(self):
        if any(np.sum(self.board, axis=0)==3):
            self.winner = 'x'
        elif any(np.sum(self.board, axis=0)==-3):
            self.winner = 'o'

    def checkDiags(self):
        s = self.board[0,0] + self.board[1,1] + self.board[2,2]
        if s == 3:
            self.winner = 'x'
        elif s ==-3:
            self.winner = 'o'
        s = self.board[2,0] + self.board[1,1] + self.board[0,2]
        if s == 3:
            self.winner = 'x'
        elif s ==-3:
            self.winner = 'o'

    def getCharArray(self):
        chAr = np.empty((3,3), dtype='str')
        for i in range(3):
            for j in range(3):
                ch = self.board[i,j]
                if ch == 1:
                    chAr[i,j] = 'X'
                elif ch == -1:
                    chAr[i,j] = 'O'
                else:
                    chAr[i,j] = ' '
        return chAr

    def move(self, who, row, col):
        if who not in ['x', 'o']:
            return False
        if row not in [0, 1, 2] or col not in [0, 1, 2]:
            return False
        if self.board[row,col] != 0:
            return False
        if self.winner is not None:
            return False
        if who is 'x':
            self.board[row,col] = 1
        else:
            self.board[row,col] = -1
        self.checkWinner()
        return True

    def getDisplay(self, p=False):
        disp = np.empty((5,5), dtype='str')
        if self.winner is None:
            disp[0, [1, 3]] = '|'
            disp[2, [1, 3]] = '|'
            disp[4, [1, 3]] = '|'
            disp[[1, 3], 0] = '-'
            disp[[1, 3], 2] = '-'
            disp[[1, 3], 4] = '-'
            disp[[1, 3], 1] = '+'
            disp[[1, 3], 3] = '+'

            chAr = self.getCharArray()
            for i in range(3):
                for j in range(3):
                    disp[i*2, j*2] = chAr[i,j]
        elif self.winner is 'x':
            disp[:, :] = ' '
            disp[0, 0] = '\\'
            disp[1, 1] = '\\'
            disp[3, 3] = '\\'
            disp[4, 4] = '\\'
            disp[0, 4] = '/'
            disp[1, 3] = '/'
            disp[3, 1] = '/'
            disp[4, 0] = '/'
            disp[2, 2] = 'X'
        else:
            disp[:, :] = ' '
            disp[[1, 2, 3], 0] = '|'
            disp[[1, 2, 3], 4] = '|'
            disp[0, [1, 2, 3]] = '-'
            disp[4, [1, 2, 3]] = '-'

        if p:
            for i in range(5):
                row = ''
                for j in range(5):
                    row += disp[i,j] + ' '
                print(row)

        return disp

class LargeBoard:
    def __init__(self):
        self.boards = []
        for i in range(9):
            self.boards.append(SmallBoard())
        self.winners = np.zeros((9,))
        self.winner = None
        self.prevMove = None

    def checkWinner(self):
        for i in range(9):
            if self.boards[i].winner is not None:
                self.winners[i] = self.boards[i].winner
        if self.winner is None:
            self.checkRows()
            self.checkCols()
            self.checkDiags()

    def checkRows(self):
        s = [np.sum(self.winners[:3]), np.sum(self.winners[3:6]), np.sum(self.winners[6:])]
        if 3 in s:
            self.winner = 'x'
        elif -3 in s:
            self.winner = 'o'

    def checkCols(self):
        s = [np.sum(self.winners[[0, 3, 6]]), np.sum(self.winners[[1, 4, 7]]), np.sum(self.winners[[2, 5, 8]])]
        if 3 in s:
            self.winner = 'x'
        elif -3 in s:
            self.winner = 'o'

    def checkDiags(self):
        s = [np.sum(self.winners[[0, 4, 8]]), np.sum(self.winners[[2, 4, 6]])]
        if 3 in s:
            self.winner = 'x'
        elif -3 in s:
            self.winner = 'o'

    def move(self, who, board, boardLoc):
        smallBoard = self.boards[board]
        if smallBoard.winner is not None:
            return False
        boardRow, boardCol = boardLoc
        ret = smallBoard.move(who, boardRow, boardCol)
        if not ret:
            return False
        else:
            self.checkWinner()
            self.prevMove = (board, boardLoc)
            return True

    def getStartRowCol(self, board):
        boardRow = math.floor(board/3)
        boardCol = board % 3
        c = (boardCol*8) + 2
        r = (boardRow*8) + 2
        return (int(r), int(c))
        
    def getDisplay(self, p=False):        
        disp = np.empty((25, 25), dtype='str')
        disp[:,:] = ' '
        disp[[8, 16], :] = '-'
        disp[:, [8, 16]] = '|'
        disp[[8, 16], 8] = '+'
        disp[[8, 16], 16] = '+'
        disp[[0, -1], :] = '='
        disp[:, [0, -1]] = '|'
        disp[1, 1] = '0'
        disp[1, 9] = '1'
        disp[1, 17] = '2'
        disp[9, 1] = '3'
        disp[9, 9] = '4'
        disp[9, 17] = '5'
        disp[17, 1] = '6'
        disp[17, 9] = '7'
        disp[17, 17] = '8'


        for boardnum in range(9):
            board = self.boards[boardnum]
            smallDisplay = board.getDisplay()
            startRow, startCol = self.getStartRowCol(boardnum)
            disp[startRow:startRow+5, startCol:startCol+5] = smallDisplay

        if p:
            for i in range(25):
                row = ''
                for j in range(25):
                    row += disp[i,j] + ' '
                print(row)
        return disp
                
def main():
    '''
    b = SmallBoard()
    b.move('x', 0, 1)
    b.move('o', 0, 2)
    b.move('x', 1, 1)
    b.move('o', 1, 2)
    b.move('x', 2, 1)
    b.move('o', 2, 2)
    print('char Array')
    print(b.getCharArray())
    print('display')
    b.getDisplay()
    print('board')
    print(b.board)
    print('winner')
    print(b.winner)
    '''
    b = LargeBoard()
    b.getDisplay(True)
    b.move('x', 5, (2, 0))
    b.getDisplay(True)
    b.move('o', 7, (1, 1))
    b.move('o', 7, (1, 0))
    b.move('o', 7, (1, 2))
    b.getDisplay(True)

if __name__ == "__main__":
    main()
