import copy
from board import *
import time


pygame.font.init()
FONT = pygame.font.SysFont('Arial', 30)
start_time = time.time()


def draw_timer_and_score(win, black_score, red_score):
    """
    Shows text for the result and time
    """
    current_time = int(time.time() - start_time)
    minutes = current_time // 60
    seconds = current_time % 60

    timer_text = FONT.render(f"Time: {minutes}:{seconds:02}", True, (255, 255, 255))
    win.blit(timer_text, (10, 10))

    score_text = FONT.render(f"Black: {black_score}  Red: {red_score}", True, (255, 255, 255))
    win.blit(score_text, (10, 50))


class Game:
    """
    Class consisting of all elements required for the game Checkers
    """

    SQUARE_SIZE = 600 // 8

    def __init__(self, win, player_1, player_2):
        """
        Initialize necessary objects for a checkers game
        """
        self.win = win
        self.player_1 = player_1
        self.player_2 = player_2
        self.board = Board()
        self.black_score = 0
        self.red_score = 0
        self.player_turn = 1
        self.board_size = 8
        self.game_won = False

    def update(self):
        """
        Updates the game state and time elapsed since the start of the game
        """
        self.board.draw(self.win)
        draw_timer_and_score(self.win, self.black_score, self.red_score)
        pygame.display.update()

    async def handle_ai_turn(self):
        """
        Handle AI's turn to make a move on the board
        """
        self.player_2.get_move(self)

    def get_mouse_position(self, pos):
        """
        Returns the position of the mouse
        """
        x, y = pos
        row = y // self.SQUARE_SIZE
        col = x // self.SQUARE_SIZE
        return row, col

    def get_piece(self, row, col):
        """
        Returns the piece of the board in the defined row and col
        """
        return self.board.get_piece(row, col)

    def get_all_valid_moves(self, color):
        """
        Returns all the valid moves for a given color (player)
        """
        valid_moves = []

        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.get_piece(row, col)
                if piece != 0 and piece.color == color:
                    moves = self.board.get_valid_moves(piece.row, piece.col)
                    for move in moves:
                        valid_moves.append(((piece.row, piece.col), move))

        return valid_moves

    def is_valid_move(self, row, col):
        """
        Checks whether a move is valid
        """
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.get_piece(row, col) == 0:
                return True
        return False

    def get_jumped_piece(self, move):
        """
        Returns the piece that is jumped if there is one
        """
        start_row, start_col = move[0][0], move[0][1]
        end_row, end_col = move[1][0], move[1][1]
        if abs(start_row - end_row) <= 1:
            return None
        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2
        return mid_row, mid_col

    def is_over(self):
        """
        Checks if the game is over
        """
        if self.black_score == 12:
            self.game_won = True
            return True
        if self.red_score == 12:
            return True
        if self.player_turn == 1 and not self.get_all_valid_moves(self.board.BLACK):
            return True
        if self.player_turn == 2 and not self.get_all_valid_moves(self.board.RED):
            self.game_won = True
            return True
        return False

    def show_text(self):
        """
        Displays the game text at the end of the game
        """
        won_text = FONT.render(f"Congratulations! You won!", True, (255, 255, 255))
        lost_text = FONT.render(f"You lost! Try again next time!", True, (255, 255, 255))

        if self.player_turn == 2 and not self.get_all_valid_moves(self.board.RED) or self.black_score == 12:
            self.win.blit(won_text, (150, 300))
        else:
            if self.game_won:
                self.win.blit(won_text, (150, 300))
            else:
                self.win.blit(lost_text, (150, 300))

        pygame.display.update()

    def clone(self):
        """
        Clones the current game
        """
        new_game = Game(self.win, self.player_1, self.player_2)
        new_game.black_score = self.black_score
        new_game.red_score = self.red_score
        new_game.player_turn = self.player_turn
        new_game.board = copy.deepcopy(self.board)
        return new_game
