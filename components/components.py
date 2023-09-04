import pygame

class Position:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    @property
    def xy(self) -> tuple[int, int]:
        return (self.x, self.y)

class Velocity:
    def __init__(self, dx, dy, speed = 10) -> None:
        self.dx = dx
        self.dy = dy
        self.speed = speed

class Image:
    def __init__(self, image: pygame.Surface) -> None:
        self.image = image

class PlayerController:
    def __init__(self,
                 left = pygame.K_LEFT,
                 right = pygame.K_RIGHT,
                 up = pygame.K_UP,
                 down = pygame.K_DOWN) -> None:
        self.left = left
        self.right = right
        self.up = up
        self.down = down

class Text:
    def __init__(self, text: str, font: pygame.font.Font, color: str) -> None:
        self.text = text
        self.text_surface = font.render(text, True, color)
        self.font = font
        self.color = color
    def rerender(self):
        self.text_surface = self.font.render(self.text, True, self.color)