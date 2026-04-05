class Piece:
    class Symbols:
        black = {
            'king': '♔',
            'queen': '♕',
            'rook': '♖',
            'bishop': '♗',
            'knight': '♘',
            'pawn': '♙'
        }
        white = {
            'king': '♚',
            'queen': '♛',
            'rook': '♜',
            'bishop': '♝',
            'knight': '♞',
            'pawn': '♟'
        }

    def __init__(self, name, isWhite, crnt_row=None, crnt_col=None):
        self.isWhite = isWhite
        self.name = name
        self.symbol = self.get_symbol()
        self.crnt_col, self.crnt_row = crnt_col, crnt_row
        
    def get_symbol(self):
        if self.name is None:
            return None
        
        if self.isWhite:
            return self.Symbols.white[self.name]
        else:
            return self.Symbols.black[self.name]
        
    def is_empty(self):
        return self.name is None

    def __str__(self):
        return self.symbol