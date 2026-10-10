from random import randint
from re import L

import pygame as pg

from src.items.cell import Cell


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
        obstacles: int = 3,
        targets: int = 2,
    ) -> None:
        # Invlid values
        if (width < 1 or height < 1) or (screen_size[0] < 1 or screen_size[1] < 1):
            raise ValueError("Invalid Board initializing arguments")

        self.width: int = width
        self.height: int = height
        self.obstacles: int = obstacles
        self.targets: int = targets

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

    def reset_board(self) -> None:
        # Generate a list of all available items
        items: list[int] = [Cell.AGENT]  # Already has one Agent
        empty = self.width * self.height - self.obstacles - self.targets - 1

        for _ in range(self.obstacles):
            items.append(Cell.OBSTACLES)
        for _ in range(self.targets):
            items.append(Cell.TARGET)
        for _ in range(empty):
            items.append(Cell.EMPTY)

        # Adding the items
        self.board = []  # empty the board
        for _ in range(self.height):
            r: list[int] = []
            for _ in range(self.width):
                r.append(items.pop(randint(0, len(items) - 1)))
            self.board.append(r)

    def draw(self, surface: pg.Surface) -> None:
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

    def setAgent(self, position: tuple[int, int]) -> None:
        """
        Set the position of the agent anywhere that on the board that is empty
        Raises Error if the position is already occupied by an obstacle
        """
        # Getting where the agent
        old_position: tuple[int, int] | None = None
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == Cell.AGENT:
                    old_position = (x, y)

        # Check if the Agent was found on the board
        if old_position is None:
            raise RuntimeError("Agent not found on Board")

        # Checking if the desired position is an obstacle(It doesn't matter if it's target)
        if self.board[position[1]][position[0]] == Cell.OBSTACLES:
            raise ValueError("That posistion is already occupied")

        self.board[position[1]][position[0]] = (
            Cell.AGENT
        )  # Set the agent to the desired position

        # Remove the old agent
        self.board[old_position[1]][old_position[0]] = Cell.EMPTY

    def switchAgent(self, posistion: tuple[int, int]) -> None:
        old_position: tuple[int, int] | None = None
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == Cell.AGENT:
                    old_position = (x, y)

        if old_position is None:
            raise RuntimeError("Agent not found on Board")

        (
            self.board[old_position[1]][old_position[0]],
            self.board[posistion[1]][posistion[0]],
        ) = (
            self.board[posistion[1]][posistion[0]],
            self.board[old_position[1]][old_position[0]],
        )

    def setBoard(self, board: list[list[int]]):
        self.board = board
