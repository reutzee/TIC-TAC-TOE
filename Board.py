from tkinter import *

class Board:
    """
    Board class to be used in the Game obj

    Attributes:
    color: the color of board
    canvas: frame which contain 3*3 cells
    available_cells: integer indicates empty cells for use
    dict_cells: for each 1...9 cells - its coordinates
    winning_combinations: all possible combinations to win TicTacToe
    """

    def __init__(self, root):
        self.color = "LightBlue1"
        self.canvas = Canvas(root, width=300, height=300)
        self.canvas.pack()
        self.available_cells = 9
        # draw board
        for x in range(3):
            for y in range(3):
                self.create_cell(x, y)

        self.dict_cells = {1: [0, 0, 100, 100],
                           2: [100, 0, 200, 100],
                           3: [200, 0, 300, 100],
                           4: [0, 100, 100, 200],
                           5: [100, 100, 200, 200],
                           6: [200, 100, 300, 200],
                           7: [0, 200, 100, 300],
                           8: [100, 200, 200, 300],
                           9: [200, 200, 300, 300]}

        self.winning_combinations = [{1, 2, 3},  # horizontal
                                    {4, 5, 6},
                                    {7, 8, 9},
                                    {1, 4, 7},  # vertical
                                    {2, 5, 8},
                                    {3, 6, 9},
                                    {1, 5, 9},  # diagonal
                                    {3, 5, 7}]

    def create_cell(self, row, col):
        self.canvas.create_rectangle(100 * col,
                                     100 * row,
                                     100 * (col + 1),
                                     100 * (row + 1),
                                     fill=self.color)