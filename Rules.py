class Rules:
    def __init__(self, chess):
        self.chess = chess
    
    def is_valid_move(self, crnt_pos, new_pos, piece):
        if piece == '.':
            return False
        piece_type = piece.upper()
        if piece_type == 'P':
            return self.is_valid_pawn_move(crnt_pos, new_pos, piece)
        if piece_type == 'N':
            return self.is_valid_knight_move(crnt_pos, new_pos, piece)
        if piece_type == 'R':
            return self.is_valid_rook_move(crnt_pos, new_pos, piece)
        if piece_type == 'B':
            return self.is_valid_bishop_move(crnt_pos, new_pos, piece)
        if piece_type == 'Q':
            return self.is_valid_queen_move(crnt_pos, new_pos, piece)
        if piece_type == 'K':
            return self.is_valid_king_move(crnt_pos, new_pos, piece)
        return False
    
    def is_valid_pawn_move(self, crnt_pos, new_pos, piece):
        direction = 1 if piece.isupper() else -1
        start_row = 1 if piece.isupper() else 6
        crnt_row = int(crnt_pos[1]) - 1
        crnt_col = self.chess.position_map[crnt_pos[0]]
        new_row = int(new_pos[1]) - 1
        new_col = self.chess.position_map[new_pos[0]]

        same_color = self.chess.are_same_color((crnt_row, crnt_col), (new_row, new_col))
        if crnt_col == new_col:
            if new_row == crnt_row + direction and self.chess.board[new_row][new_col] == '·':
                return True
            if crnt_row == start_row and new_row == crnt_row + 2 * direction and self.chess.board[crnt_row + direction][new_col] == '·' and self.chess.board[new_row][new_col] == '·':
                return True
        elif abs(crnt_col - new_col) == 1 and new_row == crnt_row + direction and self.chess.board[new_row][new_col] != '·' and not same_color:
            return True
        return False

    def is_valid_knight_move(self, crnt_pos, new_pos, piece):
        crnt_row = int(crnt_pos[1]) - 1
        crnt_col = self.chess.position_map[crnt_pos[0]]
        new_row = int(new_pos[1]) - 1
        new_col = self.chess.position_map[new_pos[0]]

        same_color = self.chess.are_same_color((crnt_row, crnt_col), (new_row, new_col))
        if (abs(crnt_row - new_row) == 2 and abs(crnt_col - new_col) == 1) or (abs(crnt_row - new_row) == 1 and abs(crnt_col - new_col) == 2):
            if self.chess.board[new_row][new_col] == '·' or not same_color:
                return True
        return False
    
    def is_valid_rook_move(self, crnt_pos, new_pos, piece):
        crnt_row = int(crnt_pos[1]) - 1
        crnt_col = self.chess.position_map[crnt_pos[0]]
        new_row = int(new_pos[1]) - 1
        new_col = self.chess.position_map[new_pos[0]]

        same_color = self.chess.are_same_color((crnt_row, crnt_col), (new_row, new_col))
        if crnt_row == new_row or crnt_col == new_col:
            if self.chess.board[new_row][new_col] == '·' or not same_color:
                return True
        return False
    
    def is_valid_bishop_move(self,crnt_pos, new_pos, piece):
        crnt_row = int(crnt_pos[1]) - 1
        crnt_col = self.chess.position_map[crnt_pos[0]]
        new_row = int(new_pos[1]) - 1
        new_col = self.chess.position_map[new_pos[0]]

        same_color = self.chess.are_same_color((crnt_row, crnt_col), (new_row, new_col))

        if abs(crnt_row - new_row) == abs(crnt_col - new_col):
            if self.chess.board[new_row][new_col] == '·' or not same_color:
                return True
        return False
    
    def is_valid_queen_move(self, crnt_pos, new_pos, piece):
        return self.is_valid_rook_move(crnt_pos, new_pos, piece) or self.is_valid_bishop_move(crnt_pos, new_pos, piece)

    def is_valid_king_move(self, crnt_pos, new_pos, piece):
        crnt_row = int(crnt_pos[1]) - 1
        crnt_col = self.chess.position_map[crnt_pos[0]]
        new_row = int(new_pos[1]) - 1
        new_col = self.chess.position_map[new_pos[0]]

        same_color = self.chess.are_same_color((crnt_row, crnt_col), (new_row, new_col))
        if abs(crnt_row - new_row) <= 1 and abs(crnt_col - new_col) <= 1:
            if self.chess.board[new_row][new_col] == '·' or not same_color:
                return True
        return False

    def is_piece_in_path(self, crnt_pos, new_pos):
        crnt_row = int(crnt_pos[1]) - 1
        crnt_col = self.chess.position_map[crnt_pos[0]]
        new_row = int(new_pos[1]) - 1
        new_col = self.chess.position_map[new_pos[0]]
        if crnt_row == new_row:
            step = 1 if new_col > crnt_col else -1
            for col in range(crnt_col + step, new_col, step):
                if self.chess.board[crnt_row][col] != self.chess.chess_pieces['.']:
                    return True
        elif crnt_col == new_col:
            step = 1 if new_row > crnt_row else -1
            for row in range(crnt_row + step, new_row, step):
                if self.chess.board[row][crnt_col] != self.chess.chess_pieces['.']:
                    return True
        elif abs(crnt_row - new_row) == abs(crnt_col - new_col):
            row_step = 1 if new_row > crnt_row else -1
            col_step = 1 if new_col > crnt_col else -1
            for i in range(1, abs(crnt_row - new_row)):
                if self.chess.board[crnt_row + i * row_step][crnt_col + i * col_step] != self.chess.chess_pieces['.']:
                    return True
        return False
    
    def is_king_in_check(self, isWhiteMove):
        # If an opponent's piece can move to the king's position, then the king is in check
        pieces = ['r', 'n', 'b', 'q', 'p'] if isWhiteMove else ['R', 'N', 'B', 'Q', 'P']

        k_row, k_col = self.chess.get_crnt_pos('k', 'w' ) if isWhiteMove else self.chess.get_crnt_pos('k', 'b')
        king_pos = self.chess.get_position_in_alpbt(k_col) + str(k_row + 1)

        for piece in pieces:
            piece_row, piece_col = self.chess.get_crnt_pos(piece, 'b' ) if isWhiteMove else self.chess.get_crnt_pos(piece, 'w')
            piece_pos = self.chess.get_position_in_alpbt(piece_col) + str(piece_row + 1)

            if self.is_valid_move(piece_pos, king_pos, piece) and not self.is_piece_in_path(piece_pos, king_pos):
                return True
        
        return False