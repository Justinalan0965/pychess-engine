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
        if piece_type == '':
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
        if crnt_col == new_col:
            if new_row == crnt_row + direction and self.chess.board[new_row][new_col] == '·':
                return True
            if crnt_row == start_row and new_row == crnt_row + 2 * direction and self.chess.board[crnt_row + direction][new_col] == '·' and self.chess.board[new_row][new_col] == '·':
                return True
        elif abs(crnt_col - new_col) == 1 and new_row == crnt_row + direction and self.chess.board[new_row][new_col] != '·' and not self.chess.board[new_row][new_col].startswith(piece[0]):
            return True
        return False

    def is_valid_knight_move(self, crnt_pos, new_pos, piece):
        crnt_row = int(crnt_pos[1]) - 1
        crnt_col = self.chess.position_map[crnt_pos[0]]
        new_row = int(new_pos[1]) - 1
        new_col = self.chess.position_map[new_pos[0]]
        if (abs(crnt_row - new_row) == 2 and abs(crnt_col - new_col) == 1) or (abs(crnt_row - new_row) == 1 and abs(crnt_col - new_col) == 2):
            if self.chess.board[new_row][new_col] == '·' or not self.chess.board[new_row][new_col].startswith(piece[0]):
                return True
        return False
    
    def is_valid_rook_move(self, crnt_pos, new_pos, piece):
        crnt_row = int(crnt_pos[1]) - 1
        crnt_col = self.chess.position_map[crnt_pos[0]]
        new_row = int(new_pos[1]) - 1
        new_col = self.chess.position_map[new_pos[0]]
        if crnt_row == new_row or crnt_col == new_col:
            if self.chess.board[new_row][new_col] == '·' or not self.chess.board[new_row][new_col].startswith(piece[0]):
                return True
        return False
    
    def is_valid_bishop_move(self,crnt_pos, new_pos, piece):
        crnt_row = int(crnt_pos[1]) - 1
        crnt_col = self.chess.position_map[crnt_pos[0]]
        new_row = int(new_pos[1]) - 1
        new_col = self.chess.position_map[new_pos[0]]
        if abs(crnt_row - new_row) == abs(crnt_col - new_col):
            if self.chess.board[new_row][new_col] == '·' or not self.chess.board[new_row][new_col].startswith(piece[0]):
                return True
        return False
    
    def is_valid_queen_move(self, crnt_pos, new_pos, piece):
        return self.is_valid_rook_move(crnt_pos, new_pos, piece) or self.is_valid_bishop_move(crnt_pos, new_pos, piece)

    def is_valid_king_move(self, crnt_pos, new_pos, piece):
        crnt_row = int(crnt_pos[1]) - 1
        crnt_col = self.chess.position_map[crnt_pos[0]]
        new_row = int(new_pos[1]) - 1
        new_col = self.chess.position_map[new_pos[0]]
        if abs(crnt_row - new_row) <= 1 and abs(crnt_col - new_col) <= 1:
            if self.chess.board[new_row][new_col] == '·' or not self.chess.board[new_row][new_col].startswith(piece[0]):
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
                if self.chess.board[crnt_row][col] != '·':
                    return True
        elif crnt_col == new_col:
            step = 1 if new_row > crnt_row else -1
            for row in range(crnt_row + step, new_row, step):
                if self.chess.board[row][crnt_col] != '·':
                    return True
        elif abs(crnt_row - new_row) == abs(crnt_col - new_col):
            row_step = 1 if new_row > crnt_row else -1
            col_step = 1 if new_col > crnt_col else -1
            for i in range(1, abs(crnt_row - new_row)):
                if self.chess.board[crnt_row + i * row_step][crnt_col + i * col_step] != '.':
                    return True
        return False