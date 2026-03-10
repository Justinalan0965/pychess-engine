# PyChess Engine

A simple command-line chess game implemented in Python, featuring basic chess rules, move validation, check detection, and rollback for illegal moves.

## Features

- **Board Representation**: 8x8 grid with Unicode chess pieces.
- **Move Validation**: Supports all standard piece movements (pawn, knight, bishop, rook, queen, king) with path clearance checks.
- **Check Detection**: Identifies when a king is in check and prevents moves that leave the king exposed.
- **Game Flow**: Alternates turns between White and Black, with move history tracking.
- **Error Handling**: Invalid moves are rejected with appropriate messages, and illegal moves (e.g., those putting the king in check) are rolled back.

## Requirements

- Python 3.6+

## Installation

Install dependencies with pip:
```
pip install -r requirements.txt
```

Or with uv:
```
uv pip install -r requirements.txt
```

## How to Run

1. Navigate to the project directory:
   ```
   cd path/to/pychess-engine
   ```

2. Run the game:
   ```
   python Chess_Basic.py
   ```

3. Enter moves in algebraic notation (e.g., `e2 e4`). Press Ctrl+C to exit.

## Project Structure

- `Chess_Basic.py`: Main game class handling board setup, move execution, display, and game loop.
- `Rules.py`: Contains logic for validating moves, checking paths, and detecting checks.
- `LICENSE`: MIT License.
- `README.md`: This file.

## Key Classes and Methods

### Chess Class (Chess_Basic.py)
- `__init__()`: Initializes the board, pieces, and game state.
- `create_board()`: Sets up an empty 8x8 board.
- `arrage_pieces()`: Places pieces in starting positions.
- `move(crnt_pos, new_pos)`: Validates and executes a move, checks for check, and rolls back if necessary.
- `display_board()`: Prints the current board state with coordinates.
- `are_same_color(pos1, pos2)`: Determines if two pieces are the same color.
- `get_piece_key(piece)`: Maps Unicode piece symbols to letter keys (e.g., ♕ → 'Q').

### Rules Class (Rules.py)
- `is_valid_move(crnt_pos, new_pos, piece)`: Checks if a move is legal for the piece type.
- `is_piece_in_path(crnt_pos, new_pos)`: Ensures the path between start and end is clear.
- `is_king_in_check(isWhiteMove)`: Scans for enemy pieces that can attack the king.
- Piece-specific validators: `is_valid_pawn_move()`, `is_valid_knight_move()`, etc.

## Contributing

Feel free to submit issues or pull requests for improvements, such as adding castling, en passant, or promotion.

## License

MIT License - see LICENSE file for details.
