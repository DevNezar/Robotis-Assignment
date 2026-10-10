import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "yes"

from typing import cast

import pygame as pg

from items.board import Board


def main() -> None:
    _ = pg.init()

    screen = pg.display.set_mode((280, 240))
    clock = pg.time.Clock()
    running: bool = True
    board = Board()

    while running:
        # When exit even -> exit
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                key = cast(int, event.key)
                if key == pg.K_r:
                    board.reset_board()
                if key == pg.K_ESCAPE:
                    running = False

        # Background
        _ = screen.fill("purple")

        # Items
        board.draw(screen)

        pg.display.flip()

        _ = clock.tick(60)  # Limits FPS to 60


if __name__ == "__main__":
    main()
