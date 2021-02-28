import pygame
import random
from shapes_for_elements import shapes_for_elements, colors_for_elements

global best_score
pygame.font.init()
WIDTH = 800
HEIGHT = 700
WIDTH_TETRIS = 300
HEIGHT_TETRIS = 600
TOP_X = (WIDTH - WIDTH_TETRIS) // 2
TOP_Y = HEIGHT - HEIGHT_TETRIS
best_score = [0]


class Element:
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = colors_for_elements[shapes_for_elements.index(shape)]
        self.rotate = 0


def do_board(locked):
    board = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (j, i) in locked:
                c = locked[(j, i)]
                board[i][j] = c
    return board


def to_normal_shape(shape):
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


def current_pos(shape, board):
    get_pos = [[(j, i) for j in range(10) if board[i][j] == (0, 0, 0)] for i in range(20)]
    get_pos = [j for _ in get_pos for j in _]
    formated = to_normal_shape(shape)
    for y in formated:
        if y not in get_pos:
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


def draw_text_middle(text, size, color, screen):
    font = pygame.font.SysFont('impact', size)
    label = font.render(text, 1, color)
    screen.blit(label, (TOP_X + WIDTH_TETRIS / 2 - (label.get_width() / 2),
                        TOP_Y + HEIGHT_TETRIS / 2 - label.get_height() / 2))


def draw_grid(screen, row, col):
    for i in range(row):
        pygame.draw.line(screen, (0, 55, 0), (TOP_X, TOP_Y + i * 30),
                         (TOP_X + WIDTH_TETRIS, TOP_Y + i * 30))
        for j in range(col):
            pygame.draw.line(screen, (0, 55, 0), (TOP_X + j * 30, TOP_Y),
                             (TOP_X + j * 30, TOP_Y + HEIGHT_TETRIS))


def clear_rows(board, locked):
    global counter
    rows = 0
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
                rows += 1
        return True


def draw_next_shape(shape, screen):
    font = pygame.font.SysFont('impact', 20)
    label = font.render('Следующий элемент:', 1, (0, 255, 0))
    tetris_x = TOP_X + WIDTH_TETRIS + 50
    tetris_y = TOP_Y + HEIGHT_TETRIS / 2 - 100
    format_shape = shape.shape[shape.rotate % len(shape.shape)]
    for i, line in enumerate(format_shape):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(screen, shape.color, ((tetris_x + j * 30, tetris_y + i * 30), (30, 30)), 0)
    screen.blit(label, (tetris_x - 20, tetris_y - 30))


def give_info(screen):
    x, y = 1, 1
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('Small Font', 20)
    with open("information.txt", 'r', encoding='UTF=8') as file:
        for line in file:
            list_line = list(line)
            if len(list_line) > 1:
                del list_line[-1]
            line = ''.join(list_line)
            label = font.render(line, 1, (0, 255, 0))
            screen.blit(label, (x, y))
            y += 20


def draw_window(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('impact', 50)
    label = font.render('THE MATRIX TETRIS', 1, pygame.Color('green'))
    screen.blit(label, (TOP_X + WIDTH_TETRIS / 2 - (label.get_width() / 2), 30))
    for i in range(len(board)):
        for j in range(len(board[i])):
            pygame.draw.rect(screen, board[i][j], (TOP_X + j * 30, TOP_Y + i * 30, 30, 30), 0)
    draw_grid(screen, 20, 10)
    pygame.draw.rect(screen, (0, 255, 0), (TOP_X, TOP_Y, WIDTH_TETRIS, HEIGHT_TETRIS), 5)


def draw_menu(screen):
    font = pygame.font.SysFont('impact', 24)
    label = font.render('Попасть в матрицу', 1, (0, 255, 0))
    screen.blit(label, (WIDTH / 2 - 96, HEIGHT / 2 - 20))
    font = pygame.font.SysFont('impact', 15)
    label = font.render('Информация', 1, (0, 255, 0))
    screen.blit(label, (WIDTH - 95, HEIGHT - 40))
    pygame.draw.rect(screen, (0, 255, 0), ((WIDTH / 2 - 100, HEIGHT / 2 - 50), (200, 100)), 3)
    pygame.draw.rect(screen, (0, 255, 0), ((WIDTH - 102, HEIGHT - 50), (100, 50)), 3)
    font = pygame.font.SysFont('impact', 100)
    label = font.render('MATRIX TETRIS', 1, (0, 255, 0))
    screen.blit(label, (WIDTH / 2 - 280, 20))


def draw_current_score(current_score, screen):
    score_x = TOP_X + WIDTH_TETRIS + 50
    score_y = TOP_Y + HEIGHT_TETRIS / 2 - 100
    font = pygame.font.SysFont('impact', 24)
    label = font.render(f'Очки сбоя: {current_score}', 1, (0, 255, 0))
    screen.blit(label, (score_x + 10, score_y + 160))


def draw_best_score(best_score, screen):
    score_x = 10
    score_y = TOP_Y + HEIGHT_TETRIS / 2 - 100
    font = pygame.font.SysFont('impact', 20)
    label = font.render('Минимум Очков:', 1, (0, 255, 0))
    screen.blit(label, (score_x + 40, score_y - 30))
    label = font.render(f'{best_score}', 1, (0, 255, 0))
    screen.blit(label, (score_x + 40, score_y))


def main():
    global board
    locked = {}
    current_score = 0
    board = do_board(locked)
    current_piece = get_shape()
    next_element = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    next_level = False
    change_piece = False
    running = True

    while running:
        fall_speed = 0.3
        board = do_board(locked)
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (current_pos(current_piece, board)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not current_pos(current_piece, board):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not current_pos(current_piece, board):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate = current_piece.rotate + 1 % len(current_piece.shape)
                    if not current_pos(current_piece, board):
                        current_piece.rotate = current_piece.rotate - 1 % len(current_piece.shape)
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not current_pos(current_piece, board):
                        current_piece.y -= 1
        shape_pos = to_normal_shape(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                board[y][x] = current_piece.color
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked[p] = current_piece.color
            current_score += 10
            current_piece = next_element
            next_element = get_shape()
            change_piece = False
            combo = clear_rows(board, locked)
            if combo:
                current_score += 100
        draw_window(screen)
        draw_next_shape(next_element, screen)
        draw_best_score(best_score[-1], screen)
        draw_current_score(current_score, screen)
        pygame.display.update()
        if check_lost(locked):
            if current_score > best_score[-1]:
                best_score.append(current_score)
                next_level = True
            running = False
    # Экран окончания
    screen.fill((0, 0, 0))
    if next_level:
        draw_text_middle('Хорошая работа, ты спас всю нашу команду', 30, pygame.Color('green'), screen)
    else:
        draw_text_middle('Паражение. Тебе не удалось выполнить миссию, Нео выведен из матрицы',
                         20, pygame.Color('green'), screen)
    pygame.display.update()
    pygame.time.delay(3000)
    main_menu()


def main_menu():
    running = True
    info = False
    while running:
        if info:
            give_info(screen)
            pygame.display.update()
        else:
            screen.fill((0, 0, 0))
            draw_menu(screen)
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if 300 <= pos[0] <= 500 and 300 <= pos[1] <= 400:
                    pygame.time.delay(500)
                    main()
                elif 696 <= pos[0] <= 799 and 648 <= pos[1] <= 699:
                    info = True
    pygame.quit()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('THE MATRIX TETRIS')
main_menu()