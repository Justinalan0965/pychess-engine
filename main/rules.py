import helper
import finder

class Rules:
    def __init__(self, chess):
        self.chess = chess
        self.helper = helper.Helper()
        self.finder = finder.Finder(self.chess)

    def is_valid_move(self, piece, new_pos):        
        if piece is None or piece.is_empty():
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
            if new_row == crnt_row + direction and self.chess.board[new_row][new_col].is_empty():
                return True
            if crnt_row == start_row and new_row == crnt_row + 2 * direction and self.chess.board[crnt_row + direction][new_col].is_empty() and self.chess.board[new_row][new_col].is_empty():
                return True
        elif abs(crnt_col - new_col) == 1 and new_row == crnt_row + direction and not self.chess.board[new_row][new_col].is_empty() and not same_color:
            return True
        return False

    def is_valid_knight_move(self, piece, new_pos):
        crnt_row, crnt_col = self.helper.get_crnt_pos(piece)
        new_row, new_col = new_pos

        same_color = self.chess.is_same_color((crnt_row, crnt_col), (new_row, new_col))
        if (abs(crnt_row - new_row) == 2 and abs(crnt_col - new_col) == 1) or (abs(crnt_row - new_row) == 1 and abs(crnt_col - new_col) == 2):
            if self.chess.board[new_row][new_col].is_empty() or not same_color:
                return True
        return False
    
    def is_valid_rook_move(self, piece, new_pos):
        crnt_row, crnt_col = self.helper.get_crnt_pos(piece)
        new_row, new_col = new_pos

        same_color = self.chess.is_same_color((crnt_row, crnt_col), (new_row, new_col))
        if crnt_row == new_row or crnt_col == new_col:
            if self.chess.board[new_row][new_col].is_empty() or not same_color:
                return True
        return False
    
    def is_valid_bishop_move(self, piece, new_pos):
        crnt_row, crnt_col = self.helper.get_crnt_pos(piece)
        new_row, new_col = new_pos

        same_color = self.chess.is_same_color((crnt_row, crnt_col), (new_row, new_col))
        if abs(crnt_row - new_row) == abs(crnt_col - new_col):
            if self.chess.board[new_row][new_col].is_empty() or not same_color:
                return True
        return False
    
    def is_valid_queen_move(self, piece, new_pos):
        return self.is_valid_rook_move(piece, new_pos) or self.is_valid_bishop_move(piece, new_pos)

    def is_valid_king_move(self, piece, new_pos):
        crnt_row, crnt_col = self.helper.get_crnt_pos(piece)
        new_row, new_col = new_pos

        same_color = self.chess.is_same_color((crnt_row, crnt_col), (new_row, new_col))
        if abs(crnt_row - new_row) <= 1 and abs(crnt_col - new_col) <= 1:
            if self.chess.board[new_row][new_col].is_empty() or not same_color:
                return True
        return False

    def is_piece_in_path(self, piece, new_pos):
        crnt_row, crnt_col = self.helper.get_crnt_pos(piece)
        new_row, new_col = new_pos

        if crnt_row == new_row:
            step = 1 if new_col > crnt_col else -1
            for col in range(crnt_col + step, new_col, step):
                if not self.chess.board[crnt_row][col].is_empty():
                    return True
        elif crnt_col == new_col:
            step = 1 if new_row > crnt_row else -1
            for row in range(crnt_row + step, new_row, step):
                if not self.chess.board[row][crnt_col].is_empty():
                    return True
        elif abs(crnt_row - new_row) == abs(crnt_col - new_col):
            row_step = 1 if new_row > crnt_row else -1
            col_step = 1 if new_col > crnt_col else -1
            for i in range(1, abs(crnt_row - new_row)):
                if not self.chess.board[crnt_row + i * row_step][crnt_col + i * col_step].is_empty():
                    return True
        return False
    
    def is_king_in_check(self, isWhiteMove):
        # If an opponent's piece can move to the king's position, then the king is in check

        king = self.finder.find_piece('king', isWhiteMove)
        king_pos = self.helper.get_crnt_pos(king)

        # Check all opponent pieces on the board
        for i in range(8):
            for j in range(8):
                piece = self.chess.board[i][j]
                if not piece.is_empty() and piece.isWhite != isWhiteMove:  # Opponent piece
                    if self.is_valid_move(piece, king_pos) and not self.is_piece_in_path(piece, king_pos):
                        return True
        return False

    def is_checkmate(self, isWhiteMove):
        if not self.is_king_in_check(isWhiteMove):
            return False
  
        for i in range(8):
            for j in range(8):
                piece = self.chess.board[i][j]
                if not piece.is_empty() and piece.isWhite == isWhiteMove:
                    available_moves = self.finder.get_available_moves(piece)
                    for move in available_moves:

                        original_pos = self.helper.get_crnt_pos(piece)

                        # store the captured piece if there's any
                        captured_piece = self.chess.board[move[0]][move[1]]

                        # Simulate the move
                        self.chess.board[original_pos[0]][original_pos[1]] = self.helper.EmptySquare()
                        piece.crnt_row, piece.crnt_col = move
                        self.chess.board[move[0]][move[1]] = piece
    
                        # Check if the king is still in check after the move
                        if not self.is_king_in_check(isWhiteMove):
                            # Undo the move
                            self.chess.board[move[0]][move[1]] = self.helper.EmptySquare()
                            piece.crnt_row, piece.crnt_col = original_pos
                            self.chess.board[original_pos[0]][original_pos[1]] = piece
                            return False
    
                        # Undo the move
                        self.chess.board[original_pos[0]][original_pos[1]] = piece
                        piece.crnt_row, piece.crnt_col = original_pos
                        self.chess.board[move[0]][move[1]] = captured_piece

        return True
            