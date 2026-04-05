import piece

class Helper:

    def create_and_get_piece(self, name=None, isWhite=None, row=None, col=None):
        return piece.Piece(name, isWhite, row, col)
    
    def get_crnt_pos(self, piece):
        return piece.crnt_row, piece.crnt_col
    
    def get_algebraic_pos(self, row, col):
        # print(f"Converting indices ({row}, {col}) to algebraic notation as {chr(col + ord('a')) + str(row + 1)}")
        return chr(col + ord('a')) + str(row + 1)
    
    def convert_algebraic_to_indices(self, pos):
        if len(pos) != 2:
            raise ValueError("Invalid Input. Must be in the format 'e4'.")
        
        col = ord(pos[0]) - ord('a')
        row = int(pos[1]) - 1
        # print(f"Converted {pos} to indices: ({row}, {col})")
        return row, col
    
    def EmptySquare(self):
        return self.create_and_get_piece()
    
    def validate_algebraic_notation(self, pos):
        if len(pos) != 2:
            return False
        col, row = pos[0], pos[1]
        if col < 'a' or col > 'h' or row < '1' or row > '8':
            return False
        return True