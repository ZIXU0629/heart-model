"""贪吃蛇：方向键控制，空格暂停，R 重新开始。"""

import random
import tkinter as tk

CELL = 20
COLS = 30
ROWS = 20
WIDTH = CELL * COLS
HEIGHT = CELL * ROWS
SPEED_MS = 120


class SnakeGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("贪吃蛇")
        self.root.resizable(False, False)

        self.score_var = tk.StringVar(value="得分: 0")
        tk.Label(root, textvariable=self.score_var, font=("Segoe UI", 12)).pack(pady=6)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack()

        tip = "方向键移动 | 空格暂停 | R 重开"
        tk.Label(root, text=tip, font=("Segoe UI", 9), fg="#666").pack(pady=4)

        self.root.bind("<KeyPress>", self.on_key)
        self.reset()
        self.tick()

    def reset(self) -> None:
        cx, cy = COLS // 2, ROWS // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.pending_direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.paused = False
        self.game_over = False
        self.score_var.set("得分: 0")
        self.draw()

    def spawn_food(self) -> tuple[int, int]:
        empty = {(x, y) for x in range(COLS) for y in range(ROWS)} - set(self.snake)
        return random.choice(list(empty))

    def on_key(self, event: tk.Event) -> None:
        key = event.keysym
        if key in ("Up", "Down", "Left", "Right"):
            mapping = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}
            nxt = mapping[key]
            # 禁止直接掉头
            if (nxt[0] + self.direction[0], nxt[1] + self.direction[1]) != (0, 0):
                self.pending_direction = nxt
        elif key == "space" and not self.game_over:
            self.paused = not self.paused
            self.draw()
        elif key in ("r", "R"):
            self.reset()

    def tick(self) -> None:
        if not self.paused and not self.game_over:
            self.step()
        self.root.after(SPEED_MS, self.tick)

    def step(self) -> None:
        self.direction = self.pending_direction
        dx, dy = self.direction
        hx, hy = self.snake[0]
        head = (hx + dx, hy + dy)

        hit_wall = not (0 <= head[0] < COLS and 0 <= head[1] < ROWS)
        hit_self = head in self.snake
        if hit_wall or hit_self:
            self.game_over = True
            self.draw()
            return

        self.snake.insert(0, head)
        if head == self.food:
            self.score += 1
            self.score_var.set(f"得分: {self.score}")
            self.food = self.spawn_food()
        else:
            self.snake.pop()
        self.draw()

    def draw(self) -> None:
        self.canvas.delete("all")
        fx, fy = self.food
        self.canvas.create_rectangle(
            fx * CELL, fy * CELL, (fx + 1) * CELL, (fy + 1) * CELL,
            fill="#e74c3c", outline="",
        )
        for i, (x, y) in enumerate(self.snake):
            color = "#2ecc71" if i == 0 else "#27ae60"
            self.canvas.create_rectangle(
                x * CELL, y * CELL, (x + 1) * CELL, (y + 1) * CELL,
                fill=color, outline="#1a1a1a",
            )
        if self.paused:
            self._overlay("暂停")
        elif self.game_over:
            self._overlay(f"游戏结束  得分 {self.score}\n按 R 重开")

    def _overlay(self, text: str) -> None:
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#000000", stipple="gray50")
        self.canvas.create_text(
            WIDTH // 2, HEIGHT // 2, text=text, fill="white",
            font=("Segoe UI", 16, "bold"), justify="center",
        )


def main() -> None:
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
