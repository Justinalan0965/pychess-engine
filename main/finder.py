import helper

class Finder:
    def __init__(self, chess):
        self.chess = chess
        self.helper = helper.Helper()

    def get_available_moves(self, piece):
        # find all legal moves for the given piece
        # Will go with Brute Force for now, will optimize later

        crn_pos = self.helper.get_crnt_pos(piece)
        available_moves = []
        
        for i in range(8):
            for j in range(8):
                new_pos = (i, j)
                if self.chess.rules.is_valid_move(piece, new_pos) and not self.chess.rules.is_piece_in_path(piece, new_pos) and (self.chess.board[new_pos[0]][new_pos[1]].is_empty() or not self.chess.is_same_color(crn_pos, new_pos)):
                    available_moves.append(new_pos)
        return available_moves


    def find_piece(self, piece_name, isWhite):
        # find the position of a piece given its name and color
        # Will go with Brute Force for now, will optimize later
        for i in range(len(self.chess.board)):
            for j in range(len(self.chess.board[i])):
                piece = self.chess.board[i][j]
                if piece.is_empty():
                    continue
                if piece.name == piece_name and piece.isWhite == isWhite:
                    return piece
        return None 
    
    
    
