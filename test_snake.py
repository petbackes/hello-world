import unittest
from snake import Snake


class RulesTest(unittest.TestCase):
    def test_seed(self):
        self.assertEqual(Snake(seed=7).food, Snake(seed=7).food)

    def test_food_and_growth(self):
        game = Snake()
        game.food = game.next_head(0)
        _, reward, done = game.step(0)
        self.assertEqual((len(game.body), game.score, reward, done), (4, 1, 10, False))

    def test_wall_and_terminal(self):
        game = Snake(5)
        game.food = (0, 0)
        while not game.done:
            game.step(0)
        with self.assertRaises(RuntimeError):
            game.step(0)

    def test_tail_vacates(self):
        game = Snake()
        game.body = [(2, 2), (2, 3), (1, 3), (1, 2)]
        game.food = (8, 8)
        self.assertFalse(game.collision((1, 2)))
        self.assertTrue(game.collision((2, 3)))

    def test_full_board(self):
        game = Snake(5)
        game.body = [(3, 0)] + [(x, y) for y in range(5) for x in range(5)
                                if (x, y) not in ((3, 0), (4, 0))]
        game.food = (4, 0)
        _, reward, done = game.step(0)
        self.assertTrue(done)
        self.assertIsNone(game.food)
        self.assertEqual(reward, 10)


if __name__ == "__main__":
    unittest.main()
