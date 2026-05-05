"""
Лабораторная работа №7. Вариант 10: Кривая Пеано.
Реализация GUI на tkinter с анимацией и управлением.
"""
import tkinter as tk
from tkinter import messagebox


class PeanoCurveApp(tk.Tk):
    """Приложение для визуализации кривой Пеано."""

    def __init__(self):
        super().__init__()
        self.title("Кривая Пеано - Марчук М.Т.")
        self.geometry("900x700")

        self.is_running = True
        self.speed = 50
        self.depth = 3
        self.points = []

        self._setup_ui()
        self.update_fractal()

    def _setup_ui(self):
        """Создание элементов интерфейса."""
        self.canvas = tk.Canvas(self, bg="white", width=600, height=600)
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        ctrl_frame = tk.Frame(self, width=250)
        ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.btn_pause = tk.Button(ctrl_frame, text="Пауза", command=self.toggle_pause)
        self.btn_pause.pack(fill=tk.X, pady=5)

        tk.Label(ctrl_frame, text="Глубина рекурсии:").pack()
        self.depth_scale = tk.Scale(ctrl_frame, from_=1, to=4, orient=tk.HORIZONTAL,
                                     command=self.on_param_change)
        self.depth_scale.set(3)
        self.depth_scale.pack(fill=tk.X, pady=5)

        tk.Label(ctrl_frame, text="Скорость (задержка мс):").pack()
        self.speed_scale = tk.Scale(ctrl_frame, from_=1, to=200, orient=tk.HORIZONTAL)
        self.speed_scale.set(50)
        self.speed_scale.pack(fill=tk.X, pady=5)

        tk.Button(ctrl_frame, text="Снять скриншот", command=self.take_screenshot).pack(fill=tk.X, pady=5)

    def toggle_pause(self):
        """Приостановка/запуск анимации."""
        self.is_running = not self.is_running
        self.btn_pause.config(text="Старт" if not self.is_running else "Пауза")

    def on_param_change(self, _):
        """Обработка изменения параметров."""
        self.depth = self.depth_scale.get()
        self.update_fractal()

    def generate_peano(self, x, y, size, depth):
        """Рекурсивный алгоритм генерации точек кривой Пеано."""
        if depth == 0:
            self.points.append((x + size / 2, y + size / 2))
            return

        new_size = size / 3
        for i in range(3):
            for j in range(3):
                self.generate_peano(x + i * new_size, y + j * new_size, new_size, depth - 1)

    def update_fractal(self):
        """Обновление списка точек и сброс холста."""
        self.canvas.delete("all")
        self.points = []
        self.generate_peano(50, 50, 500, self.depth)
        self.draw_step(0)

    def draw_step(self, index):
        """Пошаговая отрисовка для эффекта анимации."""
        if not self.is_running:
            self.after(100, lambda: self.draw_step(index))
            return

        if index < len(self.points) - 1:
            p1 = self.points[index]
            p2 = self.points[index + 1]
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="blue", width=2)
            self.speed = self.speed_scale.get()
            self.after(self.speed, lambda: self.draw_step(index + 1))

    def take_screenshot(self):
        """Сохранение холста в файл."""
        try:
            self.canvas.postscript(file="peano_fractal.ps", colormode='color')
            messagebox.showinfo("Готово", "Скриншот сохранен как peano_fractal.ps")
        except OSError as err:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {err}")


if __name__ == "__main__":
    app = PeanoCurveApp()
    app.mainloop()
