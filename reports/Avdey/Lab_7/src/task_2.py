import time
import tkinter as tk
from PIL import Image, ImageTk, ImageGrab


class MandelbrotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Множество Мандельброта")

        self.canvas = tk.Canvas(root, width=600, height=500, bg="white")
        self.canvas.pack()

        controls = tk.Frame(root)
        controls.pack(pady=5)

        tk.Label(controls, text="Ширина:").grid(row=0, column=0)
        self.width_entry = tk.Entry(controls, width=5)
        self.width_entry.insert(0, "600")
        self.width_entry.grid(row=0, column=1)

        tk.Label(controls, text="Высота:").grid(row=0, column=2)
        self.height_entry = tk.Entry(controls, width=5)
        self.height_entry.insert(0, "500")
        self.height_entry.grid(row=0, column=3)

        tk.Label(controls, text="Макс итераций:").grid(row=0, column=4)
        self.iter_entry = tk.Entry(controls, width=5)
        self.iter_entry.insert(0, "100")
        self.iter_entry.grid(row=0, column=5)

        tk.Button(controls, text="Старт", command=self.start).grid(row=0, column=6)
        tk.Button(controls, text="Скриншот", command=self.screenshot).grid(row=0, column=7)

        self.img = None
        self.photo = None

    def mandelbrot(self, c, max_iter):
        z = 0
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z * z + c
        return max_iter

    def generate(self, width, height, max_iter):
        self.img = Image.new("RGB", (width, height))
        pixels = self.img.load()

        re_start, re_end = -2.0, 1.0
        im_start, im_end = -1.5, 1.5

        for x in range(width):
            for y in range(height):
                c = complex(re_start + (x / width) * (re_end - re_start), im_start + (y / height) * (im_end - im_start))
                m = self.mandelbrot(c, max_iter)
                color = 255 - int(m * 255 / max_iter)
                pixels[x, y] = (color, color, color)

            if x % 20 == 0:
                self.update_canvas()

        self.update_canvas()

    def update_canvas(self):
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.root.update()

    def start(self):
        width = int(self.width_entry.get())
        height = int(self.height_entry.get())
        max_iter = int(self.iter_entry.get())

        self.canvas.config(width=width, height=height)
        self.generate(width, height, max_iter)

    def screenshot(self):
        self.canvas.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(f"screenshot_mandelbrot_{int(time.time())}.png")


if __name__ == "__main__":
    main_root = tk.Tk()
    app = MandelbrotApp(main_root)
    main_root.mainloop()
