from random import randint

import pygame as pg


class Board:
    def __init__(
        self,
        width: int = 5,
        height: int = 5,
        screen_size: tuple[int, int] = (280, 240),
        screen_position: tuple[int, int] = (0, 0),
        cell_colors: tuple[
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
        ] = (
            (28, 30, 36),  # Empty     - dark slate
            (255, 200, 87),  # Target  - warm amber
            (100, 210, 255),  # Agent  - sky blue
            (200, 60, 80),  # Obstacle - muted red
        ),
    ):
        # Invlid values
        if (width < 1 or height < 1) or (screen_size[0] < 1 or screen_size[1] < 1):
            raise ValueError("Invalid Board initializing arguments")

        self.width: int = width
        self.height: int = height

        self.cell_colors: tuple[
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
        ] = cell_colors

        self.screen_size: tuple[int, int] = screen_size
        self.screen_position: tuple[int, int] = screen_position

        self.board: list[list[int]] = []

        self.cw: int = screen_size[0] // width  # Cell width
        self.ch: int = screen_size[1] // height  # Cell height

        self.reset_board()

    def reset_board(self):
        # Generate a list of all available items
        items: list[int] = []

        obstacles = 3
        agent = 1
        targets = 2
        empty = self.width * self.height - obstacles - agent - targets

        for _ in range(obstacles):
            items.append(3)
        for _ in range(agent):
            items.append(1)
        for _ in range(targets):
            items.append(2)
        for _ in range(empty):
            items.append(0)

        # Adding the items
        self.board = []  # empty the board
        for _ in range(self.height):
            r: list[int] = []
            for _ in range(self.width):
                r.append(items.pop(randint(0, len(items) - 1)))
            self.board.append(r)

    def draw(self, surface: pg.Surface):
        x, y = self.screen_position
        for line in self.board:
            x = 0
            for cell in line:
                # Color of the cell
                color = self.cell_colors[cell]

                _ = pg.draw.rect(surface, color, (x, y, self.cw, self.ch))
                _ = pg.draw.rect(
                    surface, (255, 255, 255), (x, y, self.cw, self.ch), width=2
                )

                x += self.cw  # x position of the cell
            y += self.ch  # y position of the cell
