import time

KING_VALUE = 2
PIECE_VALUE = 1
CENTER_VALUE = 2


class Player:
    """
    Base player class
    """
    def __init__(self, color):
        self.color = color


class HumanPlayer(Player):
    """
    Human player class
    """
    def __init__(self, color):
        super().__init__(color)


class AIPlayer(Player):
    """
    Base AI player class that contains all the functions necessary
    for both Minimax and Expectimax agents
    """
    def __init__(self, color):
        super().__init__(color)

    def execute_multijump_for_clone(self, game, jumped_piece, move):
        """
        Executes moves after a jump only for the cloned game
        """
        game.board.delete_piece(jumped_piece[0], jumped_piece[1])
        next_jump = move
        while True:
            next_jump = self.get_next_jump_move(game, next_jump)
            if next_jump is None:
                break
            game.board.make_move(next_jump)
            jumped_piece = game.get_jumped_piece(next_jump)
            game.board.delete_piece(jumped_piece[0], jumped_piece[1])

    def get_next_jump_move(self, game, move):
        """
        Returns a list of possible continuation jumps after a jump for the original game
        """
        current_piece_row, current_piece_col = move[1][0], move[1][1]
        piece = game.board.get_piece(current_piece_row, current_piece_col)
        valid_moves = game.board.get_valid_moves(piece.row, piece.col)
        for next_move in valid_moves:
            if abs(current_piece_row - next_move[0]) == 2:
                return (current_piece_row, current_piece_col), next_move

        return None

    def execute_multijump(self, game, move):
        """
        Executes a jump and all the jumps after it if there are any
        """
        game.board.make_move(move)
        jumped_piece = game.get_jumped_piece(move)

        if jumped_piece:
            game.board.delete_piece(jumped_piece[0], jumped_piece[1])
            game.red_score += 1
            game.update()
            time.sleep(1)
            next_jump = move

            while True:
                next_jump = self.get_next_jump_move(game, next_jump)
                if next_jump is None:
                    break
                game.board.make_move(next_jump)
                jumped_piece = game.get_jumped_piece(next_jump)
                game.board.delete_piece(jumped_piece[0], jumped_piece[1])
                game.red_score += 1
                game.update()
                time.sleep(0.5)

    def evaluate(self, game):
        """
        Evaluates the game against the player's moves
        """
        return self.evaluate_second(game)

    def evaluate_first(self, game):
        ai_pieces = sum(1 for row in game.board.board for piece in row if piece != 0 and piece.color == self.color)
        opponent_pieces = sum(1 for row in game.board.board for piece in row if piece != 0 and piece.color != self.color)

        return ai_pieces - opponent_pieces

    def evaluate_second(self, game):
        ai_pieces = sum(1 for row in game.board.board for piece in row if piece != 0 and piece.color == self.color)
        opponent_pieces = sum(1 for row in game.board.board for piece in row if piece != 0 and piece.color != self.color)

        ai_kings = sum(1 for row in game.board.board for piece in row if piece != 0 and piece.color == self.color and piece.king)
        opponent_kings = sum(1 for row in game.board.board for piece in row if piece != 0 and piece.color != self.color and piece.king)

        piece_score = (ai_pieces - opponent_pieces) * PIECE_VALUE
        king_score = (ai_kings - opponent_kings) * KING_VALUE

        return piece_score + king_score

    def evaluate_third(self, game):
        center_positions = [(3, 3), (3, 4), (4, 3), (4, 4)]

        agent_score = 0
        opponent_score = 0

        for row in range(game.board.ROWS):
            for col in range(game.board.COLS):
                piece = game.board.get_piece(row, col)
                if piece != 0:
                    if piece.color == game.board.BLACK and (piece.row, piece.col) in center_positions:
                        opponent_score += CENTER_VALUE
                    elif piece.color == game.board.RED and (piece.row, piece.col) in center_positions:
                        agent_score += CENTER_VALUE

        return agent_score - opponent_score

    def opponent_color(self):
        """
        Returns the color of the opponents pieces
        """
        return (255, 0, 0) if self.color == (0, 0, 0) else (0, 0, 0)


class MinimaxPlayer(AIPlayer):
    """
    Class for the Minimax agent
    """
    def __init__(self, color, depth):
        super().__init__(color)
        self.depth = depth

    def get_move(self, game):
        """
        Executes the best move
        """
        if game.is_over():
            game.show_text()
            return
        _, best_move = self.minimax(game, depth=self.depth, alpha=-float('inf'), beta=float('inf'), maximizing_player=True)
        if best_move is None:
            best_move = game.get_all_valid_moves(self.color)[0]
        self.execute_multijump(game, best_move)

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        """
        Executes the minimax algorithm
        """
        if depth == 0:
            return self.evaluate(game), None

        if maximizing_player:
            max_eval = -float('inf')
            best_move = None
            for move in game.get_all_valid_moves(self.color):
                game_copy = game.clone()
                game_copy.board.make_move(move)
                jumped_piece = game.get_jumped_piece(move)
                if jumped_piece:
                    self.execute_multijump_for_clone(game_copy, jumped_piece, move)

                eval, _ = self.minimax(game_copy, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else:
            min_eval = float('inf')
            best_move = None
            for move in game.get_all_valid_moves(self.opponent_color()):
                game_copy = game.clone()
                game_copy.board.make_move(move)
                jumped_piece = game.get_jumped_piece(move)
                if jumped_piece:
                    self.execute_multijump_for_clone(game_copy, jumped_piece, move)

                eval, _ = self.minimax(game_copy, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move


class ExpectimaxPlayer(AIPlayer):
    """
    Class for the Expectimax player
    """
    def __init__(self, color, depth=5):
        super().__init__(color)
        self.depth = depth

    def get_move(self, game):
        """
        Executes the best move
        """
        if game.is_over():
            game.show_text()
            return
        _, best_move = self.expectimax(game, self.depth, True)
        if best_move is None:
            best_move = game.get_all_valid_moves(self.color)[0]
        self.execute_multijump(game, best_move)

    def expectimax(self, game, depth, maximizing_player):
        """
        Executes the expectimax algorithm
        """
        if depth == 0:
            return self.evaluate(game), None

        if maximizing_player:
            max_eval = -float('inf')
            best_move = None
            for move in game.get_all_valid_moves(self.color):
                game_copy = game.clone()
                game_copy.board.make_move(move)
                jumped_piece = game.get_jumped_piece(move)
                if jumped_piece:
                    self.execute_multijump_for_clone(game_copy, jumped_piece, move)

                eval, _ = self.expectimax(game_copy, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            total_eval = 0
            best_move = None
            moves = game.get_all_valid_moves(self.opponent_color())
            for move in moves:
                game_copy = game.clone()
                game_copy.board.make_move(move)
                jumped_piece = game.get_jumped_piece(move)
                if jumped_piece:
                    self.execute_multijump_for_clone(game_copy, jumped_piece, move)

                eval, _ = self.expectimax(game_copy, depth - 1, True)
                total_eval += eval
            if not best_move and moves:
                best_move = moves[0]
            return total_eval / len(moves) if moves else 0, best_move
