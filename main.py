import tkinter as tk
from tkinter import ttk, font
import time
import math

class RasterAlgorithmsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Растровые алгоритмы")
        self.geometry("1000x700")
        self.scale = 1  # Масштаб (1 пиксель = 1 единица координат)
        self.point_size = 3  # Размер точки
        self.create_widgets()
        self.create_fonts()  # Инициализация шрифтов
        self.setup_canvas()

    def create_fonts(self):
        # Инициализация шрифта с начальным размером
        self.label_font = font.Font(family="Helvetica", size=10)

    def create_widgets(self):
        # Фрейм для элементов управления
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Выбор алгоритма
        tk.Label(control_frame, text="Выберите алгоритм:").pack(anchor=tk.W)
        self.algorithm = tk.StringVar(value="DDA")
        algorithms = [("Пошаговый алгоритм", "step"),
                      ("Алгоритм ЦДА", "DDA"),
                      ("Алгоритм Брезенхема (отрезок)", "bresenham_line"),
                      ("Алгоритм Брезенхема (окружность)", "bresenham_circle"),
                      ("Алгоритм Кастла-Питвея", "casteljau"),
                      ("Алгоритм Ву (сглаживание)", "wu_line")]
        for text, mode in algorithms:
            tk.Radiobutton(control_frame, text=text, variable=self.algorithm,
                           value=mode).pack(anchor=tk.W)

        # Поля ввода координат
        tk.Label(control_frame, text="Начальная точка (x0, y0):").pack(anchor=tk.W)
        self.x0_entry = tk.Entry(control_frame)
        self.x0_entry.pack(anchor=tk.W)
        self.y0_entry = tk.Entry(control_frame)
        self.y0_entry.pack(anchor=tk.W)

        tk.Label(control_frame, text="Конечная точка (x1, y1):").pack(anchor=tk.W)
        self.x1_entry = tk.Entry(control_frame)
        self.x1_entry.pack(anchor=tk.W)
        self.y1_entry = tk.Entry(control_frame)
        self.y1_entry.pack(anchor=tk.W)

        # Поля ввода для окружности
        tk.Label(control_frame, text="Центр окружности (xc, yc):").pack(anchor=tk.W)
        self.xc_entry = tk.Entry(control_frame)
        self.xc_entry.pack(anchor=tk.W)
        self.yc_entry = tk.Entry(control_frame)
        self.yc_entry.pack(anchor=tk.W)
        tk.Label(control_frame, text="Радиус (r):").pack(anchor=tk.W)
        self.r_entry = tk.Entry(control_frame)
        self.r_entry.pack(anchor=tk.W)

        # Кнопки управления
        tk.Button(control_frame, text="Отрисовать", command=self.draw).pack(pady=5)
        tk.Button(control_frame, text="Очистить", command=self.clear_canvas).pack(pady=5)

        # Кнопки масштабирования
        tk.Button(control_frame, text="Увеличить масштаб", command=self.zoom_in).pack(pady=5)
        tk.Button(control_frame, text="Уменьшить масштаб", command=self.zoom_out).pack(pady=5)

        # Метка для отображения времени выполнения
        self.time_label = tk.Label(control_frame, text="Время выполнения: N/A")
        self.time_label.pack(pady=5)

    def setup_canvas(self):
        # Холст для рисования
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda event: self.draw_grid())
        self.draw_grid()

    def draw_grid(self):
        # Отрисовка системы координат
        self.canvas.delete("grid")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        # Центр координат
        ox = width // 2
        oy = height // 2
        # Шаг сетки
        base_grid_step = 20  # Базовый шаг сетки в пикселях
        grid_step = base_grid_step * self.scale

        if grid_step == 0:
            grid_step = 1  # Избежать деления на ноль

        # Минимальное расстояние между метками в пикселях
        min_label_spacing = 50  
        # Вычисление шага меток, чтобы обеспечить минимальное расстояние
        label_step = max(1, math.ceil(min_label_spacing / grid_step))

        # Обновление размера шрифта в зависимости от масштаба
        # Размер шрифта увеличивается при уменьшении масштаба
        # Ограничиваем размер шрифта между 8 и 20
        # Используем обратную пропорцию: меньше scale -> больше размер шрифта
        new_font_size = max(8, min(int(20 / self.scale), 20))
        self.label_font.configure(size=new_font_size)

        # Линии сетки и подписи по оси X
        for i in range(int(-ox / grid_step), int(ox / grid_step) + 1):
            x = ox + i * grid_step
            self.canvas.create_line(x, 0, x, height, fill="lightgrey", tag="grid")
            if i != 0 and i % label_step == 0:
                self.canvas.create_text(x, oy + 15, text=str(i), fill="black", font=self.label_font, tag="grid_text")

        # Линии сетки и подписи по оси Y
        for i in range(int(-oy / grid_step), int(oy / grid_step) + 1):
            y = oy + i * grid_step
            self.canvas.create_line(0, y, width, y, fill="lightgrey", tag="grid")
            if i != 0 and i % label_step == 0:
                self.canvas.create_text(ox + 15, y, text=str(-i), fill="black", font=self.label_font, tag="grid_text")

        # Оси координат
        self.canvas.create_line(ox, 0, ox, height, fill="black", arrow=tk.LAST, tag="grid")
        self.canvas.create_line(0, oy, width, oy, fill="black", arrow=tk.LAST, tag="grid")
        # Подписи осей
        self.canvas.create_text(ox - 10, oy + 10, text="0", fill="black", font=self.label_font, tag="grid_text")
        self.canvas.create_text(width - 10, oy + 10, text="X", fill="black", font=self.label_font, tag="grid_text")
        self.canvas.create_text(ox + 10, 10, text="Y", fill="black", font=self.label_font, tag="grid_text")

        # Поднять все элементы с тегом "grid_text" поверх других элементов с тегом "grid"
        self.canvas.tag_raise("grid_text")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.time_label.config(text="Время выполнения: N/A")

    def draw(self):
        self.clear_canvas()
        alg = self.algorithm.get()
        start_time = time.time()
        if alg == "step":
            self.step_by_step()
        elif alg == "DDA":
            self.dda_algorithm()
        elif alg == "bresenham_line":
            self.bresenham_line()
        elif alg == "bresenham_circle":
            self.bresenham_circle()
        elif alg == "casteljau":
            self.casteljau_algorithm()
        elif alg == "wu_line":
            self.wu_line()
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000  # Время в миллисекундах
        self.time_label.config(text=f"Время выполнения: {elapsed_time:.2f} мс")

    def to_canvas_coords(self, x, y):
        # Преобразование логических координат в координаты Canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        ox = width // 2  # Центр по X
        oy = height // 2  # Центр по Y

        # Логические координаты умножаются на текущий масштаб
        canvas_x = ox + x * (20 * self.scale)  # 20 — базовый шаг сетки
        canvas_y = oy - y * (20 * self.scale)  # Y инвертируется
        return canvas_x, canvas_y

    def put_pixel(self, x, y, color="black"):
        x, y = self.to_canvas_coords(x, y)
        size = self.point_size * self.scale
        half_size = size / 2
        self.canvas.create_rectangle(x - half_size, y - half_size, x + half_size, y + half_size,
                                     fill=color, outline=color, tag="pixel")

    def step_by_step(self):
        try:
            x0 = int(self.x0_entry.get())
            y0 = int(self.y0_entry.get())
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
        except ValueError:
            return
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            self.put_pixel(x0, y0)
            return
        x_inc = dx / steps
        y_inc = dy / steps
        x = x0
        y = y0
        for i in range(steps + 1):
            self.put_pixel(round(x), round(y))
            x += x_inc
            y += y_inc

    def dda_algorithm(self):
        try:
            x0 = int(self.x0_entry.get())
            y0 = int(self.y0_entry.get())
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
        except ValueError:
            return
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            self.put_pixel(x0, y0)
            return
        x_inc = dx / steps
        y_inc = dy / steps
        x = x0
        y = y0
        for i in range(steps + 1):
            self.put_pixel(round(x), round(y))
            x += x_inc
            y += y_inc

    def bresenham_line(self):
        try:
            x0 = int(self.x0_entry.get())
            y0 = int(self.y0_entry.get())
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
        except ValueError:
            return
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        if dx > dy:
            err = dx / 2.0
            while x != x1:
                self.put_pixel(x, y)
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                self.put_pixel(x, y)
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        self.put_pixel(x, y)

    def bresenham_circle(self):
        try:
            xc = int(self.xc_entry.get())
            yc = int(self.yc_entry.get())
            r = int(self.r_entry.get())
        except ValueError:
            return
        x = 0
        y = r
        d = 3 - 2 * r
        self.draw_circle_points(xc, yc, x, y)
        while y >= x:
            x += 1
            if d > 0:
                y -=1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
            self.draw_circle_points(xc, yc, x, y)

    def draw_circle_points(self, xc, yc, x, y):
        points = [
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x),
        ]
        for point in points:
            self.put_pixel(*point)

    def casteljau_algorithm(self):
        try:
            x0 = float(self.x0_entry.get())
            y0 = float(self.y0_entry.get())
            x1 = float(self.x1_entry.get())
            y1 = float(self.y1_entry.get())
            x2 = float(self.xc_entry.get()) if self.xc_entry.get() else (x0 + x1) / 2
            y2 = float(self.yc_entry.get()) if self.yc_entry.get() else (y0 + y1) / 2
        except ValueError:
            return
        self.casteljau_curve([(x0, y0), (x2, y2), (x1, y1)])

    def casteljau_curve(self, points, t_step=0.001):
        t = 0
        while t <= 1:
            x, y = self.de_casteljau(points.copy(), t)
            self.put_pixel(round(x), round(y), color="blue")
            t += t_step

    def de_casteljau(self, points, t):
        while len(points) > 1:
            points = [((1 - t) * p0[0] + t * p1[0],
                       (1 - t) * p0[1] + t * p1[1]) for p0, p1 in zip(points[:-1], points[1:])]
        return points[0]

    def wu_line(self):
        try:
            x0 = float(self.x0_entry.get())
            y0 = float(self.y0_entry.get())
            x1 = float(self.x1_entry.get())
            y1 = float(self.y1_entry.get())
        except ValueError:
            return
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = y1 - y0
        gradient = dy / dx if dx != 0 else 1
        x_end = round(x0)
        y_end = y0 + gradient * (x_end - x0)
        x_pix1 = x_end
        y_pix1 = int(y_end)
        self.plot_wu(steep, x_pix1, y_pix1, y_end - y_pix1)
        intery = y_end + gradient
        x_end = round(x1)
        y_end = y1 + gradient * (x_end - x1)
        x_pix2 = x_end
        y_pix2 = int(y_end)
        self.plot_wu(steep, x_pix2, y_pix2, y_end - y_pix2)
        for x in range(x_pix1 + 1, x_pix2):
            y = int(intery)
            self.plot_wu(steep, x, y, intery - y)
            intery += gradient

    def plot_wu(self, steep, x, y, brightness):
        brightness = max(0, min(int(255 * (1 - brightness)), 255))
        color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
        if steep:
            self.put_pixel(y, x, color)
            self.put_pixel(y + 1, x, color)
        else:
            self.put_pixel(x, y, color)
            self.put_pixel(x, y + 1, color)

    def zoom_in(self):
        self.scale *= 1.5
        self.draw_grid()
        self.redraw_all()

    def zoom_out(self):
        self.scale /= 1.5
        self.draw_grid()
        self.redraw_all()

    def redraw_all(self):
        # Перерисовать все элементы после изменения масштаба
        # Сохраним текущ выбранный алгоритм и параметры
        alg = self.algorithm.get()
        x0 = self.x0_entry.get()
        y0 = self.y0_entry.get()
        x1 = self.x1_entry.get()
        y1 = self.y1_entry.get()
        xc = self.xc_entry.get()
        yc = self.yc_entry.get()
        r = self.r_entry.get()

        # Очистить холст и сетку
        self.canvas.delete("all")
        self.draw_grid()

        # Если есть введенные данные, перерисовать фигуры
        if alg in ["step", "DDA", "bresenham_line", "wu_line"]:
            if x0 and y0 and x1 and y1:
                try:
                    start_time = time.time()
                    if alg == "step":
                        self.step_by_step()
                    elif alg == "DDA":
                        self.dda_algorithm()
                    elif alg == "bresenham_line":
                        self.bresenham_line()
                    elif alg == "wu_line":
                        self.wu_line()
                    end_time = time.time()
                    elapsed_time = (end_time - start_time) * 1000  # Время в миллисекундах
                    self.time_label.config(text=f"Время выполнения: {elapsed_time:.2f} мс")
                except Exception as e:
                    print(f"Ошибка при перерисовке: {e}")
        elif alg in ["bresenham_circle", "casteljau"]:
            if (xc and yc and r) or (alg == "casteljau" and x0 and y0 and x1 and y1):
                try:
                    start_time = time.time()
                    if alg == "bresenham_circle":
                        self.bresenham_circle()
                    elif alg == "casteljau":
                        self.casteljau_algorithm()
                    end_time = time.time()
                    elapsed_time = (end_time - start_time) * 1000  # Время в миллисекундах
                    self.time_label.config(text=f"Время выполнения: {elapsed_time:.2f} мс")
                except Exception as e:
                    print(f"Ошибка при перерисовке: {e}")

if __name__ == "__main__":
    app = RasterAlgorithmsApp()
    app.mainloop()
