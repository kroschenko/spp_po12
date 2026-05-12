import tkinter as tk

class BouncingCircle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.r = 20
        self.x, self.y = 50, 50
        self.dx, self.dy = 5, 3  # Скорость
        self.circle = self.canvas.create_oval(self.x-self.r, self.y-self.r,
                                              self.x+self.r, self.y+self.r, fill="blue")
        self.running = True

    def move(self):
        if not self.running: return
        self.canvas.move(self.circle, self.dx, self.dy)
        pos = self.canvas.coords(self.circle)
        # Проверка границ
        if pos[0] <= 0 or pos[2] >= 400:
            self.dx = -self.dx
        if pos[1] <= 0 or pos[3] >= 300:
            self.dy = -self.dy
        self.canvas.after(20, self.move)

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()
app = BouncingCircle(canvas)
app.move()
root.mainloop()
