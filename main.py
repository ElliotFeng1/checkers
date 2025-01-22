import random

class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king

    def make_king(self):
        self.king = True

    def __repr__(self):
        if self.king:
            return 'K' if self.color == 'white' else 'k'
        return 'O' if self.color == 'white' else 'X'


class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = []
        for row in range(8):
            board.append([])
            for col in range(8):
                if (row + col) % 2 != 0:
                    if row < 3:
                        board[row].append(Piece('red'))
                    elif row > 4:
                        board[row].append(Piece('white'))
                    else:
                        board[row].append(None)
                else:
                    board[row].append(None)
        return board

    def print_board(self):
        print("  " + " ".join(map(str, range(8))))
        for idx, row in enumerate(self.board):
            print(idx, ' '.join([str(piece) if piece else '.' for piece in row]))

    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        self.board[to_row][to_col] = piece

        if to_row == 0 or to_row == 7:
            piece.make_king()

    def get_piece(self, row, col):
        return self.board[row][col]

    def remove_piece(self, row, col):
        self.board[row][col] = None

    def winner(self):
        red_left = white_left = 0
        for row in self.board:
            for piece in row:
                if piece:
                    if piece.color == 'red':
                        red_left += 1
                    else:
                        white_left += 1
        if red_left == 0:
            return 'White'
        elif white_left == 0:
            return 'Red'
        return None


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'red'

    def switch_turn(self):
        self.turn = 'white' if self.turn == 'red' else 'red'

    def get_valid_moves(self, piece, row, col):
        moves = []
        capture_moves = []
        directions = [(-1, -1), (-1, 1)] if piece.color == 'white' else [(1, -1), (1, 1)]
        if piece.king:
            directions.extend([(-d[0], -d[1]) for d in directions])

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if self.board.get_piece(r, c) is None:
                    moves.append((r, c))
                elif self.board.get_piece(r, c).color != piece.color:
                    jump_r, jump_c = r + dr, c + dc
                    if 0 <= jump_r < 8 and 0 <= jump_c < 8 and self.board.get_piece(jump_r, jump_c) is None:
                        capture_moves.append((jump_r, jump_c))

        return capture_moves if capture_moves else moves

    def suggest_move(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == self.turn:
                    valid_moves = self.get_valid_moves(piece, row, col)
                    if valid_moves:
                        print(f"Hint: Move piece at {row}{col} to {valid_moves[0][0]}{valid_moves[0][1]}")
                        return

    def random_computer_move(self):
        all_moves = []
        capture_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == self.turn:
                    valid_moves = self.get_valid_moves(piece, row, col)
                    for move in valid_moves:
                        if abs(move[0] - row) == 2:
                            capture_moves.append((piece, row, col, move[0], move[1]))
                        else:
                            all_moves.append((piece, row, col, move[0], move[1]))

        if capture_moves:
            piece, from_row, from_col, to_row, to_col = random.choice(capture_moves)
        else:
            piece, from_row, from_col, to_row, to_col = random.choice(all_moves)

        self.board.move_piece(from_row, from_col, to_row, to_col)
        if abs(to_row - from_row) == 2:
            self.board.remove_piece((from_row + to_row) // 2, (from_col + to_col) // 2)

    def play(self):
        while True:
            self.board.print_board()
            print(f"{self.turn.capitalize()}'s turn")

            if self.turn == 'red':
                self.suggest_move()
                from_to = input("Enter the move (from_row from_col to_row to_col): ").strip()
                from_row, from_col, to_row, to_col = int(from_to[0]), int(from_to[1]), int(from_to[2]), int(from_to[3])

                piece = self.board.get_piece(from_row, from_col)
                valid_moves = self.get_valid_moves(piece, from_row, from_col)
                if piece and piece.color == self.turn and (to_row, to_col) in valid_moves:
                    self.board.move_piece(from_row, from_col, to_row, to_col)
                    if abs(to_row - from_row) == 2:
                        self.board.remove_piece((from_row + to_row) // 2, (from_col + to_col) // 2)
                else:
                    print("Invalid move. Try again.")
                    continue
            else:
                self.random_computer_move()

            self.switch_turn()

            winner = self.board.winner()
            if winner:
                self.board.print_board()
                print(f"{winner} wins!")
                break


if __name__ == "__main__":
    game = Game()
    game.play()