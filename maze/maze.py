import random

import numpy as np

from .algo import generate_random_maze_eller, generate_random_maze_hunt_and_kill, generate_random_maze_prim

MAZE_WALL = 1
MAZE_PATH = 0
MAZE_TELEPORT = 6


class Maze:
    def __init__(self, width, height, generator_algorithm="prim"):
        if width < 3 or height < 3:
            raise ValueError("Maze dimensions must be at least 3x3")
        self.width, self.height = width, height
        self.start, self.exit = (0, 0), (width - 1, height - 1)
        self.matrix = np.full((width, height), MAZE_WALL, dtype=int)
        generators = {"prim": generate_random_maze_prim, "eller": generate_random_maze_eller, "hunt-and-kill": generate_random_maze_hunt_and_kill}
        if generator_algorithm not in generators:
            raise ValueError(f"Unknown maze algorithm: {generator_algorithm}")
        generators[generator_algorithm](self)
        self.matrix[self.start] = MAZE_PATH
        self.matrix[self.exit] = MAZE_PATH
        if not self._is_reachable():
            self._carve_direct_route()

        available = [(x, y) for x in range(width) for y in range(height) if self.matrix[x, y] == MAZE_PATH and (x, y) not in {self.start, self.exit}]
        random.shuffle(available)
        flag_count = min(3, max(0, len(available) - 2))
        self.flags = available[:flag_count]
        remaining = available[flag_count:]
        self.teleport_points = remaining[:2] if len(remaining) >= 2 else []
        for point in self.teleport_points:
            self.matrix[point] = MAZE_TELEPORT
        self.reset_episode()

    def reset_episode(self):
        self.flags_collected = set()
        self.visited_states = {self.start}

    def state(self, position):
        return position, tuple(sorted(self.flags_collected))

    def is_wall(self, x, y):
        return not self.is_within_maze(x, y) or self.matrix[x, y] == MAZE_WALL

    def is_exit(self, x, y):
        return (x, y) == self.exit

    def is_within_maze(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_teleport(self, x, y):
        return (x, y) if (x, y) in self.teleport_points else None

    def valid_actions(self, position):
        x, y = position
        candidates = ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
        return [action for action, point in enumerate(candidates) if not self.is_wall(*point)]

    def step(self, position, action):
        moves = ((-1, 0), (1, 0), (0, -1), (0, 1))
        if action not in range(4):
            raise ValueError("Action must be 0, 1, 2, or 3")
        dx, dy = moves[action]
        candidate = (position[0] + dx, position[1] + dy)
        if self.is_wall(*candidate):
            return position, -1.0, False
        next_position, reward = candidate, -0.1
        if next_position in self.teleport_points:
            next_position = self.teleport_points[1 - self.teleport_points.index(next_position)]
            reward += 0.1
        if next_position in self.flags and next_position not in self.flags_collected:
            self.flags_collected.add(next_position)
            reward += 1.0
        if next_position in self.visited_states:
            reward -= 0.2
        self.visited_states.add(next_position)
        done = next_position == self.exit and len(self.flags_collected) == len(self.flags)
        if done:
            reward += 10.0
        elif next_position == self.exit:
            reward -= float(len(self.flags) - len(self.flags_collected))
        return next_position, reward, done

    def _is_reachable(self):
        frontier, seen = [self.start], {self.start}
        while frontier:
            position = frontier.pop()
            if position == self.exit:
                return True
            x, y = position
            for point in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if point not in seen and not self.is_wall(*point):
                    seen.add(point)
                    frontier.append(point)
        return False

    def _carve_direct_route(self):
        x, y = self.start
        while x != self.exit[0]:
            self.matrix[x, y] = MAZE_PATH
            x += 1
        while y != self.exit[1]:
            self.matrix[x, y] = MAZE_PATH
            y += 1
        self.matrix[self.exit] = MAZE_PATH
