import pygame
import random
from math import log2

pygame.init()

window_size = (595, 760)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Game "2048"')

screen.fill((220, 220, 195))

button1_font = pygame.font.SysFont('Verdana', 70)
button1_text_color = pygame.Color(70, 70, 70)
button1_color = pygame.Color(230, 130, 0)
button1_rect = pygame.Rect(50, 400, 500, 120)
button1_text1 = button1_font.render('Новая игра', True, button1_text_color)

font1 = pygame.font.Font(None, 55)
text1 = font1.render("Добро пожаловать в игру!", True, (125, 105, 105))
pygame.display.flip()

button_return_rect = pygame.Rect(370, 35, 160, 90)
font4 = pygame.font.Font(None, 55)
text4 = font4.render("НАЗАД", True, (90, 90, 90))
button_return_rect_center = text4.get_rect(center=button_return_rect.center)

game_list = [[0 for i in range(4)] for j in range(4)]
game_list_copy = [[0 for i in range(4)] for j in range(4)]
coordinate_x = [[0 for i in range(4)] for j in range(4)]
coordinate_y = [[0 for i in range(4)] for j in range(4)]
score = 0
square = 130
indent = 15
colors_back = [(120, 120, 125),
           (150, 150, 150),
           (140, 140, 110),
           (200, 160, 110),
           (180, 140, 90),
           (190, 130, 80),
           (205, 120, 75),
           (160, 160, 70),
           (175, 175, 65),
           (190, 190, 60),
           (200, 200, 55),
           (120, 120, 190)]
colors_num = [(70, 70, 70),
           (70, 70, 70),
           (70, 70, 70),
           (220, 220, 220),
           (220, 220, 220),
           (220, 220, 220),
           (220, 220, 220),
           (220, 220, 220),
           (220, 220, 220),
           (220, 220, 220),
           (220, 220, 220),
           (220, 220, 220)]
size_num = [120, 120, 120, 120, 100,
            100, 100, 85, 85, 85, 50, 50]

# Цикл игры
running = True
button1_pressed = False
show_text1 = True
generate_first_num = True

def draw_begin(score):
    global generate_first_num
    screen.fill((220, 220, 195))
    pygame.draw.rect(screen, (230, 130, 0), button_return_rect)
    screen.blit(text4, button_return_rect_center)
    for row in range(4):
        for col in range(4):
            x = indent + col * (square + indent)
            y = 180 + row * (square + indent)
            coordinate_x[row][col] = x + square // 2
            coordinate_y[row][col] = y + square // 2
            pygame.draw.rect(screen, colors_back[0], (x, y, square, square))
    font2 = pygame.font.Font(None, 70)
    text2 = font2.render("Счёт:", True, (125, 105, 105))
    screen.blit(text2, (30, 50))
    font3 = pygame.font.Font(None, 80)
    text3 = font3.render(str(score), True, (125, 105, 105))
    screen.blit(text3, (190, 50))
    if generate_first_num:
        generate_first_num = False
        num_x1 = random.randint(0, 3)
        num_y1 = random.randint(0, 3)
        num_x2 = random.randint(0, 3)
        num_y2 = random.randint(0, 3)
        while num_x2 == num_x1 and num_y2 == num_y1:
            num_x2 = random.randint(0, 3)
            num_y2 = random.randint(0, 3)
        game_list[num_y1][num_x1] = 2
        game_list[num_y2][num_x2] = 2
        game_list_copy[num_y1][num_x1] = 2
        game_list_copy[num_y2][num_x2] = 2
def find_num():
    new_x = -1
    new_y = -1
    count = 0
    while new_x == -1 and new_y == -1 and count < 500:
        num_x = random.randint(0, 3)
        num_y = random.randint(0, 3)
        count += 1
        if game_list[num_y][num_x] == 0:
            new_x = num_x
            new_y = num_y
            chek1 = random.randint(1, 10)
            if chek1 == 10:
                game_list[new_y][new_x] = 4
            else:
                game_list[new_y][new_x] = 2
def updating_table():
    for row in range(4):
        for col in range(4):
            if game_list[row][col] != 0:
                x = coordinate_x[row][col] - square // 2
                y = coordinate_y[row][col] - square // 2
                pygame.draw.rect(screen, colors_back[int(log2(game_list[row][col]))], (x, y, square, square))
                font = pygame.font.Font(None, size_num[int(log2(game_list[row][col]))])
                text = font.render(str(game_list[row][col]), True, colors_num[int(log2(game_list[row][col]))])
                text_rect = text.get_rect(center=(coordinate_x[row][col], coordinate_y[row][col]))
                screen.blit(text, text_rect)
def updating_score():
    font3 = pygame.font.Font(None, 70)
    text3 = font3.render(str(score), True, (125, 105, 105))
    screen.blit(text3, (190, 50))

def func_up():
    global change
    global score
    for j in range(4):
        for i in range(4):
            game_list_copy[i][j] = game_list[i][j]
            if game_list[i][j] != 0:
                p = 0
                while p < i and game_list[p][j] != 0:
                    p += 1
                if p < i:
                    game_list[p][j] = game_list[i][j]
                    game_list[i][j] = 0
                    change = True
    for j in range(4):
        i = 1
        while i < 4 and game_list[i][j] != 0:
            if game_list[i][j] == game_list[i-1][j]:
                score += game_list[i][j] * 2
                game_list[i-1][j] *= 2
                game_list[i][j] = 0
                change = True
                for k in range(i+1, 4):
                    game_list[k-1][j] = game_list[k][j]
                    game_list[k][j] = 0
            i += 1

def func_down():
    global change
    global score
    for j in range(4):
        for i in range(3, -1, -1):
            game_list_copy[i][j] = game_list[i][j]
            if game_list[i][j] != 0:
                p = 3
                while p > i and game_list[p][j] != 0:
                    p -= 1
                if p > i:
                    game_list[p][j] = game_list[i][j]
                    game_list[i][j] = 0
                    change = True
    for j in range(4):
        i = 2
        while i > -1 and game_list[i][j] != 0:
            if game_list[i][j] == game_list[i+1][j]:
                score += game_list[i][j] * 2
                game_list[i+1][j] *= 2
                game_list[i][j] = 0
                change = True
                for k in range(i-1, -1, -1):
                    game_list[k+1][j] = game_list[k][j]
                    game_list[k][j] = 0
            i -= 1

def func_left():
    global change
    global score
    for i in range(4):
        for j in range(4):
            game_list_copy[i][j] = game_list[i][j]
            if game_list[i][j] != 0:
                p = 0
                while p < j and game_list[i][p] != 0:
                    p += 1
                if p < j:
                    game_list[i][p] = game_list[i][j]
                    game_list[i][j] = 0
                    change = True
    for i in range(4):
        j = 1
        while j < 4 and game_list[i][j] != 0:
            if game_list[i][j] == game_list[i][j-1]:
                score += game_list[i][j] * 2
                game_list[i][j-1] *= 2
                game_list[i][j] = 0
                change = True
                for k in range(j+1, 4):
                    game_list[i][k-1] = game_list[i][k]
                    game_list[i][k] = 0
            j += 1

def func_right():
    global change
    global score
    for i in range(4):
        for j in range(3, -1, -1):
            game_list_copy[i][j] = game_list[i][j]
            if game_list[i][j] != 0:
                p = 3
                while p > j and game_list[i][p] != 0:
                    p -= 1
                if p > j:
                    game_list[i][p] = game_list[i][j]
                    game_list[i][j] = 0
                    change = True
    for i in range(4):
        j = 2
        while j > -1 and game_list[i][j] != 0:
            if game_list[i][j] == game_list[i][j+1]:
                score += game_list[i][j] * 2
                game_list[i][j+1] *= 2
                game_list[i][j] = 0
                change = True
                for k in range(j-1, -1, -1):
                    game_list[i][k+1] = game_list[i][k]
                    game_list[i][k] = 0
            j -= 1

def chek_defeat():
    numbers = 0
    chek2 = True
    for row in range(4):
        for col in range(4):
            if game_list[row][col] != 0:
                numbers += 1
                if row - 1 > 0:
                    if game_list[row - 1][col] == game_list[row][col]:
                        chek2 = False
                if row + 1 < 4:
                    if game_list[row + 1][col] == game_list[row][col]:
                        chek2 = False
                if col - 1 > 0:
                    if game_list[row][col - 1] == game_list[row][col]:
                        chek2 = False
                if col + 1 < 4:
                    if game_list[row][col + 1] == game_list[row][col]:
                        chek2 = False
    if numbers != 16:
        chek2 = False
    return chek2

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button1_rect.collidepoint(event.pos):
                show_text1 = False
            if button_return_rect.collidepoint(event.pos) and not(chek_defeat()):
                for i in range(4):
                    for j in range(4):
                        game_list[i][j] = game_list_copy[i][j]
        if show_text1:
            pygame.draw.rect(screen, button1_color, button1_rect)
            button_rect_center = button1_text1.get_rect(center=button1_rect.center)
            screen.blit(button1_text1, button_rect_center)
            screen.blit(text1, (50, 200))
        else:
            draw_begin(score)
        if event.type == pygame.KEYDOWN:
            x = 0
            y = 0
            change = False
            if event.key == pygame.K_UP:
                func_up()
            if event.key == pygame.K_DOWN:
                func_down()
            if event.key == pygame.K_RIGHT:
                func_right()
            if event.key == pygame.K_LEFT:
                func_left()
            if change:
                find_num()
            for i in range(4):
                print(*game_list[i])
            print()
        updating_table()
        if chek_defeat():
            defeat_rect = pygame.Rect(5, 350, 585, 120)
            pygame.draw.rect(screen, (90, 90, 90), defeat_rect)
            font3 = pygame.font.Font(None, 127)
            text3 = font3.render("ПОРАЖЕНИЕ", True, (180, 30, 30))
            defeat_rect_center = text3.get_rect(center=defeat_rect.center)
            screen.blit(text3, defeat_rect_center)
        pygame.display.update()

pygame.quit()

