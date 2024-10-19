import pygame
from piece import Piece


class Board:
    """
    Class consisting of all elements required for a board in the game Checkers
    """

    ROWS, COLS = 8, 8
    SQUARE_SIZE = 600 // 8
    DARK = (150, 90, 20)
    LIGHT = (220, 160, 90)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

    def __init__(self):
        """
        Initializes the board with the game settings
        """
        self.board = []
        self.selected_piece = None
        self.jumped_piece = None
        self.valid_moves = []
        self.create_board()
        self.board_size = 8

    def create_board(self):
        """
        Creates the board with all the pieces
        """
        for row in range(self.ROWS):
            self.board.append([])
            for col in range(self.COLS):
                if row % 2 != col % 2:
                    if row < 3:
                        self.board[row].append(Piece(row, col, self.RED))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, self.BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw_squares(self, win):
        """
        Draws all the squares in the board
        """
        win.fill(self.DARK)
        for row in range(self.ROWS):
            for col in range(row % 2, self.COLS, 2):
                pygame.draw.rect(win, self.LIGHT, (col*self.SQUARE_SIZE, row*self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw(self, win):
        """
        Draws all the pieces in the board
        """
        self.draw_squares(win)
        for row in range(self.ROWS):
            for col in range(self.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
        if self.selected_piece:
            pygame.draw.circle(win, self.WHITE, (self.selected_piece.x, self.selected_piece.y), self.SQUARE_SIZE // 2, 4)
            for move in self.valid_moves:
                pygame.draw.circle(win, self.GREEN, (move[1] * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, move[0] * self.SQUARE_SIZE + self.SQUARE_SIZE // 2), self.SQUARE_SIZE // 4)

    def select(self, row, col, color):
        """
        Selects the piece from the board according to the given coordinates
        and updates valid moves according to the selected piece
        """
        piece = self.board[row][col]
        if piece != 0 and piece.color == color:
            self.selected_piece = piece
            if self.jumped_piece is None:
                self.valid_moves = self.get_valid_moves(row, col)
            else:
                self.valid_moves = self.get_valid_moves_after_jump(row, col)

    def select_and_move(self, row, col):
        """
        Checks whether a selected piece is valid
        and clears the selected piece if not valid
        """
        if self.selected_piece:
            result = self.move(self.selected_piece, row, col)
            if result and self.jumped_piece is None:
                self.selected_piece = None
                self.valid_moves = []

    def move(self, piece, row, col):
        """
        Moves the selected piece to the given coordinates
        """
        if (row, col) in self.valid_moves:
            if abs(piece.row - row) == 2 and abs(piece.col - col) == 2:
                mid_row = (piece.row + row) // 2
                mid_col = (piece.col + col) // 2
                self.jumped_piece = self.board[mid_row][mid_col]
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
            piece.move(row, col)
            self.valid_moves = []
            return True
        return False

    def get_valid_moves(self, row, col):
        """
        Returns a list of valid moves for the given coordinates
        """
        moves = []
        if self.board[row][col].color is self.BLACK and self.board[row][col].king is False:
            directions = [(-1, -1), (-1, 1)]
        elif self.board[row][col].color is self.RED and self.board[row][col].king is False:
            directions = [(1, -1), (1, 1)]
        else:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < self.ROWS and 0 <= new_col < self.COLS and self.board[new_row][new_col] == 0:
                moves.append((new_row, new_col))

        for drow, dcol in directions:
            jump_row, jump_col = row + 2 * drow, col + 2 * dcol
            mid_row, mid_col = row + drow, col + dcol
            piece = self.board[row][col]

            if self.is_valid_jump(piece, mid_row, mid_col, jump_row, jump_col):
                moves.append((jump_row, jump_col))
        return moves

    def is_valid_jump(self, piece, mid_row, mid_col, jump_row, jump_col):
        """
        Checks whether a jump is valid
        """
        if 0 <= jump_row < self.board_size and 0 <= jump_col < self.board_size:
            mid_piece = self.get_piece(mid_row, mid_col)
            landing_piece = self.get_piece(jump_row, jump_col)

            if mid_piece != 0 and mid_piece.color != piece.color and landing_piece == 0:
                return True
        return False

    def get_valid_moves_after_jump(self, row, col):
        """
        Returns all valid moves after a jump for given coordinates
        """
        moves = []

        if self.board[row][col].color is self.BLACK and self.board[row][col].king is False:
            directions = [(-1, -1), (-1, 1)]
        elif self.board[row][col].color is self.RED and self.board[row][col].king is False:
            directions = [(1, -1), (1, 1)]
        else:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for drow, dcol in directions:
            new_row, new_col = row + 2 * drow, col + 2 * dcol
            if 0 > new_row or new_row >= self.ROWS or 0 > new_col or new_col >= self.COLS:
                continue
            mid_row, mid_col = row + drow, col + dcol
            piece = self.board[row][col]

            if self.is_valid_jump(piece, mid_row, mid_col, new_row, new_col):
                moves.append((new_row, new_col))
        return moves

    def get_piece(self, row, col):
        """
        Returns the piece of the board in the defined row and col
        """
        return self.board[row][col]

    def make_move(self, move):
        """
        Makes a move
        """
        piece_row, piece_col = move[0][0], move[0][1]
        piece = self.board[piece_row][piece_col]
        new_pos_row, new_pos_col = move[1]

        if abs(piece_row - new_pos_row) == 2 and abs(piece_col - new_pos_col) == 2:
            mid_row = (piece_row + new_pos_row) // 2
            mid_col = (piece_col + new_pos_col) // 2
            self.jumped_piece = self.board[mid_row][mid_col]

        moved_piece = self.board[piece_row][piece_col]
        self.board[new_pos_row][new_pos_col] = moved_piece
        self.board[piece_row][piece_col] = 0
        piece.move(new_pos_row, new_pos_col)

        self.valid_moves = []

    def place_piece(self, piece, row, col):
        """
        Places a piece in a new position
        """
        self.board[row][col] = piece
        piece.move(row, col)

    def clone(self):
        """
        Clones the board
        """
        new_board = Board()
        new_board.jumped_piece = self.jumped_piece
        for row in range(self.ROWS):
            for col in range(self.COLS):
                new_board.board[row][col] = 0

        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.board[row][col] != 0:
                    new_board.board[row][col] = self.get_piece(row, col).clone()

        return new_board

    def delete_piece(self, row, col):
        """
        Deletes a piece at a given position
        """
        self.board[row][col] = 0
