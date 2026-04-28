import tkinter as tk
from tkinter import filedialog
import math
import colorsys
from PIL import ImageGrab # Для скриншотов

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class RotatingLine:
    def __init__(self, canvas):
        self.canvas = canvas
        self.center = Point(300, 300)
        self.length = 150
        self.angle = 0
        self.speed = 0.05
        self.is_running = True
        self.hue = 0
        self.line_id = None

    def update(self):
        if self.is_running:
            self.angle += self.speed
            self.hue = (self.hue + 0.01) % 1.0
            
            # Расчет координат конца отрезка
            x_end = self.center.x + self.length * math.cos(self.angle)
            y_end = self.center.y + self.length * math.sin(self.angle)
            
            # Перевод HSV в RGB для изменения цвета
            rgb = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
            color = '#%02x%02x%02x' % tuple(int(x*255) for x in rgb)
            
            if self.line_id:
                self.canvas.delete(self.line_id)
            
            self.line_id = self.canvas.create_line(
                self.center.x, self.center.y, x_end, y_end, 
                fill=color, width=3
            )
        
        self.canvas.after(20, self.update)

# Создание окна
root = tk.Tk()
root.title("Лаба 7 - Задание 1 (Вариант 5)")

canvas = tk.Canvas(root, width=600, height=500, bg='white')
canvas.pack()

line_app = RotatingLine(canvas)

# Панель управления
controls = tk.Frame(root)
controls.pack()

def toggle_pause():
    line_app.is_running = not line_app.is_running
    btn_pause.config(text="Старт" if not line_app.is_running else "Пауза")

def make_screenshot():
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    ImageGrab.grab().crop((x, y, x1, y1)).save("screenshot_line.png")
    print("Скриншот сохранен!")

btn_pause = tk.Button(controls, text="Пауза", command=toggle_pause)
btn_pause.pack(side=tk.LEFT)

tk.Label(controls, text="Скорость:").pack(side=tk.LEFT)
scale_speed = tk.Scale(controls, from_=0, to=0.2, resolution=0.01, orient=tk.HORIZONTAL,
                       command=lambda v: setattr(line_app, 'speed', float(v)))
scale_speed.set(0.05)
scale_speed.pack(side=tk.LEFT)

btn_snap = tk.Button(controls, text="Скриншот", command=make_screenshot)
btn_snap.pack(side=tk.LEFT)

line_app.update()
root.mainloop()