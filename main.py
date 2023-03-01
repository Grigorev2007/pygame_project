import os
import sys
import pygame
import math
import time

pygame.init()
FPS = 20  # количество кадров в секунду
SIZE = WIDTH, HEIGHT = 650, 700
all_sprites = pygame.sprite.Group()
x_cell = 1
y_cell = 1
x_pac = 30
y_pac = 30
x_ghost = 0
y_ghost = 0
counter = 0
checker = 1
lifes = 1
time_start = 1000000000
level = [["#", "#", "#", "#", "#", "#", "#", "#", "#", "*", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
         ["#", "-", "*", "*", "*", "*", "#", "#", "#", "*", "#", "#", "*", "*", "*", "#", "*", "*", "*", "#"],
         ["#", "*", "#", "#", "#", "*", "#", "#", "#", "*", "#", "#", "*", "#", "*", "*", "*", "#", "*", "#"],
         ["#", "*", "#", "#", "#", "*", "*", "*", "*", "*", "*", "*", "*", "#", "#", "#", "*", "#", "*", "#"],
         ["#", "*", "#", "#", "#", "*", "#", "#", "#", "*", "#", "#", "*", "#", "#", "#", "*", "#", "*", "#"],
         ["#", "*", "*", "*", "*", "*", "#", "#", "#", "*", "*", "*", "*", "*", "*", "*", "*", "#", "*", "#"],
         ["#", "*", "#", "#", "#", "*", "#", "#", "#", "#", "#", "#", "*", "#", "#", "#", "*", "#", "*", "#"],
         ["#", "*", "#", "#", "#", "*", "*", "*", "*", "#", "#", "#", "*", "#", "#", "#", "*", "#", "*", "#"],
         ["#", "*", "*", "*", "*", "*", "#", "#", "*", "#", "#", "#", "*", "*", "*", "*", "*", "*", "*", "#"],
         ["#", "#", "#", "*", "#", "#", "#", "*", "*", "#", "#", "#", "#", "#", "#", "#", "*", "#", "#", "#"],
         ["#", "*", "*", "*", "*", "*", "#", "*", "#", "#", "#", "#", "*", "*", "*", "*", "*", "*", "*", "#"],
         ["#", "*", "#", "#", "#", "*", "#", "*", "#", "#", "#", "#", "*", "#", "#", "#", "*", "#", "*", "#"],
         ["#", "*", "#", "#", "#", "*", "*", "*", "#", "#", "#", "#", "*", "#", "#", "#", "*", "#", "*", "#"],
         ["#", "*", "#", "#", "#", "*", "#", "*", "#", "#", "#", "#", "*", "#", "#", "#", "*", "#", "*", "#"],
         ["#", "*", "*", "*", "*", "*", "#", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "#", "*", "#"],
         ["#", "*", "#", "#", "#", "*", "#", "#", "#", "*", "#", "#", "*", "#", "#", "#", "*", "#", "*", "#"],
         ["#", "*", "#", "#", "#", "*", "*", "*", "*", "*", "*", "*", "*", "#", "#", "#", "*", "#", "*", "#"],
         ["#", "*", "#", "#", "#", "*", "#", "#", "#", "*", "#", "#", "*", "#", "*", "*", "*", "#", "*", "#"],
         ["#", "*", "*", "*", "*", "*", "#", "#", "#", "*", "#", "#", "*", "*", "*", "#", "*", "*", "*", "#"],
         ["#", "#", "#", "#", "#", "#", "#", "#", "#", "*", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]]


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


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color, image):
        super().__init__()
        self.image = image
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = "right"
        self.speed = 5

    def upd(self, level, screen):
        global x_pac, y_pac, lifes, time_start
        if self.direction == "right":
            if level[self.rect.x // 30][(self.rect.y - 80) // 30] != "#":
                self.rect.x += self.speed
            else:
                self.direction = "left"
        else:
            if level[(self.rect.x - 31) // 30][(self.rect.y - 80) // 30] != "#":
                self.rect.x -= self.speed
            else:
                self.direction = "right"
        if self.rect.x - 49 <= x_pac <= self.rect.x - 11 and self.rect.y - 109 <= y_pac <= self.rect.y - 51 \
                and lifes == 0:
            if time.time() - time_start >= 3:
                pygame.font.init()
                my_font = pygame.font.SysFont(None, 60)
                screen.fill("black")
                text_surface = my_font.render('Жизни кончились :(!', False, (0, 0, 205))
                screen.blit(text_surface, (140, 300))
                pygame.display.update()
                time.sleep(3)
                sys.exit()
        else:
            if self.rect.x - 49 <= x_pac <= self.rect.x - 11 and self.rect.y - 109 <= y_pac <= self.rect.y - 51:
                lifes -= 1
                time_start = time.time()


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
                if self.level[a][b] == "#":
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
                    if self.level[a][b] == "*":
                        pygame.draw.circle(
                            screen,
                            "yellow",
                            (x + self.cell_size // 2, y + self.cell_size // 2),
                            3)
                b += 1


class Pacman(pygame.sprite.Sprite):
    pacman_images = [pygame.transform.scale(load_image("pacman01.png"), (25, 25)),
                     pygame.transform.scale(load_image("pacman02.png"), (25, 25)),
                     pygame.transform.scale(load_image("pacman03.png"), (25, 25)),
                     pygame.transform.scale(load_image("pacman04.png"), (25, 25))]

    def __init__(self, level, *group):
        super().__init__(*group)
        self.image = Pacman.pacman_images[0]
        self.level = level
        self.image = pygame.transform.scale(self.image, (22, 22))
        self.rect = self.image.get_rect()
        self.rect.center = (70, 120)

    def update(self, screen, *args):
        global counter, checker, x_cell, y_cell, x_pac, y_pac
        counter += 1
        if counter == 4:
            counter = 0
        self.image = Pacman.pacman_images[counter]
        if args:
            if args[0] == "up":
                self.image = pygame.transform.rotate(self.image, 90)
                y_pac -= 10
                y_cell = math.floor(y_pac / 30)
                if x_pac % 30 == 0 and y_pac % 30 == 0:
                    if self.level[x_pac // 30][y_pac // 30] != "-":
                        self.level[x_pac // 30][y_pac // 30] = "-"
                        checker += 1
                if x_pac % 30 == 0:
                    x_cell = x_pac // 30
                    if self.level[x_cell][y_cell] != "#":
                        self.rect = self.rect.move(0, -10)
                    else:
                        y_pac += 10
                else:
                    y_pac += 10

            if args[0] == "down":
                self.image = pygame.transform.rotate(self.image, 270)
                y_pac += 10
                y_cell = math.ceil(y_pac / 30)
                if x_pac % 30 == 0 and y_pac % 30 == 0:
                    if self.level[x_pac // 30][y_pac // 30] != "-":
                        self.level[x_pac // 30][y_pac // 30] = "-"
                        checker += 1
                if x_pac % 30 == 0:
                    x_cell = x_pac // 30
                    if self.level[x_cell][y_cell] != "#":
                        self.rect = self.rect.move(0, 10)
                    else:
                        y_pac -= 10
                else:
                    y_pac -= 10

            if args[0] == "left":
                self.image = pygame.transform.flip(self.image, True, False)
                x_pac -= 10
                x_cell = math.floor(x_pac / 30)
                if x_pac % 30 == 0 and y_pac % 30 == 0:
                    if self.level[x_pac // 30][y_pac // 30] != "-":
                        self.level[x_pac // 30][y_pac // 30] = "-"
                        checker += 1
                if y_pac % 30 == 0:
                    y_cell = y_pac // 30
                    if x_cell == -1 and y_cell == 9:
                        self.rect = self.rect.move(570, 0)
                        x_pac = 570
                        if self.level[x_pac // 30][y_pac // 30] != "-":
                            self.level[x_pac // 30][y_pac // 30] = "-"
                            checker += 1
                    elif self.level[x_cell][y_cell] != "#":
                        self.rect = self.rect.move(-10, 0)
                    else:
                        x_pac += 10
                else:
                    x_pac += 10

            if args[0] == "right":
                x_pac += 10
                x_cell = math.ceil(x_pac / 30)
                if x_pac % 30 == 0 and y_pac % 30 == 0:
                    if self.level[x_pac // 30][y_pac // 30] != "-":
                        self.level[x_pac // 30][y_pac // 30] = "-"
                        checker += 1
                if y_pac % 30 == 0:
                    y_cell = y_pac // 30
                    if x_cell == 20 and y_cell == 9:
                        self.rect = self.rect.move(-570, 0)
                        x_pac = 0
                        if self.level[x_pac // 30][y_pac // 30] != "-":
                            self.level[x_pac // 30][y_pac // 30] = "-"
                            checker += 1
                    elif self.level[x_cell][y_cell] != "#":
                        self.rect = self.rect.move(10, 0)
                    else:
                        x_pac -= 10
                else:
                    x_pac -= 10


def main():
    global level
    pygame.font.init()
    my_font = pygame.font.SysFont(None, 60)
    pygame.display.set_caption('Клетчатое поле начало')
    screen = pygame.display.set_mode(SIZE)

    Pacman(level, all_sprites)

    clock = pygame.time.Clock()
    running = True
    board = Board(20, 20, level)
    board.set_view(25, 75, 30)
    board.render(screen)
    ghosts = pygame.sprite.Group()
    blue_ghost_image = load_image('blueghost.png', colorkey=-1)
    red_ghost_image = load_image('redghost.png', colorkey=-1)
    blue_ghost = Ghost(300, 290, (0, 0, 255), blue_ghost_image)
    red_ghost = Ghost(60, 560, (255, 0, 0), red_ghost_image)
    ghosts.add(blue_ghost, red_ghost)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            all_sprites.update(screen, "left")
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            all_sprites.update(screen, "right")
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            all_sprites.update(screen, "up")
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            all_sprites.update(screen, "down")
        all_sprites.draw(screen)
        for ghost in ghosts:
            ghost.upd(level, screen)
        ghosts.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        screen.fill("black")
        if checker == 168:
            text_surface = my_font.render('Ты выиграл!', False, (255, 255, 0))
            screen.blit(text_surface, (210, 300))
            pygame.display.update()
            time.sleep(3)
            break
        else:
            board.render(screen)
            text_surface = my_font.render('Очков: ' + str(checker) + " из 168", False, (0, 0, 205))
            screen.blit(text_surface, (280, 30))
            text_surface2 = my_font.render('Жизней: ' + str(lifes + 1), False, (205, 0, 0))
            screen.blit(text_surface2, (30, 30))


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
