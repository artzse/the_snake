from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
UPD_DIRECTION = {
    (LEFT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_UP): UP,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_LEFT): LEFT,
    (DOWN, pg.K_RIGHT): RIGHT
}
CENTRAL = (GRID_WIDTH // 2 * GRID_SIZE,
           GRID_HEIGHT // 2 * GRID_SIZE)

# Скорость движения по умолчанию
SPEED = 20

# Цвета используемые в игре:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Змейка | Выход из игры: ESC")
clock = pg.time.Clock()


class GameObject():
    """Базовый класс, необходимый для описания других объектов."""

    def __init__(self, color=BOARD_BACKGROUND_COLOR):
        self.position = CENTRAL
        self.body_color = color

    def create_rect(self, position: tuple = CENTRAL):
        """Создание прямоугольника для дальнейшей отрисовки."""
        return pg.Rect(position,
                       (GRID_SIZE,
                        GRID_SIZE))

    def draw(self):
        """Метод для будущих классов"""
        raise NotImplementedError(
            f'Метод класса {type(self).__name__} не определён.')


class Apple(GameObject):
    """Класс описывающий яблоко и действия с ним."""

    def __init__(self, snake_positions=(), color=APPLE_COLOR):
        self.randomize_position(snake_positions)
        self.body_color = color

    def randomize_position(self, snake_positions):
        """Генерация случайной позиции."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in snake_positions:
                break

    def draw(self):
        """Функция отрисовки."""
        pg.draw.rect(screen, self.body_color,
                     self.create_rect(self.position))


class Snake(GameObject):
    """Класс описывающий змейку и ее поведение."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(color=body_color)
        self.reset()

    def update_direction(self):
        """Функция для обновления направления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Функция определящяющая следующую ячейку движения змеи."""
        self.positions = self.positions[:self.length]
        self.last = self.positions[-1]

        dir_x, dir_y = self.direction
        head_x, head_y = self.get_head_position()

        self.positions.insert(0,
                              ((head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
                               (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT))

    def get_head_position(self):
        """Получение позиции головы змеи."""
        return self.positions[0]

    def draw(self):
        """Функция отрисовки."""
        # Отрисовка головы змейки
        pg.draw.rect(screen, self.body_color,
                     self.create_rect(self.get_head_position()))

        # Затирание последнего сегмента
        if self.last:
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR,
                         self.create_rect(self.last))

    def reset(self):
        """Сброс игры до стартовых значений."""
        self.length = 1
        self.positions = [CENTRAL, ]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(object):
    """Обработка нажимаемых клавишь игроком."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False
            else:
                new_direction = (object.direction, event.key)
                object.next_direction = UPD_DIRECTION.get(new_direction,
                                                          object.direction)
    return True


def main():
    """Основная логика игры."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        if not handle_keys(snake):
            break

        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

        elif snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            snake.length += 1

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
