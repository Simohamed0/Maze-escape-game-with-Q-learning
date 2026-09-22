import random
import unittest

from agent.DoubleQAgent import DoubleQAgent
from maze.maze import Maze


class MazeTests(unittest.TestCase):
    def setUp(self):
        random.seed(7)

    def test_generators_produce_reachable_exit(self):
        for algorithm in ("prim", "eller", "hunt-and-kill"):
            maze = Maze(8, 8, algorithm)
            self.assertTrue(maze._is_reachable(), algorithm)

    def test_flags_and_teleports_do_not_overlap(self):
        maze = Maze(8, 8)
        self.assertTrue(set(maze.flags).isdisjoint(maze.teleport_points))
        self.assertNotIn(maze.start, maze.flags)
        self.assertNotIn(maze.exit, maze.flags)

    def test_episode_reset_clears_history(self):
        maze = Maze(8, 8)
        maze.flags_collected.update(maze.flags)
        maze.visited_states.add(maze.exit)
        maze.reset_episode()
        self.assertEqual(maze.flags_collected, set())
        self.assertEqual(maze.visited_states, {maze.start})

    def test_double_q_update_uses_other_table(self):
        maze = Maze(8, 8)
        agent = DoubleQAgent(maze, alpha=1.0, gamma=1.0)
        state = maze.state(maze.start)
        next_position = next(
            (point for point in ((1, 0), (0, 1)) if not maze.is_wall(*point)),
            maze.start,
        )
        next_state = maze.state(next_position)
        actions = maze.valid_actions(next_position)
        agent.action = maze.valid_actions(maze.start)[0]
        best = actions[0]
        agent.q_table1[next_state] = {action: (5.0 if action == best else 0.0) for action in actions}
        agent.q_table2[next_state] = {best: 3.0}
        agent._update(agent.q_table1, agent.q_table2, state, next_state, 1.0, False)
        self.assertEqual(agent.q_table1[state][agent.action], 4.0)


if __name__ == "__main__":
    unittest.main()
