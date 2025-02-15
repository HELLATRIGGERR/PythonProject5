import tkinter as tk
import random

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
CELL_SIZE = 20
DELAY = 200
APPLE_COUNT = 3  # Кількість яблук

class SnakeGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game ")

        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.canvas.pack()

        self.state = "MENU"
        self.score = 0
        self.snake = None
        self.apples = []  # Тут буде список яблук

        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_menu()

    def draw_menu(self):
        """Малює головне меню зі кнопками: Start / Quit."""
        self.canvas.delete("all")
        self.canvas.create_text(CANVAS_WIDTH // 2, 100, text="Snake Game",
                                font=("Arial", 24, "bold"), fill="green")
        self.canvas.create_rectangle(150, 150, 250, 190, fill="lightgreen")
        self.canvas.create_text(200, 170, text="Start", font=("Arial", 16, "bold"))
        self.canvas.create_rectangle(150, 210, 250, 250, fill="lightgreen")
        self.canvas.create_text(200, 230, text="Quit", font=("Arial", 16, "bold"))

    def handle_click(self, event):
        if self.state == "MENU":
            if 150 < event.x < 250 and 150 < event.y < 190:
                self.start_game()
            elif 150 < event.x < 250 and 210 < event.y < 250:
                self.root.destroy()
        elif self.state == "GAME_OVER":
            if 150 < event.x < 250 and 150 < event.y < 190:
                self.start_game()
            elif 150 < event.x < 250 and 210 < event.y < 250:
                self.root.destroy()

    def start_game(self):
        """Підготовка стану для початку гри: обнуляємо змійку, яблука, рахунок."""
        self.state = "GAME"
        self.score = 0
        self.snake = Snake()
        self.apples = [Apple(self.snake.body) for _ in range(APPLE_COUNT)]  # Створюємо N яблук

        self.root.bind("<Up>", lambda e: self.snake.set_direction(0, -1))
        self.root.bind("<Down>", lambda e: self.snake.set_direction(0, 1))
        self.root.bind("<Left>", lambda e: self.snake.set_direction(-1, 0))
        self.root.bind("<Right>", lambda e: self.snake.set_direction(1, 0))

        self.game_loop()

    def game_loop(self):
        """Основний цикл оновлення гри."""
        if self.state != "GAME":
            return

        self.snake.move()
        self.wrap_around()

        head = self.snake.body[0]
        if head in self.snake.body[1:]:
            self.game_over()
            return

        # Перевіряємо чи змійка з'їла яблуко
        for apple in self.apples:
            if head == (apple.x, apple.y):
                self.score += 1
                self.snake.grow()
                apple.reposition(self.snake.body)  # Переміщуємо лише з'їдене яблуко

        self.draw_game()
        self.root.after(DELAY, self.game_loop)

    def draw_game(self):
        """Малює змійку, яблука та поточний рахунок."""
        self.canvas.delete("all")

        # Малюємо яблука
        for apple in self.apples:
            self.canvas.create_rectangle(
                apple.x * CELL_SIZE, apple.y * CELL_SIZE,
                apple.x * CELL_SIZE + CELL_SIZE, apple.y * CELL_SIZE + CELL_SIZE,
                fill="red"
            )

        # Малюємо змійку
        for i, (x, y) in enumerate(self.snake.body):
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE,
                fill="yellow" if i == 0 else "green"
            )

        # Рахунок
        self.canvas.create_text(50, 10, text=f"Score: {self.score}",
                                font=("Arial", 14), fill="black")

    def wrap_around(self):
        """Реалізує проходження крізь стіни."""
        head = self.snake.body[0]
        x, y = head
        max_col = (CANVAS_WIDTH // CELL_SIZE) - 1
        max_row = (CANVAS_HEIGHT // CELL_SIZE) - 1

        if x < 0:
            x = max_col
        elif x > max_col:
            x = 0
        if y < 0:
            y = max_row
        elif y > max_row:
            y = 0

        self.snake.body[0] = (x, y)

    def game_over(self):
        """Завершує гру та показує екран "GAME OVER" з вибором дії."""
        self.state = "GAME_OVER"
        self.canvas.delete("all")
        self.canvas.create_text(CANVAS_WIDTH // 2, 100, text="GAME OVER",
                                font=("Arial", 24, "bold"), fill="red")
        self.canvas.create_text(CANVAS_WIDTH // 2, 140, text=f"Score: {self.score}",
                                font=("Arial", 18), fill="black")

        self.canvas.create_rectangle(150, 150, 250, 190, fill="lightgreen")
        self.canvas.create_text(200, 170, text="Play Again", font=("Arial", 14))
        self.canvas.create_rectangle(150, 210, 250, 250, fill="lightgreen")
        self.canvas.create_text(200, 230, text="Quit", font=("Arial", 14))

class Snake:
    def __init__(self):
        self.body = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)

    def set_direction(self, dx, dy):
        current_dx, current_dy = self.direction
        if (dx, dy) != (-current_dx, -current_dy):
            self.direction = (dx, dy)

    def move(self):
        head = self.body[0]
        x, y = head
        dx, dy = self.direction
        new_head = (x + dx, y + dy)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

class Apple:
    def __init__(self, snake_body):
        self.reposition(snake_body)

    def reposition(self, snake_body):

        cols = CANVAS_WIDTH // CELL_SIZE
        rows = CANVAS_HEIGHT // CELL_SIZE
        while True:
            self.x = random.randint(0, cols - 1)
            self.y = random.randint(0, rows - 1)
            if (self.x, self.y) not in snake_body:
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = SnakeGameApp(root)
    root.mainloop()
