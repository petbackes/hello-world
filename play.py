"""A small pastel Snake game. Run python play.py on a desktop."""
import tkinter as tk
from snake import Snake


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Little Snake • a tiny arcade garden")
        self.root.configure(bg="#f4f1e8")
        self.game = Snake(16)
        self.cell = 26
        self.paused = False
        self.pending = None
        self.best = 0
        tk.Label(self.root, text="LITTLE SNAKE", font=("Arial", 23, "bold"),
                 bg="#f4f1e8", fg="#254c3a").pack(pady=(20, 5))
        self.status = tk.Label(self.root, bg="#f4f1e8", fg="#254c3a",
                               font=("Arial", 12))
        self.status.pack(pady=8)
        self.canvas = tk.Canvas(self.root, width=416, height=416,
                                bg="#e2ebd9", highlightthickness=0)
        self.canvas.pack(padx=24)
        tk.Label(self.root, text="Arrows / WASD • Space to pause • R to restart",
                 bg="#f4f1e8", fg="#536653").pack(pady=18)
        self.root.bind("<KeyPress>", self.key)
        self.draw()
        self.root.after(140, self.tick)

    def key(self, event):
        key = event.keysym.lower()
        if key == "r":
            self.game.reset()
            self.pending = None
            self.paused = False
        elif key == "space":
            self.paused = not self.paused
        elif self.pending is None:
            direction = {"right": 0, "d": 0, "down": 1, "s": 1,
                         "left": 2, "a": 2, "up": 3, "w": 3}.get(key)
            if direction is not None:
                delta = (direction - self.game.direction) % 4
                if delta != 2:
                    self.pending = {0: 0, 1: 1, 3: 2}[delta]
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for y in range(16):
            for x in range(16):
                if (x + y) % 2 == 0:
                    self.canvas.create_rectangle(x*26, y*26, x*26+26, y*26+26,
                                                  fill="#dce6d2", outline="")
        for i, (x, y) in enumerate(self.game.body):
            self.canvas.create_rectangle(x*26+2, y*26+2, x*26+24, y*26+24,
                                          fill="#285943" if i == 0 else "#78a86d",
                                          outline="")
        if self.game.food:
            x, y = self.game.food
            self.canvas.create_oval(x*26+5, y*26+5, x*26+22, y*26+22,
                                     fill="#e67979", outline="")
        self.best = max(self.best, self.game.score)
        self.status.config(text=f"Apples {self.game.score}     Session best {self.best}")
        if self.game.done or self.paused:
            label = "Garden complete!" if self.game.food is None else "Game over • press R"
            if not self.game.done:
                label = "Paused"
            self.canvas.create_rectangle(35, 170, 381, 246, fill="#f4f1e8", outline="")
            self.canvas.create_text(208, 208, text=label, fill="#254c3a",
                                     font=("Arial", 18, "bold"))

    def tick(self):
        if not self.paused and not self.game.done:
            self.game.step(self.pending if self.pending is not None else 0)
            self.pending = None
            self.draw()
        self.root.after(max(65, 140 - self.game.score * 3), self.tick)


if __name__ == "__main__":
    Game().root.mainloop()
