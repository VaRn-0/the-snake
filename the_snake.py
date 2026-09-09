from random import choice, randint
 
import pygame
 
# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
 
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
 
# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
 
# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
 
# Цвет яблока
APPLE_COLOR = (255, 0, 0)
 
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)
 
# Скорость движения змейки:
SPEED = 20
 
# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
 
# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')
 
# Настройка времени:
clock = pygame.time.Clock()
 
 
class GameObject:
    """Базовый класс для игровых объектов"""
 
    def __init__(self):
        """Задаёт стартовую позицию объекта - центр экрана"""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None
 
    def draw(self):
        """Отрисовка объекта. Переопределяется в дочерних классах"""
        pass
 
 
class Apple(GameObject):
    """Класс яблока, которое появляется в случайной точке поля"""
 
    def __init__(self):
        """Задаёт цвет яблока и его первую позицию на поле"""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()
 
    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
 
    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
 
 
class Snake(GameObject):
    """Класс змейки: движение, рост, столкновения"""
 
    def __init__(self):
        """Задаёт начальное состояние змейки: длина, позиция, цвет"""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
 
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
 
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
 
    def draw(self):
        """Отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
 
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
 
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
 
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
 
 
def main():
    """Основной игровой цикл"""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake()
    apple = Apple()
 
    while True:
        clock.tick(SPEED)
 
        handle_keys(snake)
        snake.update_direction()
        snake.move()
 
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
 
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
 
        snake.draw()
        apple.draw()
        pygame.display.update()
 
 
if __name__ == '__main__':
    main()
 