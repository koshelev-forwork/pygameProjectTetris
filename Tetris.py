import pygame
import random
from shapes_for_elements import shapes_for_elements, colors_for_elements


pygame.font.init()
WIDTH = 800
HEIGHT = 700
WIDTH_TETRIS = 300
HEIGHT_TETRIS = 600
TOP_X = (WIDTH - WIDTH_TETRIS) // 2
TOP_Y = HEIGHT - HEIGHT_TETRIS


class Element:
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = colors_for_elements[shapes_for_elements.index(shape)]
        self.rotate = 0


def create_grid(locked):
    board = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (j, i) in locked:
                c = locked[(j, i)]
                board[i][j] = c
    return board


def convert_shape_format(shape):
    positions = []
    format_shape = shape.shape[shape.rotate % len(shape.shape)]
    for i, line in enumerate(format_shape):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions


def valid_space(shape, board):
    accept_pos = [[(j, i) for j in range(10) if board[i][j] == (0, 0, 0)] for i in range(20)]
    accept_pos = [j for _ in accept_pos for j in _]
    formatted = convert_shape_format(shape)
    for y in formatted:
        if y not in accept_pos:
            if y[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Element(5, 0, random.choice(shapes_for_elements))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size)
    label = font.render(text, 1, color)
    surface.blit(label, (TOP_X + WIDTH_TETRIS/2 - (label.get_width() / 2),
                         TOP_Y + HEIGHT_TETRIS/2 - label.get_height() / 2))


def draw_grid(surface, row, col):
    tetris_x = TOP_X
    tetris_y = TOP_Y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (tetris_x, tetris_y + i * 30),
                         (tetris_x + WIDTH_TETRIS, tetris_y + i * 30))
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (tetris_x + j * 30, tetris_y),
                             (tetris_x + j * 30, tetris_y + HEIGHT_TETRIS))


def clear_rows(board, locked):
    y_plus = 0
    for i in range(len(board) - 1, -1, -1):
        row = board[i]
        if (0, 0, 0) not in row:
            y_plus += 1
            counter = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except IndexError:
                    continue
    if y_plus > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < counter:
                new_key = (x, y + y_plus)
                locked[new_key] = locked.pop(key)


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 25)
    label = font.render('Следующий элемент', 1, (255, 255, 255))
    tetris_x = TOP_X + WIDTH_TETRIS + 50
    tetris_y = TOP_Y + HEIGHT_TETRIS / 2 - 100
    format_shape = shape.shape[shape.rotate % len(shape.shape)]
    for i, line in enumerate(format_shape):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, ((tetris_x + j * 30, tetris_y + i * 30), (30, 30)), 0)
    surface.blit(label, (tetris_x + 10, tetris_y - 30))


def draw_window(surface):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('comicsans', 50)
    label = font.render('The Matrix TETRIS', 1, pygame.Color('green'))
    surface.blit(label, (TOP_X + WIDTH_TETRIS / 2 - (label.get_width() / 2), 30))
    for i in range(len(board)):
        for j in range(len(board[i])):
            pygame.draw.rect(surface, board[i][j], (TOP_X + j * 30, TOP_Y + i * 30, 30, 30), 0)
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (TOP_X, TOP_Y, WIDTH_TETRIS, HEIGHT_TETRIS), 5)


def main():
    global board
    locked = {}
    board = create_grid(locked)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        fall_speed = 0.27

        board = create_grid(locked)
        fall_time += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, board)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, board):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, board):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotate = current_piece.rotate + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, board):
                        current_piece.rotate = current_piece.rotate - 1 % len(current_piece.shape)
                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, board):
                        current_piece.y -= 1
        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                board[y][x] = current_piece.color
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            clear_rows(board, locked)
        draw_window(win)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        if check_lost(locked):
            run = False

    draw_text_middle("You Lost", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press any key to begin.', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')
main_menu()