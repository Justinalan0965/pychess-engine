import Rules
from rich import print

class Chess:
    def __init__(self):
        self.board = []
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

        self.chess_pieces = {
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',  # White
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',  # Black
            '.': '·'  # Empty square
        }

    def create_board(self):
        for i in range(8):
            row = []
            for j in range(8):
                row.append(self.chess_pieces['.'])
            self.board.append(row)
        return self.board
    
    def arrage_pieces(self):
        self.board[0][0] = self.chess_pieces['R']
        self.board[0][1] = self.chess_pieces['N']
        self.board[0][2] = self.chess_pieces['B']
        self.board[0][3] = self.chess_pieces['Q']
        self.board[0][4] = self.chess_pieces['K']
        self.board[0][5] = self.chess_pieces['B']
        self.board[0][6] = self.chess_pieces['N']
        self.board[0][7] = self.chess_pieces['R']
        for i in range(8):
            self.board[1][i] = self.chess_pieces['P']

        for i in range(8):
            self.board[6][i] = self.chess_pieces['p']
        self.board[7][0] = self.chess_pieces['r']
        self.board[7][1] = self.chess_pieces['n']
        self.board[7][2] = self.chess_pieces['b']
        self.board[7][3] = self.chess_pieces['q']
        self.board[7][4] = self.chess_pieces['k']
        self.board[7][5] = self.chess_pieces['b']
        self.board[7][6] = self.chess_pieces['n']
        self.board[7][7] = self.chess_pieces['r']

    def move(self, crnt_pos, new_pos):
        row_from = int(crnt_pos[1]) - 1
        col_from = self.position_map[crnt_pos[0]]
        piece = self.board[row_from][col_from]
        key = next((k for k, v in self.chess_pieces.items() if v == piece), None)
        
        if (self.isWhiteMove and key.isupper()) or (not self.isWhiteMove and key.islower()):
            if self.rules.is_valid_move(crnt_pos, new_pos, key) and not self.rules.is_piece_in_path(crnt_pos, new_pos):
                row_to = int(new_pos[1]) - 1
                col_to = self.position_map[new_pos[0]]
                self.board[row_to][col_to] = piece
                self.board[row_from][col_from] = ' '
                self.isWhiteMove = not self.isWhiteMove
                self.move_history["white" if not self.isWhiteMove else "black"].append((crnt_pos, new_pos))
            else:
                print("[red]Invalid move. Pls enter correct new position.")
        else:
            print(f"[red]Invalid move. It's [blue]{'White' if self.isWhiteMove else 'Black'}[red]'s turn.")
            

    def display_board(self):
        num_pos = [str(i+1) for i in range(8)]
        alpbt_pos = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        largest_piece_length = max(len(piece) for row in self.board for piece in row)
        
        board_to_display = [row[:] for row in self.board]
        
        # Rotate board 180 degrees for black's perspective
        if not self.isWhiteMove:
            board_to_display = board_to_display[::-1]
            num_pos = num_pos[::-1]

        for i in range(7, -1, -1):
            print("[blue]" + num_pos[i], end=' ')
            for j in range(8):
                piece = board_to_display[i][j]
                print(piece.ljust(largest_piece_length), end=' ')   
            print()

        print("  ", end="")
        for letter in alpbt_pos:
            print("[blue]" + letter.ljust(largest_piece_length), end=" ")
        print()

        
if __name__ == "__main__":
    chess = Chess()
    chess.create_board()
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


