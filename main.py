import pygame

FPS = 50  # количество кадров в секунду
SIZE = WIDTH, HEIGHT = 650, 700


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
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

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is None:
            # Пользователь нажал мимо поля, поэтому ничего не делать
            return
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        mx, my = mouse_pos
        if mx <= self.left or mx >= self.width * self.cell_size + self.left:
            print("Пользователь нажал слишком слева или слишком справа")
            return
        if my <= self.top or my >= self.height * self.cell_size + self.top:
            print("Пользователь нажал слишком высоко или слишком низко")
            return
        print("Пользователь внутри поля")

        column = (mx - self.left) // self.cell_size
        row = (my - self.top) // self.cell_size
        return row, column

    def on_click(self, cell):
        print(f"Пользователь нажал на клетку {cell}")

    def render(self, screen):
        level = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                 [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1],
                 [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
                 [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
                 [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                 [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
                 [1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
                 [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                 [1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                 [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
                 [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
                 [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
                 [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                 [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
                 [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
                 [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1],
                 [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        a = -1
        b = 0
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
                if level[a][b] != 0:
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
                        4)
                b += 1


def main():
    pygame.display.set_caption('Клетчатое поле начало')
    screen = pygame.display.set_mode(SIZE)

    clock = pygame.time.Clock()
    running = True

    board = Board(20, 20)
    board.set_view(25, 75, 30)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill('black')
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()

