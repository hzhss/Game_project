import os
import sys
import pygame

import Corgi
import dop_function
import Level


size = width, height = Level.size
screen = Level.screen
tile_width = tile_height = Level.tile_width
fps = 60
fon = Level.fon

# группы спрайтов
all_sprites = Corgi.all_sprites
tiles_group = Level.tiles_group
player_group = Corgi.player_group

dop_function.start_screen(screen)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


if __name__ == '__main__':

    pygame.mixer.music.load('data/sounds/barradeen-boku-no-love.mp3')
    pygame.mixer.music.play(-1)
    corgi = Level.generate_level(Level.load_level('level1.txt'))
    left = right = False
    jump = False
    turbo = False
    running = True
    game_over = False
    level_completed = False
    level_2_completed = False
    level_2 = False
    camera = Camera()
    clock = pygame.time.Clock()
    count = 0
    # Цикл игры
    while running:

        if (game_over or level_completed) and not level_2:
            running = False
            game_over = dop_function.show_end_screen(screen, game_over)

            if not game_over:
                for sprite in all_sprites:
                    sprite.kill()
                pygame.mixer.music.play(-1)
                if not level_completed:
                    corgi = Level.generate_level(Level.load_level('level1.txt'))
                else:
                    corgi = Level.generate_level(Level.load_level('level2.txt'))
                    level_completed = False
                    level_2 = True
                left = right = False
                jump = False
                turbo = False
                running = True

        if level_2 and game_over:
            running = False
            game_over = dop_function.show_end_screen(screen, game_over)
            if not game_over:
                for sprite in all_sprites:
                    sprite.kill()
                pygame.mixer.music.play(-1)
                corgi = Level.generate_level(Level.load_level('level2.txt'))
                level_completed = False
                level_2 = True
                left = right = False
                jump = False
                turbo = False
                running = True

        if level_2_completed:
            dop_function.show_win_screen(screen, corgi.point)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                jump = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                right = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                turbo = True
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                jump = False
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left = False
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                turbo = False

        # изменяем ракурс камеры
        camera.update(corgi)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        if count == 2:
            for coin in Level.coin_group:
                coin.coin_update()
        corgi.update(left, right, jump, turbo, tiles_group)
        if corgi.health == 0:
            game_over = True
        count = (count + 1) % 3
        clock.tick(30)
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))

        tiles_group.draw(screen)
        Level.traps.draw(screen)
        player_group.draw(screen)
        Level.bonus_group.draw(screen)
        Corgi.health.draw(screen)
        Level.Score(corgi.point, corgi.health)

        # если уровень_1 пройден и все сердечки собраны
        if level_2 and not Level.star_group:
            level_2_completed = True

        # если все сердечки собраны
        if not Level.star_group:
            level_completed = True
        pygame.display.flip()
