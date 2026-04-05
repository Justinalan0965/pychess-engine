from rich import print
import helper
import rules
import finder


class Chess:
    def __init__(self):
        self.rules = rules.Rules(self)
        self.helper = helper.Helper()
        self.finder = finder.Finder(self)

        self.board = []

        self.isWhiteMove = True
        self.last_check_point = None

        self.white_captured_pieces = []
        self.black_captured_pieces = []

        self.move_history = {
            "white": [],
            "black": []
        }

    def create_board(self):
        for i in range(8):
            row = []
            for j in range(8):
                row.append(self.helper.EmptySquare())
            self.board.append(row)
        return self.board

    def arrage_pieces(self):
        # White pieces
        self.board[0][0] = self.helper.create_and_get_piece(
            'rook', True, 0, 0)
        self.board[0][1] = self.helper.create_and_get_piece(
            'knight', True, 0, 1)
        self.board[0][2] = self.helper.create_and_get_piece(
            'bishop', True, 0, 2)
        self.board[0][3] = self.helper.create_and_get_piece(
            'queen', True, 0, 3)
        self.board[0][4] = self.helper.create_and_get_piece(
            'king', True, 0, 4)
        self.board[0][5] = self.helper.create_and_get_piece(
            'bishop', True, 0, 5)
        self.board[0][6] = self.helper.create_and_get_piece(
            'knight', True, 0, 6)
        self.board[0][7] = self.helper.create_and_get_piece(
            'rook', True, 0, 7)
        for i in range(8):
            self.board[1][i] = self.helper.create_and_get_piece(
                'pawn', True, 1, i)

        # Black pieces
        self.board[7][0] = self.helper.create_and_get_piece(
            'rook', False, 7, 0)
        self.board[7][1] = self.helper.create_and_get_piece(
            'knight', False, 7, 1)
        self.board[7][2] = self.helper.create_and_get_piece(
            'bishop', False, 7, 2)
        self.board[7][3] = self.helper.create_and_get_piece(
            'queen', False, 7, 3)
        self.board[7][4] = self.helper.create_and_get_piece(
            'king', False, 7, 4)
        self.board[7][5] = self.helper.create_and_get_piece(
            'bishop', False, 7, 5)
        self.board[7][6] = self.helper.create_and_get_piece(
            'knight', False, 7, 6)
        self.board[7][7] = self.helper.create_and_get_piece(
            'rook', False, 7, 7)
        for i in range(8):
            self.board[6][i] = self.helper.create_and_get_piece(
                'pawn', False, 6, i)

    def move(self, piece, new_pos):
        row_from, col_from = self.helper.get_crnt_pos(piece)
        self.last_check_point = [row[:] for row in self.board]

        if (self.isWhiteMove and piece.isWhite) or (not self.isWhiteMove and not piece.isWhite):

            row_to, col_to = self.helper.convert_algebraic_to_indices(new_pos)

            # Update captured pieces if there's a piece at the destination
            if not self.board[row_to][col_to].is_empty():
                captured_piece = self.board[row_to][col_to]
                if captured_piece.isWhite:
                    self.black_captured_pieces.append(captured_piece)
                else:
                    self.white_captured_pieces.append(captured_piece)

            # Update piece position
            piece.crnt_row = row_to
            piece.crnt_col = col_to

            # Move the piece on the board
            self.board[row_to][col_to] = piece

            # Empty piece
            self.board[row_from][col_from] = self.helper.EmptySquare()


            # Check for check or checkmate
            if (self.rules.is_checkmate(not self.isWhiteMove)):
                print(f"[red]Checkmate! [blue]{'White' if self.isWhiteMove else 'Black'}[red] wins!")
                exit()
            
            elif (self.rules.is_king_in_check(self.isWhiteMove)):
                print(f"[yellow]You can't make that move! [blue]{'White' if self.isWhiteMove else 'Black'}[yellow] king is in check!")
                # Undo the move
                self.board = [row[:] for row in self.last_check_point]
                if not self.isWhiteMove:
                    self.white_captured_pieces.pop() if self.white_captured_pieces else None
                else:
                    self.black_captured_pieces.pop() if self.black_captured_pieces else None    
                return
            
            elif self.rules.is_king_in_check(not self.isWhiteMove):
                print(f"[yellow]Check! [blue]{'Black' if self.isWhiteMove else 'White'}[yellow] king is in check!") 
            
            # Toggle turn
            self.isWhiteMove = not self.isWhiteMove

            # Update move history
            FROM = self.helper.get_algebraic_pos(row_from, col_from)
            TO = self.helper.get_algebraic_pos(row_to, col_to)
            self.move_history["white" if not self.isWhiteMove else "black"].append((FROM, TO))

        else:
            print(f"[red]Invalid move. It's [blue]{'White' if self.isWhiteMove else 'Black'}[red]'s turn.")

    def render_board(self):
        num_pos = [str(i+1) for i in range(8)]
        alpbt_pos = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Determine max symbol width
        largest_piece_length = max(len(piece.symbol) if not piece.is_empty() else 0 for row in self.board for piece in row)

        # Make cells bigger (minimum width)
        cell_width = max(5, largest_piece_length + 2)

        board_to_display = [row[:] for row in self.board]

        if not self.isWhiteMove:
            board_to_display.reverse()
            num_pos = ['8', '7', '6', '5', '4', '3', '2', '1']
        else:
            num_pos = ['1', '2', '3', '4', '5', '6', '7', '8']

        # Horizontal separator
        def print_separator():
            print("   +" + "+".join(["-" * cell_width for _ in range(8)]) + "+")

        # Print column letters (aligned)
        print("    ", end="")
        for letter in alpbt_pos:
            print(f"[blue]{letter.center(cell_width)}[/blue]", end=" ")
        print()

        print_separator()

        for i in range(7, -1, -1):
            print(f"{num_pos[i]}  |", end="")

            for j in range(8):
                piece = board_to_display[i][j]
                symbol = piece.symbol if not piece.is_empty() else " "
                print(symbol.center(cell_width), end="|")

            print()
            print_separator()
        
        print(f"\n[green]Captured By White: [blue]{self.format_captured(self.white_captured_pieces)}[/blue]")
        print(f"[green]Captured By Black: [blue]{self.format_captured(self.black_captured_pieces)}[/blue]")

    def format_captured(self, pieces):
        return " ".join(p.symbol for p in pieces) if pieces else "None"


    def get_crnt_pos(self, piece, color):
        color = color.lower()
        if color == "white" or color == "w":
            piece = piece.upper()

        piece_symbol = self.helper.get_crnt_pos(piece, color == "white").symbol
        for i in range(len(self.board)):
            row = self.board[i]
            for j in range(len(row)):
                square = row[j]
                if square == piece_symbol:
                    return (i, j)

    def is_same_color(self, pos1, pos2):
        piece1 = self.board[pos1[0]][pos1[1]]
        piece2 = self.board[pos2[0]][pos2[1]]
        if piece1.is_empty() or piece2.is_empty():
            return False
        return piece1.isWhite == piece2.isWhite

    def get_piece_at_position(self, pos):
        return self.board[pos[0]][pos[1]]


if __name__ == "__main__":
    chess = Chess()
    chess.create_board()
    chess.arrage_pieces()
    chess.render_board()

    try:
        while True:
            print("[green]Select a piece (e.g., e2): ", end="")
            selected_piece = input().strip().lower()

            valid_input = chess.helper.validate_algebraic_notation(selected_piece)
            if not valid_input:
                print("[red]Invalid input. Please enter a valid position in algebraic notation (e.g., e2).")
                continue

            crnt_pos = chess.helper.convert_algebraic_to_indices(selected_piece)

            piece = chess.board[crnt_pos[0]][crnt_pos[1]]
            available_moves = chess.finder.get_available_moves(piece)

            if not available_moves:
                print("[red]No available moves for the selected piece. Please select another piece.")
                continue

            print("[green]Available moves for the selected piece [{} ]:".format(piece.symbol))
            print(f"[blue] {[chess.helper.get_algebraic_pos(move[0], move[1]) for move in available_moves]}")

            print("[green]Select a move: ", end="")
            move_to = input().strip().lower()

            selected_pos = chess.helper.convert_algebraic_to_indices(move_to)
            if selected_pos not in available_moves:
                print("[red]Invalid move. Please select a valid move.")
                continue

            chess.move(piece, move_to)
            chess.render_board()
    except KeyboardInterrupt:
        print("\nGame exited.")
