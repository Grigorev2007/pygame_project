import os
import sys
import pygame

pygame.init()
FPS = 20  # количество кадров в секунду
SIZE = WIDTH, HEIGHT = 650, 700
all_sprites = pygame.sprite.Group()
x_pac = 1
y_pac = 1


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('*')
    return list(map(lambda x: x.ljust(max_width, '*'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    # создание поля
    def __init__(self, width, height, level):
        self.width = width
        self.height = height
        self.level = level
        self.board = [
            [0] * width for _ in range(height)
        ]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        a = -1
        end_x = self.width * self.cell_size + self.left
        end_y = self.height * self.cell_size + self.top
        for x in range(self.left, end_x, self.cell_size):
            a += 1
            b = 0
            for y in range(self.top, end_y, self.cell_size):
                pygame.draw.rect(
                    screen,
                    (5, 255, 255),
                    (x, y, self.cell_size, self.cell_size),
                    width=1
                )
                if self.level[a][b] != "*":
                    pygame.draw.rect(
                        screen,
                        (25, 25, 112),
                        (x, y, self.cell_size, self.cell_size),
                        width=2
                    )
                else:
                    pygame.draw.rect(
                        screen,
                        (8, 8, 8),
                        (x, y, self.cell_size, self.cell_size),
                        width=1
                    )
                    pygame.draw.circle(
                        screen,
                        "yellow",
                        (x + self.cell_size // 2, y + self.cell_size // 2),
                        3)
                b += 1


class Pacman(pygame.sprite.Sprite):
    image = load_image("pacman.png")
    def __init__(self, level, *group):
        super().__init__(*group)
        self.image = Pacman.image
        self.level = level
        self.image = pygame.transform.scale(self.image, (22, 22))
        self.rect = self.image.get_rect()
        self.rect.center = (70, 120)

    def update(self, *args):
        global x_pac, y_pac
        if args:
            if args[0] == "up":
                y_pac -= 1
                if self.level[x_pac][y_pac] != "#":
                    self.rect = self.rect.move(0, -30)
                else:
                    y_pac += 1

            if args[0] == "down":
                y_pac += 1
                if self.level[x_pac][y_pac] != "#":
                    self.rect = self.rect.move(0, 30)
                else:
                    y_pac -= 1

            if args[0] == "left":
                x_pac -= 1
                if x_pac == -1 and y_pac == 9:
                    self.rect = self.rect.move(570, 0)
                    x_pac = 19
                elif self.level[x_pac][y_pac] != "#":
                    self.rect = self.rect.move(-30, 0)
                else:
                    x_pac += 1

            if args[0] == "right":
                x_pac += 1
                if x_pac == 20 and y_pac == 9:
                    self.rect = self.rect.move(-570, 0)
                    x_pac = 0
                elif self.level[x_pac][y_pac] != "#":
                    self.rect = self.rect.move(30, 0)
                else:
                    x_pac -= 1


def main():
    pygame.display.set_caption('Клетчатое поле начало')
    screen = pygame.display.set_mode(SIZE)
    level = load_level("lvl.txt")

    Pacman(level, all_sprites)

    clock = pygame.time.Clock()
    running = True
    board = Board(20, 20, level)
    board.set_view(25, 75, 30)
    board.render(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            all_sprites.update("left")
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            all_sprites.update("right")
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            all_sprites.update("up")
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            all_sprites.update("down")
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        screen.fill("black")
        board.render(screen)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
