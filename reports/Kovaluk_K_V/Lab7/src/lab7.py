import datetime
import math
import pygame


class RotatingSegment:
    def __init__(self, screen_width=800, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = None
        self.clock = None
        self.running = True
        self.paused = False

        self.point_a = (200, 300)
        self.point_b = (600, 300)
        self.moving_point = (200, 300)
        self.rotation_angle = 0
        self.rotation_speed = 0.02
        self.moving_speed = 0.005
        self.move_t = 0

        self.font = None
        self.screenshot_count = 0

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Вращающийся отрезок")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

    def draw_segment(self, start, end, color=(255, 255, 255)):
        pygame.draw.line(self.screen, color, start, end, 3)

    def draw_point(self, point, color=(255, 0, 0), radius=8):
        pygame.draw.circle(self.screen, color, point, radius)

    def draw_controls_info(self):
        y_offset = 10
        controls = [
            "SPACE - Пауза/Возобновить",
            "UP/DOWN - Скорость вращения",
            "LEFT/RIGHT - Скорость движения точки",
            "S - Сделать скриншот",
            "ESC - Выход"
        ]
        for text in controls:
            rendered = self.font.render(text, True, (200, 200, 200))
            self.screen.blit(rendered, (10, y_offset))
            y_offset += 25

        speed_text = f"Скорость вращения: {self.rotation_speed:.3f} | Скорость движения: {self.moving_speed:.3f}"
        rendered = self.font.render(speed_text, True, (100, 255, 100))
        self.screen.blit(rendered, (10, self.screen_height - 60))

        status = "ПАУЗА" if self.paused else "РАБОТА"
        status_color = (255, 100, 100) if self.paused else (100, 255, 100)
        status_text = self.font.render(f"Статус: {status}", True, status_color)
        self.screen.blit(status_text, (10, self.screen_height - 30))

    def take_screenshot(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}_{self.screenshot_count}.png"
        pygame.image.save(self.screen, filename)
        self.screenshot_count += 1
        print(f"Скриншот сохранён: {filename}")

    def update(self):
        if not self.paused:
            self.rotation_angle += self.rotation_speed
            self.move_t += self.moving_speed
            if self.move_t > 1:
                self.move_t = 0

        self.moving_point = (
            self.point_a[0] + (self.point_b[0] - self.point_a[0]) * self.move_t,
            self.point_a[1] + (self.point_b[1] - self.point_a[1]) * self.move_t
        )

        dx = 100 * math.cos(self.rotation_angle)
        dy = 100 * math.sin(self.rotation_angle)

        rotated_start = (self.moving_point[0] - dx, self.moving_point[1] - dy)
        rotated_end = (self.moving_point[0] + dx, self.moving_point[1] + dy)

        self.screen.fill((0, 0, 0))

        self.draw_segment(self.point_a, self.point_b, (100, 100, 100))
        self.draw_segment(rotated_start, rotated_end, (255, 100, 100))
        self.draw_point(self.moving_point, (255, 0, 0))
        self.draw_point(self.point_a, (0, 255, 0), 5)
        self.draw_point(self.point_b, (0, 255, 0), 5)

        self.draw_controls_info()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_UP:
                    self.rotation_speed = min(0.1, self.rotation_speed + 0.005)
                elif event.key == pygame.K_DOWN:
                    self.rotation_speed = max(0.001, self.rotation_speed - 0.005)
                elif event.key == pygame.K_RIGHT:
                    self.moving_speed = min(0.02, self.moving_speed + 0.001)
                elif event.key == pygame.K_LEFT:
                    self.moving_speed = max(0.001, self.moving_speed - 0.001)
                elif event.key == pygame.K_s:
                    self.take_screenshot()

    def run(self):
        self.init_pygame()
        while self.running:
            self.handle_events()
            self.update()
            self.clock.tick(60)
        pygame.quit()


class KochSnowflake:
    def __init__(self, screen_width=800, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = None
        self.clock = None
        self.running = True

        self.iterations = 4
        self.start_size = 300
        self.center_x = screen_width // 2
        self.center_y = screen_height // 2

        self.animation_speed = 0.5
        self.current_iteration = 0
        self.animation_progress = 0
        self.animating = True

        self.font = None
        self.screenshot_count = 0

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Снежинка Коха")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

    def koch_curve(self, start, end, iteration):
        if iteration == 0:
            return [start, end]

        start_x, start_y = start
        end_x, end_y = end

        dx = end_x - start_x
        dy = end_y - start_y

        point1 = (start_x + dx / 3, start_y + dy / 3)
        point3 = (start_x + 2 * dx / 3, start_y + 2 * dy / 3)

        angle = math.radians(60)
        px = point1[0] + (point3[0] - point1[0]) * math.cos(angle) - (point3[1] - point1[1]) * math.sin(angle)
        py = point1[1] + (point3[0] - point1[0]) * math.sin(angle) + (point3[1] - point1[1]) * math.cos(angle)
        point2 = (px, py)

        points = []
        points.extend(self.koch_curve(start, point1, iteration - 1))
        points.extend(self.koch_curve(point1, point2, iteration - 1))
        points.extend(self.koch_curve(point2, point3, iteration - 1))
        points.extend(self.koch_curve(point3, end, iteration - 1))

        return points

    def get_snowflake_points(self, iteration):
        radius = self.start_size / 2

        angle1 = math.radians(90)
        angle2 = math.radians(210)
        angle3 = math.radians(330)

        point1 = (self.center_x + radius * math.cos(angle1), self.center_y + radius * math.sin(angle1))
        point2 = (self.center_x + radius * math.cos(angle2), self.center_y + radius * math.sin(angle2))
        point3 = (self.center_x + radius * math.cos(angle3), self.center_y + radius * math.sin(angle3))

        side1 = self.koch_curve(point1, point2, iteration)
        side2 = self.koch_curve(point2, point3, iteration)
        side3 = self.koch_curve(point3, point1, iteration)

        return side1 + side2 + side3

    def draw_snowflake(self, points, color=(255, 255, 255)):
        if len(points) < 2:
            return

        for i in range(len(points) - 1):
            pygame.draw.line(self.screen, color, points[i], points[i + 1], 2)

    def draw_controls_info(self):
        y_offset = 10
        controls = [
            f"Итерация: {self.current_iteration}/{self.iterations}",
            "UP - Увеличить итерации",
            "DOWN - Уменьшить итерации",
            "LEFT - Уменьшить размер",
            "RIGHT - Увеличить размер",
            "A - Вкл/Выкл анимацию",
            "S - Сделать скриншот",
            "ESC - Выход"
        ]
        for text in controls:
            rendered = self.font.render(text, True, (200, 200, 200))
            self.screen.blit(rendered, (10, y_offset))
            y_offset += 25

        size_text = f"Размер: {self.start_size} | Скорость анимации: {self.animation_speed:.1f}"
        rendered = self.font.render(size_text, True, (100, 255, 100))
        self.screen.blit(rendered, (10, self.screen_height - 60))

        anim_status = "АНИМАЦИЯ" if self.animating else "СТОП"
        anim_color = (255, 100, 100) if not self.animating else (100, 255, 100)
        status_text = self.font.render(f"Режим: {anim_status}", True, anim_color)
        self.screen.blit(status_text, (10, self.screen_height - 30))

    def take_screenshot(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"koch_screenshot_{timestamp}_{self.screenshot_count}.png"
        pygame.image.save(self.screen, filename)
        self.screenshot_count += 1
        print(f"Скриншот сохранён: {filename}")

    def update(self):
        if self.animating:
            self.animation_progress += self.animation_speed * 0.01
            if self.animation_progress >= 1:
                self.animation_progress = 0
                if self.current_iteration < self.iterations:
                    self.current_iteration += 1
                else:
                    self.current_iteration = 0

        target_iteration = min(int(self.current_iteration + self.animation_progress), self.iterations)
        points = self.get_snowflake_points(target_iteration)

        self.screen.fill((0, 0, 0))
        self.draw_snowflake(points, (100, 150, 255))
        self.draw_controls_info()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.iterations = min(6, self.iterations + 1)
                    self.current_iteration = min(self.current_iteration, self.iterations)
                elif event.key == pygame.K_DOWN:
                    self.iterations = max(1, self.iterations - 1)
                    self.current_iteration = min(self.current_iteration, self.iterations)
                elif event.key == pygame.K_RIGHT:
                    self.start_size = min(500, self.start_size + 20)
                elif event.key == pygame.K_LEFT:
                    self.start_size = max(100, self.start_size - 20)
                elif event.key == pygame.K_a:
                    self.animating = not self.animating
                elif event.key == pygame.K_s:
                    self.take_screenshot()

    def run(self):
        self.init_pygame()
        while self.running:
            self.handle_events()
            self.update()
            self.clock.tick(60)
        pygame.quit()


def main():
    print("Выберите задание:")
    print("1 - Вращающийся отрезок")
    print("2 - Снежинка Коха")

    choice = input("Введите номер задания (1 или 2): ").strip()

    if choice == "1":
        print("\nЗапуск вращающегося отрезка...")
        print("Управление: SPACE - пауза, UP/DOWN - скорость вращения,")
        print("LEFT/RIGHT - скорость движения точки, S - скриншот, ESC - выход\n")
        segment = RotatingSegment()
        segment.run()
    elif choice == "2":
        print("\nЗапуск снежинки Коха...")
        print("Управление: UP/DOWN - итерации, LEFT/RIGHT - размер,")
        print("A - анимация, S - скриншот, ESC - выход\n")
        snowflake = KochSnowflake()
        snowflake.run()
    else:
        print("Неверный выбор!")


if __name__ == "__main__":
    main()
