import tkinter as tk

def sierpinski(cvs, p1, p2, p3, depth):
    if depth == 0:
        cvs.create_polygon(p1, p2, p3, outline='black', fill='white')
    else:
        # Находим середины сторон
        p12 = [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2]
        p23 = [(p2[0]+p3[0])/2, (p2[1]+p3[1])/2]
        p31 = [(p3[0]+p1[0])/2, (p3[1]+p1[1])/2]
        # Рекурсивный вызов для 3-х внешних треугольников
        sierpinski(canvas, p1, p12, p31, depth-1)
        sierpinski(canvas, p2, p12, p23, depth-1)
        sierpinski(canvas, p3, p31, p23, depth-1)

root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=450)
canvas.pack()

# Вершины треугольника
points = [[250, 50], [50, 400], [450, 400]]
sierpinski(canvas, points[0], points[1], points[2], 4)
root.mainloop()
