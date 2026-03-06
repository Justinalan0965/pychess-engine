import Rules

class Chess:
    def __init__(self):
        self.board = self.create_board()
        self.isWhiteMove = True
        self.position_map = {
            'a': 0, 
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
            'h': 7
            }
        self.move_history = {
            "white": [],
            "black": []
        }
        self.rules = Rules.Rules(self)

    def create_board(self):
        board = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(' ')
            board.append(row)
        return board
    
    def arrage_pieces(self):
        self.board[0][0] = 'W-Rook'
        self.board[0][1] = 'W-Knight'
        self.board[0][2] = 'W-Bishop' 
        self.board[0][3] = 'W-Queen'
        self.board[0][4] = 'W-King'
        self.board[0][5] = 'W-Bishop'
        self.board[0][6] = 'W-Knight'
        self.board[0][7] = 'W-Rook'
        for i in range(8):
            self.board[1][i] = 'W-Pawn'

        for i in range(8):
            self.board[6][i] = 'B-Pawn'
        self.board[7][0] = 'B-Rook'
        self.board[7][1] = 'B-Knight'
        self.board[7][2] = 'B-Bishop'
        self.board[7][3] = 'B-Queen'
        self.board[7][4] = 'B-King'
        self.board[7][5] = 'B-Bishop'
        self.board[7][6] = 'B-Knight'
        self.board[7][7] = 'B-Rook'

    def move(self, crnt_pos, new_pos):
        row_from = int(crnt_pos[1]) - 1
        col_from = self.position_map[crnt_pos[0]]
        piece = self.board[row_from][col_from]
        
        if (self.isWhiteMove and piece.startswith('W')) or (not self.isWhiteMove and piece.startswith('B')):
            if self.rules.is_valid_move(crnt_pos, new_pos, piece) and not self.rules.is_piece_in_path(crnt_pos, new_pos):
                row_to = int(new_pos[1]) - 1
                col_to = self.position_map[new_pos[0]]
                self.board[row_to][col_to] = piece
                self.board[row_from][col_from] = ' '
                self.isWhiteMove = not self.isWhiteMove
                self.move_history["white" if not self.isWhiteMove else "black"].append((crnt_pos, new_pos))
            else:
                print("Invalid move. Pls enter correct new position.")
        else:
            print(f"Invalid move. It's {'White' if self.isWhiteMove else 'Black'}'s turn.")
            

    def display_board(self):
        num_pos = [str(i+1) for i in range(8)]
        alpbt_pos = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        largest_piece_length = max(len(piece) for row in self.board for piece in row)
        
        board_to_display = [row[:] for row in self.board]
        
        # Rotate board 180 degrees for black's perspective
        if not self.isWhiteMove:
            board_to_display = board_to_display[::-1]
            # alpbt_pos = alpbt_pos[::-1]
            num_pos = num_pos[::-1]

        for i in range(7, -1, -1):
            print(num_pos[i], end=' ')
            for j in range(8):
                piece = board_to_display[i][j]
                print(piece.ljust(largest_piece_length), end=' ')   
            print()

        print("  ", end="")
        for letter in alpbt_pos:
            print(letter.ljust(largest_piece_length), end=" ")
        print()

        
if __name__ == "__main__":
    chess = Chess()
    chess.arrage_pieces()
    chess.display_board()

    try:
        while True:
            move = input("Enter your move (e.g., e2 e4) or press Ctrl+C to exit: ")
            start, end = move.split()
            chess.move(start, end)
            chess.display_board()
    except KeyboardInterrupt:
        print("\nGame exited.")


