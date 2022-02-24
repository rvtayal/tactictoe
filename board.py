import numpy as np

class TacTicToeBoard:

    def __init__(self):
        self.board = np.zeros((9,9), dtype=int)
        self.turn = 'x'
        self.move_history = []


    def move(self, move):
        row, col = move
        # check if spot is filled
        if self.board[row, col] != 0:
            return False
        # check if 


    # a function that outputs the indices of the board the player needs to 
    # move in next
    def prev_move_to_small_board(self):
        pRow, pCol = self.move_history[-1]
        smallBoardR, smallBoardC = pRow%3, pCol%3
        rows = list(range(smallBoardR*3, smallBoardR*3 + 3))
        cols = list(range(smallBoardC*3, smallBoardC*3 + 3))
        indx = []
        for r in rows:
            for c in cols:
                indx.append((r,c))
        return indx


    def get_legal_moves(self):
        # base case
        if len(self.move_history) == 0:
            legal_moves = [(i%9,int(np.floor(i/9))) for i in range(81)]
        else:
            rows, cols = np.where(self.board == 0)
            unfilled_spaces = list(zip(rows, cols))
            spaces = self.prev_move_to_small_board()
            legal_moves = list(set(unfilled_spaces) & set(spaces))
        return legal_moves


    def raw_print(self):
        print("board: \n{}".format(self.board))
        print("turn: {}".format(self.turn))
        print("move history: {}".format(self.move_history))

def main():
    b = TacTicToeBoard()
    b.move_history.append((1,1))
    b.board[0,0] = 1
    b.raw_print()
    print(b.get_legal_moves())

if __name__ == "__main__":
    main()