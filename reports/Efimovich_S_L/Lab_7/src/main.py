import tkinter as tk
import math
import random
from PIL import ImageGrab

WIDTH = 800
HEIGHT = 600


class RotatingLine:
    def __init__(self, canvas, x, y, length):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.length = length
        self.angle = 0
        self.line = None

    def get_end(self):
        x2 = self.x + self.length * math.cos(self.angle)
        y2 = self.y + self.length * math.sin(self.angle)
        return x2, y2

    def update(self):
        self.angle += 0.05

        x2, y2 = self.get_end()

        color = f"#{random.randint(0, 0xFFFFFF):06x}"

        if self.line:
            self.canvas.delete(self.line)

        self.line = self.canvas.create_line(self.x, self.y, x2, y2, fill=color, width=3)


def draw_tree(canvas, point, length, angle, depth):
    if depth == 0:
        return

    x, y = point
    x2 = x + length * math.cos(angle)
    y2 = y - length * math.sin(angle)

    canvas.create_line(x, y, x2, y2, fill="green")

    draw_tree(canvas, (x2, y2), length * 0.7, angle + math.pi / 6, depth - 1)
    draw_tree(canvas, (x2, y2), length * 0.7, angle - math.pi / 6, depth - 1)


class App:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("ЛР7 - Вариант 5")

        self.canvas = tk.Canvas(root_window, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.line = RotatingLine(self.canvas, WIDTH // 2, HEIGHT // 2, 150)

        frame = tk.Frame(root_window)
        frame.pack()

        self.running = True

        tk.Button(frame, text="Пауза", command=self.toggle).pack(side=tk.LEFT)
        tk.Button(frame, text="Скриншот", command=self.screenshot).pack(side=tk.LEFT)
        tk.Button(frame, text="Фрактал", command=self.draw_fractal).pack(side=tk.LEFT)

        self.animate()

    def toggle(self):
        self.running = not self.running

    def screenshot(self):
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        ImageGrab.grab().crop((x, y, x1, y1)).save("screenshot.png")
        print("Скриншот сохранён как screenshot.png")

    def draw_fractal(self):
        self.canvas.delete("all")
        draw_tree(self.canvas, (WIDTH // 2, HEIGHT - 50), 100, math.pi / 2, 8)

    def animate(self):
        if self.running:
            self.canvas.delete("all")
            self.line.update()

        self.root.after(50, self.animate)


main_root = tk.Tk()
app = App(main_root)
main_root.mainloop()
