class Player:
    """
    Player class to be used in the Game obj

    Attributes:
    name: text to distinguish name of player ie player1, player2, computer
    color: hex code to color each player cell on click event
    selected cells: set data structure to keep track of player cells

    """

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.selected_cells = set()