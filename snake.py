"""Dependency-free Snake rules, shared by the game and learning project."""
import random

DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))


class Snake:
    def __init__(self, size=12, seed=None):
        if size < 5:
            raise ValueError("Board size must be at least 5")
        self.size = size
        self.rng = random.Random(seed)
        self.reset()

    def reset(self):
        c = self.size // 2
        self.body = [(c, c), (c - 1, c), (c - 2, c)]
        self.direction = 0
        self.score = self.steps = self.hunger = 0
        self.done = False
        self.food = self.spawn_food()
        return self.state()

    def spawn_food(self):
        free = [(x, y) for y in range(self.size) for x in range(self.size)
                if (x, y) not in self.body]
        return self.rng.choice(free) if free else None

    def next_head(self, direction):
        x, y = self.body[0]
        dx, dy = DIRECTIONS[direction]
        return x + dx, y + dy

    def collision(self, head):
        x, y = head
        # Moving into the old tail is legal when it moves away this turn.
        occupied = self.body if head == self.food else self.body[:-1]
        return not (0 <= x < self.size and 0 <= y < self.size) or head in occupied

    def state(self):
        x, y = self.body[0]
        fx, fy = self.food or (x, y)
        danger = tuple(int(self.collision(self.next_head((self.direction + d) % 4)))
                       for d in (0, 1, -1))
        return danger + (self.direction, int(fx < x), int(fx > x),
                         int(fy < y), int(fy > y))

    def step(self, action):
        """Relative actions: 0 straight, 1 right, 2 left; return state/reward/done."""
        if self.done:
            raise RuntimeError("Reset before stepping a finished episode")
        if action not in (0, 1, 2):
            raise ValueError("Action must be 0, 1, or 2")
        self.direction = (self.direction + (0, 1, -1)[action]) % 4
        head = self.next_head(self.direction)
        self.steps += 1
        self.hunger += 1
        if self.collision(head):
            self.done = True
            return self.state(), -10.0, True
        self.body.insert(0, head)
        reward = -0.01
        if head == self.food:
            self.score += 1
            self.hunger = 0
            reward = 10.0
            self.food = self.spawn_food()
            self.done = self.food is None
        else:
            self.body.pop()
        if self.hunger >= self.size * self.size * 4:
            self.done = True
            reward = -10.0
        return self.state(), reward, self.done
