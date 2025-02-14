import tkinter as tk
import random


CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
CELL_SIZE = 20
DELAY = 200


class SnakeGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game ")


        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.canvas.pack()

        # Стан програми: "MENU", "GAME", "GAME_OVER"
        self.state = "MENU"

        # Змінні для гри
        self.score = 0
        self.snake = None
        self.apple = None

        # Спробуємо завантажити зображення (якщо їх немає, підемо в fallback)

        self.apple_img = None
        self.snake_head_img = None
        self.snake_body_img = None

        # Обробка кліків мишкою для меню та екрану завершення
        self.canvas.bind("<Button-1>", self.handle_click)

        # Малюємо ГОЛОВНЕ МЕНЮ
        self.draw_menu()

    # ---------------------------------------------------
    #  МЕТОДИ ДЛЯ МЕНЮ
    # ---------------------------------------------------
    def draw_menu(self):
        """Малює головне меню зі кнопками: Start / Quit."""
        self.canvas.delete("all")

        self.canvas.create_text(
            CANVAS_WIDTH // 2, 100,
            text="Snake Game",
            font=("Arial", 24, "bold"),
            fill="green"
        )

        # Кнопка "Start"
        self.canvas.create_rectangle(150, 150, 250, 190, fill="lightgreen")
        self.canvas.create_text(200, 170, text="Start", font=("Arial", 16, "bold"))

        # Кнопка "Quit"
        self.canvas.create_rectangle(150, 210, 250, 250, fill="lightgreen")
        self.canvas.create_text(200, 230, text="Quit", font=("Arial", 16, "bold"))

    def handle_click(self, event):
        """
        Відслідковує кліки мишкою по Canvas.
        Залежить від поточного стану (self.state).
        """
        if self.state == "MENU":
            # Перевіряємо, чи клікнули по кнопках у меню
            if 150 < event.x < 250 and 150 < event.y < 190:
                self.start_game()  # натиснули "Start"
            elif 150 < event.x < 250 and 210 < event.y < 250:
                self.root.destroy()  # натиснули "Quit"
        elif self.state == "GAME_OVER":
            # Кнопки на екрані завершення
            if 150 < event.x < 250 and 150 < event.y < 190:
                self.start_game()  # "Play Again"
            elif 150 < event.x < 250 and 210 < event.y < 250:
                self.root.destroy()  # "Quit"

    # ---------------------------------------------------
    #  СТАРТ ГРИ
    # ---------------------------------------------------
    def start_game(self):
        """Підготовка стану для початку гри: обнуляємо змійку, яблуко, рахунок."""
        self.state = "GAME"
        self.score = 0

        # Створюємо змійку й яблуко
        self.snake = Snake()
        self.apple = Apple(self.snake.body)

        # Прив’язуємо клавіші стрілок
        self.root.bind("<Up>",    lambda e: self.snake.set_direction(0, -1))
        self.root.bind("<Down>",  lambda e: self.snake.set_direction(0, 1))
        self.root.bind("<Left>",  lambda e: self.snake.set_direction(-1, 0))
        self.root.bind("<Right>", lambda e: self.snake.set_direction(1, 0))

        # Запускаємо ігровий цикл
        self.game_loop()

    def game_loop(self):
        """Основний цикл оновлення гри: рух змійки, перевірка зіткнень, перемальовка."""
        if self.state != "GAME":
            return  # Якщо стан уже не "GAME", виходимо (напр., Game Over)

        # Рух змійки
        self.snake.move()

        # "Проходження крізь стіни" (wrap around):
        self.wrap_around()

        # Перевірка на самозіткнення
        head = self.snake.body[0]
        if head in self.snake.body[1:]:
            self.game_over()
            return

        # Перевірка чи з'їли яблуко
        if (head[0] == self.apple.x) and (head[1] == self.apple.y):
            self.score += 1
            self.snake.grow()
            self.apple.reposition(self.snake.body)

        # Малюємо кадр
        self.draw_game()
        # Плануємо виклик наступного оновлення через DELAY мілісекунд
        self.root.after(DELAY, self.game_loop)

    # ---------------------------------------------------
    #  ГРАФІКА (МАЛЮВАННЯ)
    # ---------------------------------------------------
    def draw_game(self):
        """Малює змійку, яблуко та поточний рахунок."""
        self.canvas.delete("all")

        # Малюємо яблуко
        if self.apple_img:
            # Якщо вдалося завантажити зображення
            self.canvas.create_image(
                self.apple.x * CELL_SIZE + CELL_SIZE // 2,
                self.apple.y * CELL_SIZE + CELL_SIZE // 2,
                image=self.apple_img
            )
        else:
            # fallback: червоний квадрат
            self.canvas.create_rectangle(
                self.apple.x * CELL_SIZE,
                self.apple.y * CELL_SIZE,
                self.apple.x * CELL_SIZE + CELL_SIZE,
                self.apple.y * CELL_SIZE + CELL_SIZE,
                fill="red"
            )

        # Малюємо змійку
        for i, (x, y) in enumerate(self.snake.body):
            # голова (i == 0)
            if i == 0:
                if self.snake_head_img:
                    self.canvas.create_image(
                        x * CELL_SIZE + CELL_SIZE // 2,
                        y * CELL_SIZE + CELL_SIZE // 2,
                        image=self.snake_head_img
                    )
                else:
                    self.canvas.create_rectangle(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        x * CELL_SIZE + CELL_SIZE,
                        y * CELL_SIZE + CELL_SIZE,
                        fill="yellow"
                    )
            else:
                # тіло
                if self.snake_body_img:
                    self.canvas.create_image(
                        x * CELL_SIZE + CELL_SIZE // 2,
                        y * CELL_SIZE + CELL_SIZE // 2,
                        image=self.snake_body_img
                    )
                else:
                    self.canvas.create_rectangle(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        x * CELL_SIZE + CELL_SIZE,
                        y * CELL_SIZE + CELL_SIZE,
                        fill="green"
                    )

        # Рахунок
        self.canvas.create_text(
            50, 10,
            text=f"Score: {self.score}",
            font=("Arial", 14),
            fill="black"
        )

    # ---------------------------------------------------
    #  "ПРОХОДЖЕННЯ КРІЗЬ СТІНИ"
    # ---------------------------------------------------
    def wrap_around(self):
        """
        Якщо голова змійки виходить за межі екрана – з'являється з протилежного боку.
        (20 клітинок по ширині й висоті, бо 400x400 з CELL_SIZE=20)
        """
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

        # Оновлюємо координати голови
        self.snake.body[0] = (x, y)

    # ---------------------------------------------------
    #  ЗАВЕРШЕННЯ ГРИ
    # ---------------------------------------------------
    def game_over(self):
        """Завершує гру та показує екран "GAME OVER" з вибором дії."""
        self.state = "GAME_OVER"
        self.canvas.delete("all")

        self.canvas.create_text(
            CANVAS_WIDTH // 2, 100,
            text="GAME OVER",
            font=("Arial", 24, "bold"),
            fill="red"
        )
        self.canvas.create_text(
            CANVAS_WIDTH // 2, 140,
            text=f"Score: {self.score}",
            font=("Arial", 18),
            fill="black"
        )

        # Кнопка "Play Again"
        self.canvas.create_rectangle(150, 150, 250, 190, fill="lightgreen")
        self.canvas.create_text(200, 170, text="Play Again", font=("Arial", 14))

        # Кнопка "Quit"
        self.canvas.create_rectangle(150, 210, 250, 250, fill="lightgreen")
        self.canvas.create_text(200, 230, text="Quit", font=("Arial", 14))

class Snake:
    def __init__(self):
        """
        Початок змійки – 3 сегменти горизонтально в центрі.
        head = (10, 10), потім (9,10), (8,10) ...
        """
        self.body = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)  # рухаємось вправо

    def set_direction(self, dx, dy):
        """
        Зміна напрямку руху, якщо він не протилежний поточному.
        Не даємо змійці "розвертатися на 180°".
        """
        current_dx, current_dy = self.direction
        # Забороняємо стати в протилежний напрямок
        if (dx, dy) != (-current_dx, -current_dy):
            self.direction = (dx, dy)

    def move(self):
        """Рух змійки: додаємо нову голову, видаляємо хвіст."""
        head = self.body[0]
        x, y = head
        dx, dy = self.direction
        new_head = (x + dx, y + dy)

        # Додаємо нову голову
        self.body.insert(0, new_head)
        # Видаляємо останній сегмент (хвіст)
        self.body.pop()

    def grow(self):
        """Змійка зростає, коли з'їдає яблуко (дублюємо останній сегмент)."""
        self.body.append(self.body[-1])

class Apple:
    def __init__(self, snake_body):
        """Одразу обираємо випадкове місце, де немає змійки."""
        self.reposition(snake_body)

    def reposition(self, snake_body):
        """Пошук нового місця на полі, де немає сегментів змійки."""
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
