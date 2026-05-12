"""
Оконное приложение для построения N-фрактала.

Функции:
- ввод параметров глубины рекурсии и длины сегмента;
- параметр скорости (задержка между шагами);
- пауза/продолжение;
- очистка;
- сохранение скриншота Canvas в .ps.
"""

from __future__ import annotations

import time
from typing import Tuple

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class NFractalApp:
    """Приложение для визуализации N-фрактала."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("N-фрактал")

        self.canvas_width = 600
        self.canvas_height = 600

        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="white",
        )
        self.canvas.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        ttk.Label(self.root, text="Глубина").grid(row=1, column=0, sticky="w")
        self.entry_depth = ttk.Entry(self.root, width=7)
        self.entry_depth.insert(0, "4")
        self.entry_depth.grid(row=1, column=1, sticky="w")

        ttk.Label(self.root, text="Длина").grid(row=1, column=2, sticky="w")
        self.entry_length = ttk.Entry(self.root, width=7)
        self.entry_length.insert(0, "200")
        self.entry_length.grid(row=1, column=3, sticky="w")

        ttk.Label(self.root, text="Задержка (мс)").grid(row=2, column=0, sticky="w")
        self.entry_delay = ttk.Entry(self.root, width=7)
        self.entry_delay.insert(0, "50")
        self.entry_delay.grid(row=2, column=1, sticky="w")

        self.btn_start = ttk.Button(
            self.root,
            text="Старт",
            command=self.start_drawing,
        )
        self.btn_start.grid(row=2, column=2, sticky="we", padx=2)

        self.btn_pause = ttk.Button(
            self.root,
            text="Пауза / Продолжить",
            command=self.toggle_pause,
        )
        self.btn_pause.grid(row=2, column=3, sticky="we", padx=2)

        self.btn_clear = ttk.Button(
            self.root,
            text="Очистить",
            command=self.clear_canvas,
        )
        self.btn_clear.grid(row=3, column=0, columnspan=2, sticky="we", padx=2)

        self.btn_screenshot = ttk.Button(
            self.root,
            text="Скриншот",
            command=self.save_screenshot,
        )
        self.btn_screenshot.grid(row=3, column=2, columnspan=2, sticky="we", padx=2)

        self.is_paused = False
        self.is_running = False

    def start_drawing(self) -> None:
        """Запуск отрисовки фрактала."""
        try:
            depth = int(self.entry_depth.get())
            length = float(self.entry_length.get())
            delay_ms = int(self.entry_delay.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Глубина, длина и задержка должны быть числами.")
            return

        if depth < 0 or length <= 0:
            messagebox.showerror("Ошибка", "Глубина >= 0, длина > 0.")
            return

        self.clear_canvas()
        self.is_running = True
        self.is_paused = False

        x_center = self.canvas_width / 2
        y_center = self.canvas_height / 2

        self._draw_n_fractal(
            depth,
            length,
            (x_center - length / 2, y_center + length / 2),
            (x_center + length / 2, y_center - length / 2),
            delay_ms,
        )

    def _draw_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        delay_ms: int,
    ) -> None:
        """Нарисовать линию с учётом паузы и скорости."""
        if not self.is_running:
            return

        while self.is_paused:
            self.root.update()
            time.sleep(0.05)

        self.canvas.create_line(x1, y1, x2, y2, fill="blue")
        self.canvas.update()

        try:
            delay_ms = int(self.entry_delay.get())
        except ValueError:
            delay_ms = delay_ms

        if delay_ms > 0:
            self.root.after(delay_ms)

    def _draw_n_fractal(
        self,
        depth: int,
        length: float,
        start: Tuple[float, float],
        end: Tuple[float, float],
        delay_ms: int,
    ) -> None:
        """
        Рекурсивная отрисовка N-фрактала.

        Базовая фигура: буква N между двумя точками.
        На концах "ног" рекурсивно рисуются уменьшенные N.
        """
        if not self.is_running:
            return

        x1, y1 = start
        x2, y2 = end

        self._draw_line(x1, y1, x1, y2, delay_ms)
        self._draw_line(x1, y2, x2, y1, delay_ms)
        self._draw_line(x2, y1, x2, y2, delay_ms)

        if depth == 0:
            return

        new_length = length / 2
        left_start = (x1 - new_length / 2, y1 + new_length / 2)
        left_end = (x1 + new_length / 2, y1 - new_length / 2)

        right_start = (x2 - new_length / 2, y2 + new_length / 2)
        right_end = (x2 + new_length / 2, y2 - new_length / 2)

        self._draw_n_fractal(depth - 1, new_length, left_start, left_end, delay_ms)
        self._draw_n_fractal(depth - 1, new_length, right_start, right_end, delay_ms)

    def toggle_pause(self) -> None:
        """Поставить отрисовку на паузу или продолжить."""
        if not self.is_running:
            return
        self.is_paused = not self.is_paused

    def clear_canvas(self) -> None:
        """Очистить Canvas."""
        self.canvas.delete("all")
        self.is_running = False
        self.is_paused = False

    def save_screenshot(self) -> None:
        """Сохранить содержимое Canvas в PostScript-файл."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript", "*.ps")],
            initialfile=f"n_fractal_{int(time.time())}.ps",
        )
        if not filename:
            return
        self.canvas.postscript(file=filename)
        messagebox.showinfo("Сохранено", f"Скриншот сохранён в файл:\n{filename}")


def main() -> None:
    """Точка входа."""
    root = tk.Tk()
    app = NFractalApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
