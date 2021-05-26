import pygame, sys
from pygame.locals import *
import random

play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30
top_left_x = 350
top_left_y = 300

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255),
                (128, 0, 128)]


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        global shapes
        global shape_colors
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

class TheGame:
    def __init__(self):
        self.mainClock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption('Tetris')
        self.screen = pygame.display.set_mode((1000, 1000), 0, 32)
        self.SCX = self.screen.get_width()
        self.SCY = self.screen.get_height()
        self.font = pygame.font.Font("c.ttf", 100)
        self.font_halfsize = pygame.font.Font("c.ttf", 50)

        self.green = (0, 255, 0)
        self.dark_green = (0, 100, 0)
        self.colors = [self.green, self.dark_green, self.dark_green]

        self.ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.user = ""
        self.pause = False
        self.finalscore = 0

    def pause_menu(self):
        choose_option = 0
        while self.pause:
            self.screen.fill((0, 0, 0))
            for i in range(len(self.colors)):
                if (i == choose_option):
                    self.colors[i] = self.green
                else:
                    self.colors[i] = self.dark_green
            self.draw_text_center('PAUSED', self.font, self.green, self.screen, self.SCX / 2, self.SCY / 4)

            resume_btn = pygame.Rect(270, self.SCY * 3 / 8 + 95, 470, 100)
            self.draw_text_center('RESUME', self.font, self.colors[0], self.screen, self.SCX / 2, self.SCY * 3 / 8 + 150)

            leader_btn = pygame.Rect(100, self.SCY * 5 / 8 - 5, 800, 100)
            self.draw_text_center('LEADER BOARD', self.font, self.colors[1], self.screen, self.SCX / 2, self.SCY * 5 / 8 + 50)

            menu_btn = pygame.Rect(350, self.SCY * 7 / 8 - 105, 300, 100)
            self.draw_text_center('MENU', self.font, self.colors[2], self.screen, self.SCX / 2, self.SCY * 7 / 8 - 50)

            pygame.draw.rect(self.screen, self.colors[0], resume_btn, 2, 25)
            pygame.draw.rect(self.screen, self.colors[1], leader_btn, 2, 25)
            pygame.draw.rect(self.screen, self.colors[2], menu_btn, 2, 25)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.pause = False
                    if event.key == K_DOWN:
                        if (choose_option == 2):
                            choose_option = 0
                        else:
                            choose_option += 1
                    if event.key == K_UP:
                        if (choose_option == 0):
                            choose_option = 2
                        else:
                            choose_option -= 1
                    if (event.key == pygame.K_RETURN):
                        if (choose_option == 0):
                            self.pause = False
                        if (choose_option == 1):
                            self.leader_board()
                        if (choose_option == 2):
                            self.game_menu()
            pygame.display.update()
            self.mainClock.tick(60)

    def game_play(self):
        running = True
        (_, last_score) = self.max_score()
        locked_positions = {}
        change_piece = False
        current_piece = self.get_shape()
        next_piece = self.get_shape()
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.27
        level_time = 0
        score = 0

        while running:
            fall_time += clock.get_rawtime()
            level_time += clock.get_rawtime()
            clock.tick()
            self.screen.fill((0, 0, 0))
            grid = self.create_grid(locked_positions)
            self.draw_text_right(str(score), self.font_halfsize, self.colors[0], self.screen, self.SCX - 20, 50)

            if level_time / 1000 > 5:
                level_time = 0
                if level_time > 0.12:
                    level_time -= 0.005

            if fall_time / 1000 > fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not (self.valid_space(current_piece, grid)) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.display.quit()
                if event.type == pygame.KEYDOWN:
                    if (event.key == K_RETURN and running == False):
                        self.game_play()
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not (self.valid_space(current_piece, grid)):
                            current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not (self.valid_space(current_piece, grid)):
                            current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not (self.valid_space(current_piece, grid)):
                            current_piece.y -= 1
                    if event.key == pygame.K_UP:
                        current_piece.rotation += 1
                        if not (self.valid_space(current_piece, grid)):
                            current_piece.rotation -= 1
                    if event.key == K_ESCAPE:
                        self.pause = True
                        self.pause_menu()
            shape_pos = self.convert_shape_format(current_piece)

            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_piece.color

            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece
                next_piece = self.get_shape()
                change_piece = False
                score += self.clear_rows(grid, locked_positions) * 10

            self.draw_window(grid, score, last_score)
            self.draw_next_shape(next_piece, self.screen)

            if self.check_lost(locked_positions):
                pygame.display.update()
                pygame.time.delay(1500)
                return score

            pygame.display.update()
            self.mainClock.tick(60)

    def game_menu(self):
        running = True
        choose_option = 0
        while running:
            self.screen.fill((0, 0, 0))
            for i in range(len(self.colors)):
                if (i == choose_option):
                    self.colors[i] = self.green
                else:
                    self.colors[i] = self.dark_green
            self.draw_text_left(self.user, self.font_halfsize, self.green, self.screen, 20, 50)

            play_btn = pygame.Rect(350, self.SCY * 3 / 8 + 95, 300, 100)
            self.draw_text_center('PLAY', self.font, self.colors[0], self.screen, self.SCX / 2, self.SCY * 3 / 8 + 150)

            leader_btn = pygame.Rect(100, self.SCY * 5 / 8 - 5, 800, 100)
            self.draw_text_center('LEADER BOARD', self.font, self.colors[1], self.screen, self.SCX / 2,
                                  self.SCY * 5 / 8 + 50)

            quit_btn = pygame.Rect(370, self.SCY * 7 / 8 - 105, 270, 100)
            self.draw_text_center('QUIT', self.font, self.colors[2], self.screen, self.SCX / 2, self.SCY * 7 / 8 - 50)

            pygame.draw.rect(self.screen, self.colors[0], play_btn, 2, 25)
            pygame.draw.rect(self.screen, self.colors[1], leader_btn, 2, 25)
            pygame.draw.rect(self.screen, self.colors[2], quit_btn, 2, 25)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_DOWN:
                        if (choose_option == 2):
                            choose_option = 0
                        else:
                            choose_option += 1
                    if event.key == K_UP:
                        if (choose_option == 0):
                            choose_option = 2
                        else:
                            choose_option -= 1
                    if (event.key == pygame.K_RETURN):
                        if (choose_option == 0):
                            self.game_restart()
                        if (choose_option == 1):
                            self.leader_board()
                        else:
                            pygame.quit()
                            sys.exit()
            pygame.display.update()
            self.mainClock.tick(60)

    def register_window(self):
        running = True
        login_text = ""
        password_text = ""
        encrypted_text = ""
        choose_option = 0
        faze = 0
        while running:
            self.screen.fill((0, 0, 0))
            for i in range(len(self.colors)):
                if (i == choose_option):
                    self.colors[i] = self.green
                else:
                    self.colors[i] = self.dark_green
            encrypted_text = ""
            for i in range(len(password_text)):
                encrypted_text += "*"
            name_btn = pygame.Rect(350, self.SCY * 3 / 8 + 95, 500, 100)
            self.draw_text_center(login_text, self.font, self.colors[0], self.screen, self.SCX / 2 + 100, self.SCY * 3 / 8 + 150)
            self.draw_text_center("NAME: ", self.font, self.colors[0], self.screen, 200, self.SCY * 3 / 8 + 150)

            password_btn = pygame.Rect(350, self.SCY * 5 / 8 - 5, 500, 100)
            self.draw_text_center(encrypted_text, self.font, self.colors[1], self.screen, self.SCX / 2 + 100, self.SCY * 5 / 8 + 50)
            self.draw_text_center('PASS:', self.font, self.colors[1], self.screen, 195, self.SCY * 5 / 8 + 50)

            register_btn = pygame.Rect(240, self.SCY * 7 / 8 - 105, 520, 100)
            self.draw_text_center('REGISTER', self.font, self.colors[2], self.screen, self.SCX / 2, self.SCY * 7 / 8 - 50)
            if faze == 1:
                self.draw_text_center('TRY AGAIN!', self.font, self.green, self.screen, self.SCX/2, self.SCY * 1 / 8 + 50)
            if faze == 2:
                self.draw_text_center('SUCCEED!', self.font, self.green, self.screen, self.SCX/2, self.SCY * 1 / 8 + 50)
            pygame.draw.rect(self.screen, self.colors[0], name_btn, 2, 25)
            pygame.draw.rect(self.screen, self.colors[1], password_btn, 2, 25)
            pygame.draw.rect(self.screen, self.colors[2], register_btn, 2, 25)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.main_menu()
                        choose_option = 0
                    if event.key == pygame.K_BACKSPACE:
                        if (choose_option == 0):
                            login_text = login_text[:-1]
                        else:
                            if (choose_option == 1):
                                password_text = password_text[:-1]
                    else:
                        if event.key == K_DOWN:
                            if (choose_option == 2):
                                choose_option = 0
                            else:
                                choose_option += 1
                        if event.key == K_UP:
                            if (choose_option == 0):
                                choose_option = 2
                            else:
                                choose_option -= 1
                        if (event.key != K_RETURN and (event.unicode in self.ascii_letters)):
                            if (choose_option == 0 and len(login_text) <= 5):
                                login_text += event.unicode
                            else:
                                if (choose_option == 1 and len(password_text) <= 5):
                                    password_text += event.unicode
                    if (event.key == pygame.K_RETURN or event.key == K_TAB):
                        if (choose_option != 2):
                            choose_option += 1
                        else:
                            if event.key == K_TAB:
                                choose_option = 0
                            else:
                                usersList = []
                                with open("users.txt", encoding="utf8") as file:
                                    for i in file:
                                        i= i[:-1]
                                        l = i.split('\t')
                                        usersList.append((l[0], l[1]))
                                isInBase = False
                                for (n, h) in usersList:
                                    if (str(n), str(h)) == (str(login_text), str(password_text)):
                                        isInBase = True
                                        break
                                if isInBase:
                                    faze = 1
                                else:
                                    f = open("users.txt", 'a')
                                    f.write(login_text + "\t" + password_text+"\n")
                                    faze = 2
            pygame.display.update()
            self.mainClock.tick(60)

    def login_window(self):
        choose_option = 0
        running = True
        login_text = ""
        password_text = ""
        encrypted_text = "dasdasd"
        faze = 0
        while running:
            self.screen.fill((0, 0, 0))
            for i in range(len(self.colors)):
                if (i == choose_option):
                    self.colors[i] = self.green
                else:
                    self.colors[i] = self.dark_green
            encrypted_text = ""
            for i in range(len(password_text)):
                encrypted_text += "*"
            signIn_btn = pygame.Rect(350, self.SCY * 3 / 8 + 95, 500, 100)
            self.draw_text_center(login_text, self.font, self.colors[0], self.screen, self.SCX / 2 + 100, self.SCY * 3 / 8 + 150)
            self.draw_text_center("NAME: ", self.font, self.colors[0], self.screen, 200, self.SCY * 3 / 8 + 150)

            register_btn = pygame.Rect(350, self.SCY * 5 / 8 - 5, 500, 100)
            self.draw_text_center(encrypted_text, self.font, self.colors[1], self.screen, self.SCX / 2 + 100, self.SCY * 5 / 8 + 50)
            self.draw_text_center('PASS:', self.font, self.colors[1], self.screen, 195, self.SCY * 5 / 8 + 50)

            quit_btn = pygame.Rect(300, self.SCY * 7 / 8 - 105, 400, 100)
            self.draw_text_center('LOG IN', self.font, self.colors[2], self.screen, self.SCX / 2, self.SCY * 7 / 8 - 50)
            if (faze == 1):
                self.draw_text_center('SUCCEED', self.font, self.green, self.screen, self.SCX / 2,
                                      self.SCY * 1 / 8 + 50)
            if (faze == 2):
                self.draw_text_center('TRY AGAIN!', self.font, self.green, self.screen, self.SCX / 2,
                                      self.SCY * 1 / 8 + 50)
            pygame.draw.rect(self.screen, self.colors[0], signIn_btn, 2, 25)
            pygame.draw.rect(self.screen, self.colors[1], register_btn, 2, 25)
            pygame.draw.rect(self.screen, self.colors[2], quit_btn, 2, 25)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.main_menu()
                        choose_option = 0
                    if event.key == pygame.K_BACKSPACE:
                        if (choose_option == 0):
                            login_text = login_text[:-1]
                        else:
                            if (choose_option == 1):
                                password_text = password_text[:-1]
                    else:
                        if event.key == K_DOWN:
                            if (choose_option == 2):
                                choose_option = 0
                            else:
                                choose_option += 1
                        if event.key == K_UP:
                            if (choose_option == 0):
                                choose_option = 2
                            else:
                                choose_option -= 1
                        if (event.key != K_RETURN and (event.unicode in self.ascii_letters)):
                            if (choose_option == 0 and len(login_text) <= 5):
                                login_text += event.unicode
                            else:
                                if (choose_option == 1 and len(password_text) <= 5):
                                    password_text += event.unicode
                    if (event.key == pygame.K_RETURN or event.key == K_TAB):
                        if (choose_option != 2):
                            choose_option += 1
                        else:
                            if event.key == K_TAB:
                                choose_option = 0
                            else:
                                usersList = []
                                with open("users.txt", encoding="utf8") as file:
                                    for i in file:
                                        i = i[:-1]
                                        l = i.split('\t')
                                        usersList.append((l[0], l[1]))
                                isInBase = False
                                for (n, h) in usersList:
                                    if ((str(n), str(h)) == (str(login_text), str(password_text))):  # username
                                        isInBase = True
                                        break
                                if isInBase:
                                    faze = 1
                                    self.user = login_text
                                    self.game_menu()
                                else:
                                    faze = 2
            pygame.display.update()
            self.mainClock.tick(60)

    def menu_functions(self, option):
        if (option == 0):
            self.login_window()

    def draw_text_center(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def draw_text_left(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.midleft = (x, y)
        surface.blit(textobj, textrect)

    def draw_text_right(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.midright = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        choose_option = 0
        while True:
            self.screen.fill((0, 0, 0))
            self.draw_text_center('MENU', self.font, self.green, self.screen, self.SCX / 2, self.SCY / 4)

            for i in range(len(self.colors)):
                if (i == choose_option):
                    self.colors[i] = self.green
                else:
                    self.colors[i] = self.dark_green

            signIn_btn = pygame.Rect(300, self.SCY * 3 / 8 + 95, 400, 100)
            self.draw_text_center('LOGIN', self.font, self.colors[0], self.screen, self.SCX / 2, self.SCY * 3 / 8 + 150)

            register_btn = pygame.Rect(240, self.SCY * 5 / 8 - 5, 520, 100)
            self.draw_text_center('REGISTER', self.font, self.colors[1], self.screen, self.SCX / 2, self.SCY * 5 / 8 + 50)

            quit_btn = pygame.Rect(350, self.SCY * 7 / 8 - 105, 300, 100)
            self.draw_text_center('QUIT', self.font, self.colors[2], self.screen, self.SCX / 2, self.SCY * 7 / 8 - 50)

            pygame.draw.rect(self.screen, self.colors[0], signIn_btn, 2, 25)
            pygame.draw.rect(self.screen, self.colors[1], register_btn, 2, 25)
            pygame.draw.rect(self.screen, self.colors[2], quit_btn, 2, 25)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_DOWN:
                        if (choose_option == 2):
                            choose_option = 0
                        else:
                            choose_option += 1
                    if event.key == K_UP:
                        if (choose_option == 0):
                            choose_option = 2
                        else:
                            choose_option -= 1
                    if event.key == K_RETURN:
                        if (choose_option == 0):
                            self.login_window()
                        if (choose_option == 1):
                            self.register_window()
                        else:
                            pygame.quit()
                            sys.exit()
            pygame.display.update()
            self.mainClock.tick(60)

    def create_grid(self, locked_positions={}):
        grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_positions:
                    c = locked_positions[(j, i)]
                    grid[i][j] = c
        return grid

    def convert_shape_format(self, shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def valid_space(self, shape, grid):
        accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        formatted = self.convert_shape_format(shape)

        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def check_lost(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True

        return False

    def get_shape(self):

        return Piece(5, 0, random.choice(shapes))

    def draw_grid( self,surface, grid):
        sx = top_left_x
        sy = top_left_y

        for i in range(len(grid)):
            pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size),
                             (sx + play_width, sy + i * block_size))
            for j in range(len(grid[i])):
                pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                                 (sx + j * block_size, sy + play_height))

    def clear_rows(self, grid, locked):

        inc = 0
        for i in range(len(grid) - 1, -1, -1):
            row = grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j, i)]
                    except:
                        continue

        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)

        return inc

    def draw_next_shape(self, shape, surface):
        self.draw_text_center('Incomming', self.font_halfsize, self.colors[0], self.screen, self.SCX / 2 + 300, 450)
        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height / 2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color,
                                     (sx + j * block_size + 30, sy + i * block_size, block_size, block_size), 0)

    def max_score(self):
        with open("highscores.txt", encoding="utf8") as file:
            highscores = []
            for i in file:
                l = i.split('\t')
                highscores.append((l[0], l[1]))
        return highscores[0]

    def draw_window(self, grid, score=0, last_score=0):
        self.screen.fill((0, 0, 0))

        self.draw_text_center('TETRIS', self.font, self.green, self.screen, self.SCX / 2,  250)

        self.draw_text_left("SCORE: ", self.font_halfsize, self.colors[0], self.screen, 650, 50)
        self.draw_text_right(str(score), self.font_halfsize, self.colors[0], self.screen, self.SCX - 20, 50)

        self.draw_text_left("HIGH SCORE: ", self.font_halfsize, self.colors[0], self.screen, 50, 50)
        (_, sc) =self.max_score()
        self.draw_text_left(sc, self.font_halfsize, self.colors[0], self.screen, 400, 50)

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(self.screen, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

        pygame.draw.rect(self.screen, self.green, (top_left_x, top_left_y, play_width, play_height), 5)

        self.draw_grid(self.screen, grid)

    def game_restart(self):
        running = True
        self.finalscore = self.game_play()
        self.register_score(self.user, self.finalscore)
        while running:
            self.screen.fill((0, 0, 0))
            self.draw_text_center("YOU LOST", self.font_halfsize, self.colors[0], self.screen,
                                  self.SCX / 2, self.SCY / 2 - 50)
            self.draw_text_center("PRESS ANY KEY TO CONTINUE", self.font_halfsize, self.colors[0],
                                  self.screen, self.SCX / 2, self.SCY / 2 + 50)
            self.draw_text_center(str(self.finalscore), self.font_halfsize, self.colors[0],
                                  self.screen, self.SCX / 2, self.SCY / 2 + 150)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.game_menu()
                    else:
                        self.finalscore = self.game_play()
                        self.register_score(self.user ,self.finalscore)
            pygame.display.update()
            self.mainClock.tick(60)

    def register_score(self, username, u_score):
        with open("highscores.txt", encoding="utf8") as file:
            highscores = []
            for i in file:
                l = i.split('\t')
                highscores.append((l[0], l[1]))
            for i in range(len(highscores)):
                (name, score) = highscores[i]
                score = score[:-1]
                if int(score) <= u_score:
                    highscores.append(("temp", 0))
                    j = 10
                    while j>i:
                        highscores[j] = highscores[j-1]
                        j -=1
                    highscores[i] = (username, str(u_score)+"\n")
                    highscores= highscores[:-1]
                    break
            f = open("highscores.txt", 'w')
            for i in range(len(highscores)):
                (u, sc) = highscores[i]
                f.write(u + "\t" + str(sc))

    def leader_board(self):
        running = True
        gap = 70

        with open("highscores.txt", encoding="utf8") as file:
            highscores = []
            for i in file:
                l = i.split('\t')
                highscores.append((l[0], l[1]))
        while running:
            helping = 1
            self.screen.fill((0, 0, 0))
            self.draw_text_center("LEADER BOARD", self.font, self.green, self.screen,
                                  self.SCX / 2, 60)
            for (name, score) in highscores:
                txt = "{:>38}"
                self.draw_text_left(str(name), self.font_halfsize, self.green, self.screen, 60, 190 + gap * helping)
                self.draw_text_left(txt.format(str(score)), self.font_halfsize, self.green, self.screen, 250, 190 + gap * helping)
                helping += 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    running = False

            pygame.display.update()
            self.mainClock.tick(60)


game = TheGame()
game.main_menu()
