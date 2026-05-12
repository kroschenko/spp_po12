import time
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageGrab
import math


class KochSnowflake:
    """Генератор снежинки Коха."""

    def __init__(self, size: int, iterations: int):
        self.size = size
        self.iterations = iterations

    def _koch_points(self, p1, p2, depth):
        """Рекурсивно строит список точек кривой Коха между p1 и p2."""
        if depth == 0:
            return [p1, p2]

        x1, y1 = p1
        x2, y2 = p2

        # Три точки деления отрезка
        ax = x1 + (x2 - x1) / 3
        ay = y1 + (y2 - y1) / 3

        bx = x1 + 2 * (x2 - x1) / 3
        by = y1 + 2 * (y2 - y1) / 3

        # Вершина равностороннего треугольника
        angle = math.atan2(y2 - y1, x2 - x1) - math.pi / 3
        length = math.hypot(x2 - x1, y2 - y1) / 3
        cx = ax + length * math.cos(angle)
        cy = ay + length * math.sin(angle)

        pts = []
        pts += self._koch_points(p1, (ax, ay), depth - 1)[:-1]
        pts += self._koch_points((ax, ay), (cx, cy), depth - 1)[:-1]
        pts += self._koch_points((cx, cy), (bx, by), depth - 1)[:-1]
        pts += self._koch_points((bx, by), p2, depth - 1)
        return pts

    def get_points(self, cx, cy):
        """Возвращает все точки снежинки Коха, центрированной в (cx, cy)."""
        r = self.size / 2

        # Три вершины равностороннего треугольника
        p1 = (cx + r * math.cos(math.radians(-90)), cy + r * math.sin(math.radians(-90)))
        p2 = (cx + r * math.cos(math.radians(30)), cy + r * math.sin(math.radians(30)))
        p3 = (cx + r * math.cos(math.radians(150)), cy + r * math.sin(math.radians(150)))

        pts = []
        pts += self._koch_points(p1, p2, self.iterations)[:-1]
        pts += self._koch_points(p2, p3, self.iterations)[:-1]
        pts += self._koch_points(p3, p1, self.iterations)[:-1]
        pts.append(pts[0])  # замкнуть контур
        return pts


class KochApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Снежинка Коха")

        self.img = None
        self.photo = None

        self._create_canvas()
        self._create_controls()

    # ------------------------------------------------------------------ UI --

    def _create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=600, height=550, bg="white")
        self.canvas.pack()

    def _create_controls(self):
        controls = tk.Frame(self.root)
        controls.pack(pady=5)

        # Размер
        tk.Label(controls, text="Размер:").grid(row=0, column=0)
        self.size_entry = tk.Entry(controls, width=5)
        self.size_entry.insert(0, "400")
        self.size_entry.grid(row=0, column=1)

        # Итерации
        tk.Label(controls, text="Итерации (0-6):").grid(row=0, column=2)
        self.iter_entry = tk.Entry(controls, width=5)
        self.iter_entry.insert(0, "4")
        self.iter_entry.grid(row=0, column=3)

        # Цвет линии
        tk.Label(controls, text="Цвет:").grid(row=0, column=4)
        self.color_var = tk.StringVar(value="blue")
        color_menu = tk.OptionMenu(controls, self.color_var, "blue", "black", "red", "green", "purple")
        color_menu.grid(row=0, column=5)

        # Заливка
        self.fill_var = tk.BooleanVar(value=True)
        tk.Checkbutton(controls, text="Заливка", variable=self.fill_var).grid(row=0, column=6)

        # Кнопки
        tk.Button(controls, text="Нарисовать", command=self.draw).grid(row=0, column=7, padx=5)
        tk.Button(controls, text="Скриншот", command=self.screenshot).grid(row=0, column=8)

    # --------------------------------------------------------- drawing ------

    def draw(self):
        try:
            size = int(self.size_entry.get())
            iterations = int(self.iter_entry.get())
            iterations = max(0, min(iterations, 6))  # ограничиваем 0..6
        except ValueError:
            return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        cx, cy = width // 2, height // 2

        snowflake = KochSnowflake(size, iterations)
        pts = snowflake.get_points(cx, cy)

        # Рисуем через PIL для сглаживания
        self.img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(self.img)

        flat = [(x, y) for x, y in pts]
        color = self.color_var.get()

        if self.fill_var.get():
            draw.polygon(flat, fill=self._lighten(color), outline=color)
        else:
            draw.line(flat, fill=color, width=2)

        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Подпись
        self.canvas.create_text(
            cx, 20, text=f"Снежинка Коха  |  итераций: {iterations}  |  размер: {size}", font=("Arial", 11), fill="gray"
        )

    @staticmethod
    def _lighten(color_name: str) -> str:
        """Возвращает светлый оттенок для заливки."""
        mapping = {
            "blue": "#cce0ff",
            "black": "#cccccc",
            "red": "#ffd0d0",
            "green": "#ccffcc",
            "purple": "#e8ccff",
        }
        return mapping.get(color_name, "#e0e0ff")

    # --------------------------------------------------------- screenshot ----

    def screenshot(self):
        self.canvas.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        filename = f"screenshot_koch_{int(time.time())}.png"
        ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
        print(f"Скриншот сохранён: {filename}")


if __name__ == "__main__":
    main_root = tk.Tk()
    app = KochApp(main_root)
    main_root.mainloop()

# task_2.py
