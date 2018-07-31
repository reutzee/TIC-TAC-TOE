from tkinter import *
import random
from Player import *
from Board import *
from itertools import permutations
from tkinter import messagebox


class TicTacToe:
    """
    GameApp class as controller for board and player objects

    Attributes:
    root: (tkinter.Tk) the root window, parent of the frame
    board: instance of the board class
    player1, player2: instances of player class
    chosen_player: current player at the game

    """
    def __init__(self, root):
        # controller
        self.root = root
        # create all players instances
        self.player1 = Player("Reut", "DarkOrchid2")
        self.player2 = Player("Computer", "dark green")
        self.players = [self.player1, self.player2]
        self.chosen_player = self.player1
        # create board
        self.board = Board(self.root)
        self.board.canvas.bind("<Button-1>", self.callback)
        # all coordinates
        self.all_coordinates = list(self.board.dict_cells.values())


    def restart(self):
        for player in self.players:
            player.selected_cells = set()
        self.chosen_player = self.player1
        self.board.canvas.destroy()
        # create a board & choosing the first player to start the game
        self.board = Board(self.root)
        self.board.canvas.bind("<Button-1>", self.callback)

    def got_chance_to_win(self):
        if len(self.chosen_player.selected_cells) > 1:
            for attempt_cells in permutations(self.chosen_player.selected_cells, 2):
                for win in self.board.winning_combinations:
                    if all([cell in win for cell in attempt_cells]):
                        abstract_cell = win.difference(attempt_cells).pop()
                        cell_coords = self.board.dict_cells[abstract_cell]
                        concrete_cell = self.board.canvas.find_closest(cell_coords[0], cell_coords[1])
                        if self.board.canvas.itemcget(concrete_cell, 'fill') != self.board.color:
                            continue
                        # found - FILL & WIN
                        self.board.canvas.itemconfig(concrete_cell, fill=self.chosen_player.color)
                        self.board.canvas.update_idletasks()

                        return True
        return False


    def computer_play(self):
        if self.got_chance_to_win():
            self.show_game_result(self.chosen_player)
            self.restart()
            return

        coords = self.all_coordinates[0]
        cell = self.board.canvas.find_closest(coords[0], coords[1])
        # search for available cell
        while self.board.canvas.itemcget(cell, 'fill') != self.board.color:
            coords = random.choice(self.all_coordinates)
            cell = self.board.canvas.find_closest(coords[0], coords[1])

        # found - fill & update game
        self.update_game(coords)
        self.board.canvas.itemconfig(cell, fill=self.chosen_player.color)
        self.board.canvas.update_idletasks()

        # before switching turns - check for winner
        if self.got_winner(self.chosen_player.selected_cells):
            self.show_game_result(self.chosen_player)
            self.restart()
            return

        # No winner yet, but no available fills = TIE
        if self.board.available_cells == 0:
            self.show_game_result(None)
            self.restart()
            return

        # switching turns
        self.chosen_player = self.next_player()
        return

    # invoked by mouse clicking
    def callback(self, event):
        # if cell is already taken, try something else
        if self.board.canvas.itemcget(CURRENT, 'fill') != self.board.color:
            print("No Can Do, Try Other Step")
            return

        # fill the cell with player's color
        if self.board.canvas.find_withtag(CURRENT):
            self.board.canvas.itemconfig(CURRENT, fill=self.chosen_player.color)
            self.board.canvas.update_idletasks()
            coords = self.board.canvas.coords(CURRENT)
            self.update_game(coords)

        # before switching turns - check for winner
        if self.got_winner(self.chosen_player.selected_cells):
            self.show_game_result(self.chosen_player)
            self.restart()

        # No winner yet, but no available fills = TIE
        if self.board.available_cells == 0:
            self.show_game_result(None)
            self.restart()

        # NO winner yet, switch turn to the other player
        self.chosen_player = self.next_player()
        if self.chosen_player.name == "Computer":
            self.board.canvas.after(100,self.computer_play)

    def update_game(self, coords):
        # dec num of empty cells
        self.board.available_cells = self.board.available_cells - 1

        # add cell to player's selected cells set
        actual_cell = [key for key, value in self.board.dict_cells.items() if value == coords]
        self.chosen_player.selected_cells.update(actual_cell)

    def next_player(self):
        curr_index = self.players.index(self.chosen_player)
        return self.players[(curr_index +1) % len(self.players)]

    def got_winner(self, selected_cells):
        if len(selected_cells) < 3:
            return False
        win_comb = self.board.winning_combinations
        for select_comb in permutations(selected_cells, 3):
            for win in win_comb:
                if set(select_comb) == win:
                    return True

    @staticmethod
    def show_game_result(winner):
        if winner is not None:
            messagebox.showinfo("GOT WINNER (:", "The Winner is: {}".format(winner.name), icon="info")
        else:
            messagebox.showinfo("GOT TIE", icon="info")


def main():
    root = Tk()
    root.title("Tic Tac Toe")
    TicTacToe(root)
    root.mainloop()


if __name__ == '__main__':
    main()