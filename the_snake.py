from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Координаты центра игрового поля
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 20

# Настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pg.display.set_caption('Змейка')

# Настройка времени
clock = pg.time.Clock()

# Соответствие (текущее направление, нажатая клавиша)
# направление. Разворот на 180 градусов отсутствует специально
# для таких пар записи в словаре нет, и направление не меняется
TURNS = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}


class GameObject:
    """Базовый класс для игровых объектов"""

    def __init__(self, position=SCREEN_CENTER, body_color=None):
        """Задаёт позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, color=None):
        """Отрисовывает одну ячейку игрового поля."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color or self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовка объекта. Переопределяется в дочерних классах"""
        raise NotImplementedError(
            'Метод draw должен быть переопределён в дочернем классе'
        )


class Apple(GameObject):
    """Класс яблока, которое появляется в случайной точке поля"""

    def __init__(
        self,
        position=SCREEN_CENTER,
        body_color=APPLE_COLOR,
        occupied_positions=None
    ):
        """Задаёт цвет яблока и его первую позицию на поле"""
        super().__init__(position, body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=None):
        """Ставит яблоко в случайную клетку вне занятых позиций"""
        occupied_positions = occupied_positions or ()
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in occupied_positions:
                self.position = position
                return

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс змейки: движение, рост, столкновения"""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        """Задаёт начальное состояние змейки."""
        super().__init__(position, body_color)
        self.reset()
        self.direction = RIGHT

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки, добавляя новую голову в начало"""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length else None
        )

    def draw(self):
        """Отрисовывает змейку на экране, затирая след"""
        self.draw_cell(self.get_head_position())

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, меняя направление змейки"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            game_object.next_direction = TURNS.get(
                (game_object.direction, event.key),
                game_object.direction
            )


def main():
    """Основной игровой цикл"""
    pg.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
