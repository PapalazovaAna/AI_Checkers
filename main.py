import sys
from game import *
import asyncio
from player import *

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Checkers')

BLACK = (0, 0, 0)
RED = (255, 0, 0)

player_1 = HumanPlayer(BLACK)
player_2 = MinimaxPlayer(RED, depth=6)
game = Game(screen, player_1, player_2)
game.update()


async def handle_event(event):
    """
    Handles an event from the user
    """
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    elif event.type == pygame.MOUSEBUTTONDOWN and not game.is_over():
        mouse_pos = pygame.mouse.get_pos()
        row, col = game.get_mouse_position(mouse_pos)

        if game.player_turn == 1:
            if game.board.selected_piece is not None and (row, col) not in game.board.valid_moves:
                if game.board.jumped_piece is not None:
                    return
                game.board.selected_piece = None
                game.player_turn = 1
                return
            await move_player_1(row, col)

        if game.board.selected_piece is None and game.player_turn == 2:
            await asyncio.sleep(0.5)
            await game.handle_ai_turn()
            game.player_turn = 1
            game.board.jumped_piece = None
            game.board.selected_piece = None


async def move_player_1(row, col):
    """
    Handles moving player 1 (the human player)
    """
    if game.board.jumped_piece is not None:
        if (row, col) in game.board.valid_moves:
            game.board.select_and_move(row, col)
        else:
            return
    if game.board.selected_piece is None:
        game.board.select(row, col, game.board.BLACK)
    else:
        game.board.select_and_move(row, col)
        if game.board.jumped_piece is not None:
            game.board.delete_piece(game.board.jumped_piece.row, game.board.jumped_piece.col)
            game.black_score += 1

            if not game.board.get_valid_moves_after_jump(row, col):
                game.board.selected_piece = None
                game.board.jumped_piece = None
                game.player_turn = 2
            else:
                game.board.valid_moves = game.board.get_valid_moves_after_jump(row, col)
                game.update()
        else:
            game.player_turn = 2

    game.update()


async def main():
    while True:
        for event in pygame.event.get():
            await handle_event(event)

        if game.is_over():
            game.show_text()
        else:
            game.update()
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
