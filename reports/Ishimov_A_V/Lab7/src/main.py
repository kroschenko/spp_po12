import tkinter as tk
import math
import time
from PIL import ImageGrab


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Segment:
    """Отрезок, заданный двумя точками."""

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def point_at(self, t: float) -> Point:
        """Возвращает точку на отрезке при параметре t ∈ [0, 1]."""
        return Point(
            self.p1.x + t * (self.p2.x - self.p1.x),
            self.p1.y + t * (self.p2.y - self.p1.y),
        )

    def length(self) -> float:
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        return math.hypot(dx, dy)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Вращающийся отрезок")

        self.running = False
        self.t = 0.0  # Положение опорной точки на базовом отрезке [0..1]
        self.t_dir = 1  # Направление движения опорной точки
        self.angle = 0.0  # Текущий угол вращения

        self._create_canvas()
        self._create_controls()
        self._create_segment_inputs()
        self._draw_base_segment()

    # ------------------------------------------------------------------ UI --

    def _create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=600, height=500, bg="white")
        self.canvas.pack()

    def _create_controls(self):
        controls = tk.Frame(self.root)
        controls.pack(pady=5)

        tk.Label(controls, text="Длина вращ. отрезка:").grid(row=0, column=0)
        self.len_entry = tk.Entry(controls, width=5)
        self.len_entry.insert(0, "80")
        self.len_entry.grid(row=0, column=1)

        tk.Label(controls, text="Скорость:").grid(row=0, column=2)
        self.speed = tk.Scale(controls, from_=1, to=100, orient=tk.HORIZONTAL, length=150)
        self.speed.set(50)
        self.speed.grid(row=0, column=3)

        tk.Button(controls, text="Старт", command=self.start).grid(row=0, column=4)
        tk.Button(controls, text="Пауза", command=self.pause).grid(row=0, column=5)
        tk.Button(controls, text="Скриншот", command=self.screenshot).grid(row=0, column=6)

    def _create_segment_inputs(self):
        frame = tk.LabelFrame(self.root, text="Координаты базового отрезка")
        frame.pack(pady=5)

        tk.Label(frame, text="P1 (x, y)").grid(row=0, column=0)
        self.p1x = tk.Entry(frame, width=5)
        self.p1x.insert(0, "100")
        self.p1y = tk.Entry(frame, width=5)
        self.p1y.insert(0, "250")
        self.p1x.grid(row=0, column=1)
        self.p1y.grid(row=0, column=2)

        tk.Label(frame, text="P2 (x, y)").grid(row=0, column=3)
        self.p2x = tk.Entry(frame, width=5)
        self.p2x.insert(0, "500")
        self.p2y = tk.Entry(frame, width=5)
        self.p2y.insert(0, "250")
        self.p2x.grid(row=0, column=4)
        self.p2y.grid(row=0, column=5)

        tk.Button(frame, text="Обновить", command=self._update_segment).grid(row=0, column=6, padx=10)

    # --------------------------------------------------------- helpers -------

    def _read_segment(self) -> Segment:
        return Segment(
            Point(int(self.p1x.get()), int(self.p1y.get())),
            Point(int(self.p2x.get()), int(self.p2y.get())),
        )

    def _update_segment(self):
        try:
            self.base_segment = self._read_segment()
            self._draw_base_segment()
        except ValueError:
            pass

    def _draw_base_segment(self):
        try:
            seg = self._read_segment()
        except ValueError:
            return
        self.base_segment = seg
        self.canvas.delete("all")
        self.canvas.create_line(seg.p1.x, seg.p1.y, seg.p2.x, seg.p2.y, fill="black", width=2, tags="base")

    # --------------------------------------------------------- animation -----

    def start(self):
        self.running = True
        try:
            self.base_segment = self._read_segment()
        except ValueError:
            return
        self.t = 0.0
        self.t_dir = 1
        self.angle = 0.0
        self._animate()

    def pause(self):
        self.running = not self.running
        if self.running:
            self._animate()

    def _animate(self):
        if not self.running:
            return

        # Шаг зависит от скорости
        speed_val = self.speed.get()  # 1..100
        t_step = speed_val * 0.0003  # скорость движения по базовому отрезку
        a_step = speed_val * 0.06  # скорость вращения (градусы за кадр)

        # Движение опорной точки туда-обратно
        self.t += t_step * self.t_dir
        if self.t >= 1.0:
            self.t = 1.0
            self.t_dir = -1
        elif self.t <= 0.0:
            self.t = 0.0
            self.t_dir = 1

        self.angle = (self.angle + a_step) % 360

        # Опорная точка на базовом отрезке
        pivot = self.base_segment.point_at(self.t)

        # Длина вращающегося отрезка
        try:
            rot_len = float(self.len_entry.get())
        except ValueError:
            rot_len = 80.0

        # Концы вращающегося отрезка
        rad = math.radians(self.angle)
        dx = rot_len * math.cos(rad)
        dy = rot_len * math.sin(rad)

        x1r = pivot.x - dx
        y1r = pivot.y - dy
        x2r = pivot.x + dx
        y2r = pivot.y + dy

        # Перерисовка
        self.canvas.delete("all")

        # Базовый отрезок
        seg = self.base_segment
        self.canvas.create_line(seg.p1.x, seg.p1.y, seg.p2.x, seg.p2.y, fill="black", width=2)

        # Вращающийся отрезок
        self.canvas.create_line(x1r, y1r, x2r, y2r, fill="blue", width=2)

        # Опорная точка
        r = 4
        self.canvas.create_oval(pivot.x - r, pivot.y - r, pivot.x + r, pivot.y + r, fill="red", outline="red")

        # Следующий кадр: задержка обратно пропорциональна скорости
        delay = max(10, 110 - speed_val)
        self.root.after(delay, self._animate)

    # --------------------------------------------------------- screenshot ----

    def screenshot(self):
        self.canvas.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        filename = f"screenshot_segment_{int(time.time())}.png"
        ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
        print(f"Скриншот сохранён: {filename}")


if __name__ == "__main__":
    main_root = tk.Tk()
    app = App(main_root)
    main_root.mainloop()

# main.py
