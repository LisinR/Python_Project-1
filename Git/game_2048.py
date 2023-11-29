import pygame
import random
from math import log2
from constants import *
from Button import Button
from Button import Text
class App():
    def __init__(self):
        pygame.display.set_caption('Game "2048"')
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.button_begin = Button(X1, Y1, WIDTH1, HEIGHT1, TEXT1, COLOR1, TEXT_COLOR1, FONT_SIZE1)
        self.button_back = Button(X2, Y2, WIDTH2, HEIGHT2, TEXT2, COLOR2, TEXT_COLOR2, FONT_SIZE2)
        self.button_end = Button(X3, Y3, WIDTH3, HEIGHT3, TEXT3, COLOR3, TEXT_COLOR3, FONT_SIZE3)
        self.button_begin2 = Button(X4, Y4, WIDTH4, HEIGHT4, TEXT4, COLOR4, TEXT_COLOR4, FONT_SIZE4)
        self.button_end2 = Button(X5, Y5, WIDTH5, HEIGHT5, TEXT5, COLOR5, TEXT_COLOR5, FONT_SIZE5)
        self.game_list = [[0 for i in range(SIZE)] for j in range(SIZE)]
        self.game_list_copy = [[0 for i in range(SIZE)] for j in range(SIZE)]
        self.coordinate_x = [[0 for i in range(SIZE)] for j in range(SIZE)]
        self.coordinate_y = [[0 for i in range(SIZE)] for j in range(SIZE)]
        self.score = 0
        self.score_copy = 0
        self.running = True
        self.show_begin = True
        self.generate_numbers = True
        self.change = False

    def draw_begin_screen(self):
        self.screen.fill(COLOR_BEGIN)
        self.button_begin.draw(self.screen)
        self.button_end.draw(self.screen)
        title = Text(FONT_SIZE_TITLE, TEXT_TITLE, TEXT_COLOR_TITLE, DEST_TITLE)
        title.draw(self.screen)

    def generate_first_numbers(self):
        self.generate_numbers = False
        num_x1 = random.randint(0, SIZE-1)
        num_y1 = random.randint(0, SIZE-1)
        num_x2 = random.randint(0, SIZE-1)
        num_y2 = random.randint(0, SIZE-1)
        while (num_x2 == num_x1) and (num_y2 == num_y1):
            num_x2 = random.randint(0, SIZE-1)
            num_y2 = random.randint(0, SIZE-1)
        self.game_list[num_y1][num_x1] = 2
        self.game_list[num_y2][num_x2] = 2
        self.game_list_copy[num_y1][num_x1] = 2
        self.game_list_copy[num_y2][num_x2] = 2

    def draw_game(self):
        self.screen.fill(COLOR_BEGIN)
        self.button_back.draw(self.screen)
        score = Text(FONT_SIZE_SCORE, TEXT_SCORE, TEXT_COLOR_SCORE, DEST_SCORE)
        score.draw(self.screen)

        for row in range(SIZE):
            for col in range(SIZE):
                x = INDENT + col * (SQUARE + INDENT)
                y = BEGIN_Y + row * (SQUARE + INDENT)
                self.coordinate_x[row][col] = x + SQUARE // 2
                self.coordinate_y[row][col] = y + SQUARE // 2
                pygame.draw.rect(self.screen, colors_back[0], (x, y, SQUARE, SQUARE))

        score2 = Text(FONT_SIZE_SCORE2, str(self.score), TEXT_COLOR_SCORE2, DEST_SCORE2)
        score2.draw(self.screen)
        if self.generate_numbers:
            self.generate_first_numbers()

    def find_number(self):
        new_x = -1
        new_y = -1
        count = 0
        while new_x == -1 and new_y == -1 and count < 500:
            num_x = random.randint(0, SIZE-1)
            num_y = random.randint(0, SIZE-1)
            count += 1
            if self.game_list[num_y][num_x] == 0:
                new_x = num_x
                new_y = num_y
                check_number = random.randint(1, 10)
                if check_number == 10:
                    self.game_list[new_y][new_x] = 4
                else:
                    self.game_list[new_y][new_x] = 2

    def updating_table(self):
        for row in range(SIZE):
            for col in range(SIZE):
                if self.game_list[row][col] != 0:
                    x = self.coordinate_x[row][col] - SQUARE // 2
                    y = self.coordinate_y[row][col] - SQUARE // 2
                    pygame.draw.rect(self.screen, colors_back[int(log2(self.game_list[row][col]))], (x, y, SQUARE, SQUARE))
                    font = pygame.font.Font(None, size_num[int(log2(self.game_list[row][col]))])
                    text = font.render(str(self.game_list[row][col]), True, colors_num[int(log2(self.game_list[row][col]))])
                    text_rect = text.get_rect(center=(self.coordinate_x[row][col], self.coordinate_y[row][col]))
                    self.screen.blit(text, text_rect)

    def updating_score(self):
        score2 = Text(FONT_SIZE_SCORE2, str(self.score), TEXT_COLOR_SCORE2, DEST_SCORE2)
        score2.draw(self.screen)

    def check_defeat(self):
        amount = 0
        check = True
        for row in range(SIZE):
            for col in range(SIZE):
                if self.game_list[row][col] != 0:
                    amount += 1
                    if row - 1 > 0:
                        if self.game_list[row - 1][col] == self.game_list[row][col]:
                            check = False
                    if row + 1 < SIZE:
                        if self.game_list[row + 1][col] == self.game_list[row][col]:
                            check = False
                    if col - 1 > 0:
                        if self.game_list[row][col - 1] == self.game_list[row][col]:
                            check = False
                    if col + 1 < SIZE:
                        if self.game_list[row][col + 1] == self.game_list[row][col]:
                            check = False
        if amount != SIZE*SIZE:
            check = False
        return check

    def copy_game_list(self):
        self.score_copy = self.score
        for j in range(SIZE):
            for i in range(SIZE):
                self.game_list_copy[i][j] = self.game_list[i][j]

    def shift(self, array):
        for i in range(SIZE):
            if array[i] != 0:
                p = 0
                while p < i and array[p] != 0:
                    p += 1
                if p < i:
                    array[p] = array[i]
                    array[i] = 0
                    self.change = True
    def merge(self, array):
        i = 1
        while i < SIZE and array[i] != 0:
            if array[i] == array[i-1]:
                self.score += array[i] * 2
                array[i-1] *= 2
                array[i] = 0
                self.change = True
                for k in range(i + 1, SIZE):
                    array[k-1] = array[k]
                    array[k] = 0
            i += 1

    def move(self, direction):
        if direction == "up":
            for j in range(SIZE):
                array = [0] * SIZE
                for i in range(SIZE):
                    array[i] = self.game_list[i][j]
                self.shift(array)
                self.merge(array)
                for i in range(SIZE):
                    self.game_list[i][j] = array[i]
        if direction == "down":
            for j in range(SIZE):
                array = [0] * SIZE
                for i in range(SIZE):
                    array[SIZE-i-1] = self.game_list[i][j]
                self.shift(array)
                self.merge(array)
                for i in range(SIZE):
                    self.game_list[i][j] = array[SIZE-i-1]
        if direction == "left":
            for i in range(SIZE):
                array = self.game_list[i]
                self.shift(array)
                self.merge(array)
                self.game_list[i] = array
        if direction == "right":
            for i in range(SIZE):
                array = self.game_list[i][::-1]
                self.shift(array)
                self.merge(array)
                self.game_list[i] = array[::-1]

    def exit(self):
        self.game_list = [[0 for i in range(SIZE)] for j in range(SIZE)]
        self.game_list_copy = [[0 for i in range(SIZE)] for j in range(SIZE)]
        self.score = 0
        self.score_copy = 0
        self.generate_numbers = True

    def handle_begin(self, event):
        self.draw_begin_screen()
        if self.button_end.check_click(event):
            self.running = False
        if self.button_begin.check_click(event):
            self.show_begin = False
        pygame.display.update()

    def handle_game(self, event):
        if self.button_back.check_click(event) and not (self.check_defeat()):
            self.score = self.score_copy
            for i in range(SIZE):
                for j in range(SIZE):
                    self.game_list[i][j] = self.game_list_copy[i][j]
        self.draw_game()
        self.handle_events(event)
        self.updating_table()
        if self.check_defeat():
            self.handle_defeat(event)
        pygame.display.update()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.change = False
            if event.key == pygame.K_UP:
                self.copy_game_list()
                self.move("up")
            if event.key == pygame.K_DOWN:
                self.copy_game_list()
                self.move("down")
            if event.key == pygame.K_RIGHT:
                self.copy_game_list()
                self.move("right")
            if event.key == pygame.K_LEFT:
                self.copy_game_list()
                self.move("left")
            if self.change:
                self.find_number()

    def handle_defeat(self, event):
        x = DEST_END_X
        y = DEST_END_Y
        for step in range(7):
            end = Text(FONT_SIZE_END, TEXT_END, TEXT_COLOR_END, (x, y))
            end.draw(self.screen)
            x -= 1
            y += 1
        end = Text(FONT_SIZE_END, TEXT_END,
                   (TEXT_COLOR_END[0] - 15, TEXT_COLOR_END[1] - 15, TEXT_COLOR_END[2] - 15), (x, y))
        end.draw(self.screen)
        self.button_begin2.draw(self.screen)
        self.button_end2.draw(self.screen)
        if self.button_begin2.check_click(event):
            self.exit()
            self.draw_game()
            self.updating_table()
            self.show_begin = False
        if self.button_end2.check_click(event):
            self.exit()
            self.draw_begin_screen()
            self.show_begin = True

    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.show_begin:
                    self.handle_begin(event)
                else:
                    self.handle_game(event)

pygame.init()
game = App()
game.main()
pygame.quit()






