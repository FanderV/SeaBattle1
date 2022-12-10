import pygame
import random
import server
import client


window_size = 30  # block_size
left_field = 40
up_field = 30

black = (0, 0, 0)
white = (255, 255, 255)
blue = (51, 153, 255)

size = (left_field + 26.5 * window_size, up_field + 12 * window_size)  # размер окна

pygame.init()

Display = pygame.display.set_mode(size)
pygame.display.set_caption("Sea Battle")

font_size = int(window_size / 1.5)

font = pygame.font.SysFont('Times New Roman', font_size)


class ShipsOnGrid:
    def __init__(self):
        self.available_blocks = set((a, b) for a in range(1, 11) for b in range(1, 11))
        self.ships_set = set()
        self.ships = self.populate_grid()

    def create_start_block(self, available_blocks):
        x_or_y = random.randint(0, 1)
        str_rev = random.choice((-1, 1))
        x, y = random.choice(tuple(available_blocks))
        return x, y, x_or_y, str_rev

    def create_ship(self, number_of_blocks, available_blocks):
        ship_coordinates = []
        x, y, x_or_y, str_rev = self.create_start_block(available_blocks)
        for _ in range(number_of_blocks):
            ship_coordinates.append((x, y))
            if not x_or_y:
                str_rev, x = self.add_block_to_ship(
                    x, str_rev, x_or_y, ship_coordinates)
            else:
                str_rev, y = self.add_block_to_ship(
                    y, str_rev, x_or_y, ship_coordinates)
        if self.is_ship_valid(ship_coordinates):
            return ship_coordinates
        return self.create_ship(number_of_blocks, available_blocks)

    def add_block_to_ship(self, coor, str_rev, x_or_y, ship_coordinates):
        if (coor <= 1 and str_rev == -1) or (coor >= 10 and str_rev == 1):
            str_rev *= -1
            return str_rev, ship_coordinates[0][x_or_y] + str_rev
        else:
            return str_rev, ship_coordinates[-1][x_or_y] + str_rev

    def is_ship_valid(self, new_ship):
        ship = set(new_ship)
        return ship.issubset(self.available_blocks)

    def add_new_ship_to_set(self, new_ship):
        for elem in new_ship:
            self.ships_set.add(elem)

    def update_available_blocks_for_creating_ships(self, new_ship):
        for elem in new_ship:
            for k in range(-1, 2):
                for m in range(-1, 2):
                    if 0 < (elem[0] + k) < 11 and 0 < (elem[1] + m) < 11:
                        self.available_blocks.discard((elem[0] + k, elem[1] + m))

    def populate_grid(self):
        ships_coordinates_list = []
        for number_of_blocks in range(4, 0, -1):
            for _ in range(5 - number_of_blocks):
                new_ship = self.create_ship(
                    number_of_blocks, self.available_blocks)
                ships_coordinates_list.append(new_ship)
                self.add_new_ship_to_set(new_ship)
                self.update_available_blocks_for_creating_ships(new_ship)
        return ships_coordinates_list


human1 = ShipsOnGrid()
human2 = ShipsOnGrid()


def draw_ships(ships_coordinates_list):
    for elem in ships_coordinates_list:
        ship = sorted(elem)
        x_start = ship[0][0]
        y_start = ship[0][1]
        # вертикально
        if len(ship) > 1 and ship[0][0] == ship[1][0]:
            ship_width = window_size
            ship_height = window_size * len(ship)
        # горизонтально и 1 клетка
        else:
            ship_width = window_size * len(ship)
            ship_height = window_size
        x = window_size * (x_start - 1) + left_field
        y = window_size * (y_start - 1) + up_field
        if ships_coordinates_list == human1.ships:
            x += 15 * window_size
        pygame.draw.rect(
            Display, black, ((x, y), (ship_width, ship_height)), width=window_size // 10)  # rect - прямоугольник


def draw_cells():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    for i in range(11):
        # горизонтальные линии
        pygame.draw.line(Display, black, (left_field, up_field + i * window_size),
                         (left_field + 10 * window_size, up_field + i * window_size), 1)
        # вертикальные линии
        pygame.draw.line(Display, black, (left_field + i * window_size, up_field),
                         (left_field + i * window_size, up_field + 10 * window_size), 1)
        # горизонтальные линии 2
        pygame.draw.line(Display, black, (left_field + 15 * window_size, up_field + i * window_size),
                         (left_field + 25 * window_size, up_field + i * window_size), 1)
        # вертикальные линии 2
        pygame.draw.line(Display, black, (left_field + i * window_size + 15 * window_size, up_field),
                         (left_field + i * window_size + 15 * window_size, up_field + 10 * window_size), 1)

        if i < 10:
            num_ver = font.render(str(i + 1), True, black)
            letters_hor = font.render(letters[i], True, black)
            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()
            # вертикальные сетки 1
            Display.blit(num_ver, (left_field - (window_size // 2 + num_ver_width // 2),
                                   up_field + i * window_size + (window_size // 2 - num_ver_height // 2)))
            # вертикальные сетки 1
            Display.blit(letters_hor, (
                left_field + i * window_size + (window_size // 2 - letters_hor_width // 2), up_field + 10 * window_size))

            # вертикальные сетки 2
            Display.blit(num_ver, (left_field - (window_size // 2 + num_ver_width // 2) + 15 * window_size,
                                   up_field + i * window_size + (window_size // 2 - num_ver_height // 2)))
            # вертикальные сетки 2
            Display.blit(letters_hor, (
                left_field + i * window_size + (window_size // 2 - letters_hor_width // 2) + 15 * window_size,
                up_field + 10 * window_size))


def main():
    game_over = False
    Display.fill(white)
    draw_cells()
    draw_ships(human1.ships)
    draw_ships(human2.ships)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True


main()
pygame.quit()
