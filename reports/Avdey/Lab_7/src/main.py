import tkinter as tk
import random
import time
from PIL import ImageGrab


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def area(self, a, b, c):
        return abs((a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)) / 2.0)

    def contains(self, point):
        A = self.area(self.p1, self.p2, self.p3)
        A1 = self.area(point, self.p2, self.p3)
        A2 = self.area(self.p1, point, self.p3)
        A3 = self.area(self.p1, self.p2, point)
        return abs(A - (A1 + A2 + A3)) < 0.5


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Triangle Visualization")
        self.running = False
        self.points = []  # Инициализация атрибута points

        self.create_canvas()
        self.create_controls()
        self.create_triangle_inputs()
        self.update_triangle()

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=600, height=500, bg="white")
        self.canvas.pack()

    def create_controls(self):
        controls = tk.Frame(self.root)
        controls.pack(pady=5)

        # Количество точек
        tk.Label(controls, text="Количество точек:").grid(row=0, column=0)
        self.points_entry = tk.Entry(controls, width=5)
        self.points_entry.insert(0, "20")
        self.points_entry.grid(row=0, column=1)

        # Скорость
        tk.Label(controls, text="Скорость:").grid(row=0, column=2)
        self.speed = tk.Scale(controls, from_=1, to=100, orient=tk.HORIZONTAL, length=150)
        self.speed.set(50)
        self.speed.grid(row=0, column=3)

        # Кнопки
        tk.Button(controls, text="Старт", command=self.start).grid(row=0, column=4)
        tk.Button(controls, text="Пауза", command=self.pause).grid(row=0, column=5)
        tk.Button(controls, text="Скриншот", command=self.screenshot).grid(row=0, column=6)

    def create_triangle_inputs(self):
        triangle_frame = tk.LabelFrame(self.root, text="Координаты треугольника")
        triangle_frame.pack(pady=5)

        tk.Label(triangle_frame, text="P1 (x,y)").grid(row=0, column=0)
        self.p1x = tk.Entry(triangle_frame, width=5)
        self.p1y = tk.Entry(triangle_frame, width=5)
        self.p1x.insert(0, "150")
        self.p1y.insert(0, "100")
        self.p1x.grid(row=0, column=1)
        self.p1y.grid(row=0, column=2)

        tk.Label(triangle_frame, text="P2 (x,y)").grid(row=0, column=3)
        self.p2x = tk.Entry(triangle_frame, width=5)
        self.p2y = tk.Entry(triangle_frame, width=5)
        self.p2x.insert(0, "450")
        self.p2y.insert(0, "120")
        self.p2x.grid(row=0, column=4)
        self.p2y.grid(row=0, column=5)

        tk.Label(triangle_frame, text="P3 (x,y)").grid(row=0, column=6)
        self.p3x = tk.Entry(triangle_frame, width=5)
        self.p3y = tk.Entry(triangle_frame, width=5)
        self.p3x.insert(0, "300")
        self.p3y.insert(0, "400")
        self.p3x.grid(row=0, column=7)
        self.p3y.grid(row=0, column=8)

        tk.Button(triangle_frame, text="Обновить треугольник", command=self.update_triangle).grid(
            row=0, column=9, padx=10
        )

    def update_triangle(self):
        try:
            self.triangle = Triangle(
                Point(int(self.p1x.get()), int(self.p1y.get())),
                Point(int(self.p2x.get()), int(self.p2y.get())),
                Point(int(self.p3x.get()), int(self.p3y.get())),
            )
            self.canvas.delete("all")
            self.draw_triangle()
        except ValueError:
            pass

    def draw_triangle(self):
        self.canvas.create_polygon(
            self.triangle.p1.x,
            self.triangle.p1.y,
            self.triangle.p2.x,
            self.triangle.p2.y,
            self.triangle.p3.x,
            self.triangle.p3.y,
            outline="black",
            fill="",
        )

    def start(self):
        self.running = True
        self.canvas.delete("all")
        self.draw_triangle()

        n = int(self.points_entry.get())
        self.points = [Point(random.randint(50, 550), random.randint(50, 450)) for _ in range(n)]

        self.animate()

    def animate(self):
        if not self.running:
            return

        self.canvas.delete("points")
        self.draw_triangle()

        for point in self.points:
            color = "green" if self.triangle.contains(point) else "red"
            self.canvas.create_oval(point.x - 3, point.y - 3, point.x + 3, point.y + 3, fill=color, tags="points")

        delay = 101 - self.speed.get()
        self.root.after(delay * 10, self.animate)

    def pause(self):
        self.running = not self.running
        if self.running:
            self.animate()

    def screenshot(self):
        self.canvas.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        ImageGrab.grab().crop((x, y, x1, y1)).save(f"screenshot_{int(time.time())}.png")


if __name__ == "__main__":
    main_root = tk.Tk()
    app = App(main_root)
    main_root.mainloop()
