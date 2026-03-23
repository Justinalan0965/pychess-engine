import helper
import finder

class Rules:
    def __init__(self, chess):
        self.chess = chess
        self.helper = helper.Helper()
        self.finder = finder.Finder(self.chess)

    def is_valid_move(self, piece, new_pos):        
        if piece.get_symbol() == '•' or piece is None:
            return False
        piece_type = piece.name.upper()
        if piece_type == 'PAWN':
            return self.is_valid_pawn_move(piece, new_pos)
        if piece_type == 'KNIGHT':
            return self.is_valid_knight_move(piece, new_pos)
        if piece_type == 'ROOK':
            return self.is_valid_rook_move(piece, new_pos)
        if piece_type == 'BISHOP':
            return self.is_valid_bishop_move(piece, new_pos)
        if piece_type == 'QUEEN':
            return self.is_valid_queen_move(piece, new_pos)
        if piece_type == 'KING':
            return self.is_valid_king_move(piece, new_pos)
        return False
    
    def is_valid_pawn_move(self, piece, new_pos):
        direction = 1 if piece.isWhite else -1
        start_row = 1 if piece.isWhite else 6

        crnt_row, crnt_col = self.helper.get_crnt_pos(piece)
        new_row, new_col = new_pos

        same_color = self.chess.is_same_color((crnt_row, crnt_col), (new_row, new_col))
        if crnt_col == new_col:
            if new_row == crnt_row + direction and self.chess.board[new_row][new_col].symbol == "•":
                return True
            if crnt_row == start_row and new_row == crnt_row + 2 * direction and self.chess.board[crnt_row + direction][new_col].symbol == "•" and self.chess.board[new_row][new_col].symbol == "•":
                return True
        elif abs(crnt_col - new_col) == 1 and new_row == crnt_row + direction and self.chess.board[new_row][new_col].symbol != "•" and not same_color:
            return True
        return False

    def is_valid_knight_move(self, piece, new_pos):
        crnt_row, crnt_col = self.helper.get_crnt_pos(piece)
        new_row, new_col = new_pos

        same_color = self.chess.is_same_color((crnt_row, crnt_col), (new_row, new_col))
        if (abs(crnt_row - new_row) == 2 and abs(crnt_col - new_col) == 1) or (abs(crnt_row - new_row) == 1 and abs(crnt_col - new_col) == 2):
            if self.chess.board[new_row][new_col].symbol == "•" or not same_color:
                return True
        return False
    
    def is_valid_rook_move(self, piece, new_pos):
        crnt_row, crnt_col = self.helper.get_crnt_pos(piece)
        new_row, new_col = new_pos

        same_color = self.chess.is_same_color((crnt_row, crnt_col), (new_row, new_col))
        if crnt_row == new_row or crnt_col == new_col:
            if self.chess.board[new_row][new_col].symbol == "•" or not same_color:
                return True
        return False
    
    def is_valid_bishop_move(self, piece, new_pos):
        crnt_row, crnt_col = self.helper.get_crnt_pos(piece)
        new_row, new_col = new_pos

        same_color = self.chess.is_same_color((crnt_row, crnt_col), (new_row, new_col))
        if abs(crnt_row - new_row) == abs(crnt_col - new_col):
            if self.chess.board[new_row][new_col].symbol == "•" or not same_color:
                return True
        return False
    
    def is_valid_queen_move(self, piece, new_pos):
        return self.is_valid_rook_move(piece, new_pos) or self.is_valid_bishop_move(piece, new_pos)

    def is_valid_king_move(self, piece, new_pos):
        crnt_row, crnt_col = self.helper.get_crnt_pos(piece)
        new_row, new_col = new_pos

        same_color = self.chess.is_same_color((crnt_row, crnt_col), (new_row, new_col))
        if abs(crnt_row - new_row) <= 1 and abs(crnt_col - new_col) <= 1:
            if self.chess.board[new_row][new_col].symbol == "•" or not same_color:
                return True
        return False

    def is_piece_in_path(self, piece, new_pos):
        crnt_row, crnt_col = self.helper.get_crnt_pos(piece)
        new_row, new_col = new_pos

        if crnt_row == new_row:
            step = 1 if new_col > crnt_col else -1
            for col in range(crnt_col + step, new_col, step):
                if self.chess.board[crnt_row][col].symbol != "•":
                    return True
        elif crnt_col == new_col:
            step = 1 if new_row > crnt_row else -1
            for row in range(crnt_row + step, new_row, step):
                if self.chess.board[row][crnt_col].symbol != "•":
                    return True
        elif abs(crnt_row - new_row) == abs(crnt_col - new_col):
            row_step = 1 if new_row > crnt_row else -1
            col_step = 1 if new_col > crnt_col else -1
            for i in range(1, abs(crnt_row - new_row)):
                if self.chess.board[crnt_row + i * row_step][crnt_col + i * col_step].symbol != "•":
                    return True
        return False
    
    def is_king_in_check(self, isWhiteMove):
        # If an opponent's piece can move to the king's position, then the king is in check
        pieces = ['rook', 'knight', 'bishop', 'queen', 'pawn']

        king = self.finder.find_piece('king', isWhiteMove)
        king_pos = self.helper.get_crnt_pos(king)

        for piece_name in pieces:
            piece = self.finder.find_piece(piece_name, not isWhiteMove)
            if self.is_valid_move(piece, king_pos) and not self.is_piece_in_path(piece, king_pos):
                return True
        return False