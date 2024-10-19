import pygame


class Piece:
    """
    Class consisting of all elements required for a piece in the game Checkers
    """
    PADDING = 5
    OUTLINE = 15

    def __init__(self, row, col, color, king=False):
        """
        Initializes the piece with the given information
        """
        self.row = row
        self.col = col
        self.color = color
        self.king = king

    def make_king(self):
        """
        Makes the piece a king
        """
        self.king = True

    def draw(self, win):
        """
        Draws the piece on the board
        """
        radius = 600 // 8 // 2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            image = pygame.image.load("crown.png")
            image = pygame.transform.scale(image, (radius * 2, radius * 2))
            win.blit(image, (self.x - radius, self.y - radius))

    def move(self, row, col):
        """
        Moves the piece
        """
        self.row = row
        self.col = col
        if (self.color == (0, 0, 0) and row == 0) or (self.color == (255, 0, 0) and row == 7):
            self.make_king()

    @property
    def x(self):
        """
        Returns the x coordinate of the piece
        """
        return self.col * 600 // 8 + 600 // 8 // 2

    @property
    def y(self):
        """
        Returns the y coordinate of the piece
        """
        return self.row * 600 // 8 + 600 // 8 // 2

    def clone(self):
        """
        Returns a clone of the piece
        """
        return Piece(self.row, self.col, self.color, self.king)
