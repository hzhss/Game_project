import os
import sys
import pygame
import Button


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    intro_text = ["КОРГИ КОРГИ КОРГИ", "",
                  "СОБЕРИ ВСЕ ЗВЕЗДОЧКИ",
                  "И ПОБЕДИШЬ",
                  "Правила игры:",
                  "Герой двигается с помощью стрелочек",
                  "Нажми пробел и ускоришься",
                  "Опасайся ловушек!!"]

    fon = pygame.transform.scale(load_image('Заставка_фиолетовый_корги_1.jpg'), (screen.get_size()))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    start_button = Button.StartButton(screen.get_size()[0] - 250 , 100, 196, 84, '', 'Play_but.png', 'Hover_play_but.png')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
                terminate()
            if start_button.handle_event(event):
                return
        start_button.check_hover(pygame.mouse.get_pos())
        start_button.draw(screen)
        pygame.display.flip()


def show_end_screen(screen, game_over):
    if game_over:
        fon = pygame.transform.scale(load_image('game_over_2.jpg'), (screen.get_size()))
        res_next_button = Button.StartButton(screen.get_size()[0] // 2 - 84 // 2, screen.get_size()[1] - 100, 84, 84,
                                             '', 'restart.png', 'Hover_restart.png')
        screen.blit(fon, (0, 0))

    else:
        intro_text = ["Вы прошли 1 уровень", "",
                      "Перейти на уровень 2"]
        font = pygame.font.Font(None, 30)
        text_coord = 50
        fon = pygame.transform.scale(load_image('level_completed.jpg'), (round(screen.get_size()[0] * 1.4),
                                                                         round(screen.get_size()[1] * 1.4)))
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord + 10
            intro_rect.move(100, screen.get_size()[1] // 2 - 100)
            text_coord += intro_rect.height
            screen.blit(fon, (0, 0))
            screen.blit(string_rendered, intro_rect)

        res_next_button = Button.StartButton(50, 150, 84, 84, '',
                                             'next_level.png', 'Hover_next_lev.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
                terminate()
            if res_next_button.handle_event(event):
                return False

        res_next_button.check_hover(pygame.mouse.get_pos())
        res_next_button.draw(screen)
        pygame.display.flip()


def show_win_screen(screen, point):
    fon = pygame.transform.scale(load_image('win_screen.jpg'), (screen.get_size()))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    score = font.render(f"Your score: {point}", True, (100, 255, 100))
    text_x = screen.get_size()[0] // 2 - score.get_width() // 2
    text_y = screen.get_size()[1] - 100
    text_w = score.get_width()
    text_h = score.get_height()
    screen.blit(score, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
                terminate()

        pygame.display.flip()
