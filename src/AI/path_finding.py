from collections import deque

from src.items.board import Board
from src.items.cell import Cell


class PathFinder:
    def __init__(self, board: Board):
        self.board: Board = board
        self.path: list[tuple[int, int]] = []

        self.agent: tuple[int, int] | None = None
        self.targets: list[tuple[int, int]] = []
        self.obstacles: frozenset[tuple[int, int]] = frozenset([])

        self.reset()

    def reset(self):
        # Turning all the Cells in the board into a 2d point for path finding
        list_obstacles: list[tuple[int, int]] = []  # Temporary variable
        self.targets = []
        self.agent = None
        self.obstacles = frozenset([])

        for y in range(self.board.height):
            for x in range(self.board.width):
                cell: int = self.board.board[y][x]
                if cell == Cell.AGENT:
                    self.agent = (x, y)
                elif cell == Cell.TARGET:
                    self.targets.append((x, y))
                elif cell == Cell.OBSTACLES:
                    list_obstacles.append((x, y))

        if self.agent is None or len(self.targets) == 0:
            raise ValueError(
                f"Board does not contain Enough elements ! {1 if self.agent is None else 0} Agent, {len(self.targets)} Targets"
            )

        self.obstacles = frozenset(list_obstacles)

    def get_path(self) -> list[tuple[int, int]] | None:
        """
        BFS from start to goal. Returns the shortest path including both ends,
        or None if no path exists.
        """

        if self.agent is None:
            raise ValueError("Faulty Board, no agent found")

        queue: deque[tuple[int, int]] = deque([self.agent])
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {self.agent: None}

        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

        while queue:
            current = queue.popleft()

            if current == self.targets[0]:
                # Reconstruct path
                path: list[tuple[int, int]] = []
                node: tuple[int, int] | None = current
                while node is not None:
                    path.append(node)
                    node = came_from[node]
                path.reverse()
                return path

            x, y = current
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                # Bounds check
                if not (0 <= nx < self.board.width and 0 <= ny < self.board.height):
                    continue

                neighbor = (nx, ny)

                # Skip obstacles and already-visited cells
                if neighbor in self.obstacles or neighbor in came_from:
                    continue

                came_from[neighbor] = current
                queue.append(neighbor)

        return None

    def move(self) -> None:
        # Check if finished all targets
        if not self.targets:
            print("Already done.")
            return

        # No path yet
        if not self.path:
            path = self.get_path()
            if path is None:
                print("No clear path to target")
                return
            self.path = path

        # Advance one cell
        _ = self.path.pop(0)  # remove current cell
        if not self.path:
            return
        self.agent = self.path[0]
        self.board.setAgent(self.agent)

        # Reached this target? Drop it so next leg goes to the next one.
        if self.agent == self.targets[0]:
            _ = self.targets.pop(0)
            self.path = []  # force replan for the next leg
