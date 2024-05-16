from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

# Цвета используемые в игре:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Создание и настройка окна игры:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


class GameObject():
    """Базовый класс, необходимый для описания других объектов."""

    position = (GRID_WIDTH // 2 * GRID_SIZE,
                GRID_HEIGHT // 2 * GRID_SIZE)
    body_color = (0, 0, 0)

    def __init__(self):
        pass

    def draw(self):
        """Метод для будущих классов"""
        pass


class Apple(GameObject):
    """Класс описывающий яблоко и действия с ним."""

    body_color = APPLE_COLOR

    def __init__(self):
        self.position = self.randomize_position()

    def randomize_position(self):
        """Генерация случайной позиции."""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовка объекта."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)


class Snake(GameObject):
    """Класс описывающий змейку и ее поведение."""

    direction = RIGHT
    next_direction = None
    body_color = SNAKE_COLOR
    last = None

    def __init__(self):
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [super().position, ]

    def update_direction(self):
        """Функция для обновления направления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        """Функция определящяющая следующую ячейку движения змеи"""
        head = self.get_head_position()
        new_x = head[0] + self.direction[0] * GRID_SIZE
        new_y = head[1] + self.direction[1] * GRID_SIZE

        if new_x < 0 or new_x >= 640:
            new_x = 0 if new_x >= 640 else 640

        if new_y < 0 or new_y >= 480:
            new_y = 0 if new_y >= 480 else 480

        new_head_position = (new_x, new_y)

        if new_head_position in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)
            if new_head_position != apple.position:
                self.last = self.positions.pop()
            else:
                self.length += 1
                while True:
                    apple.position = apple.randomize_position()
                    if apple.position not in self.positions:
                        break

    def draw(self):
        """Функция отрисовки."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            self.last = None
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Функция возвращающася позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс игры в случае проигрыша."""
        self.__init__()


def handle_keys(game_object):
    """Обработка нажимаемых клавишь игроком."""
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
    """Основная функция игры."""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        apple.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        snake.draw()
        clock.tick(20)
        pygame.display.update()


if __name__ == '__main__':
    main()
