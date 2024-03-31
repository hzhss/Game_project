import os
import sys
import pygame

import Corgi
import dop_function
import Level

pygame.init()
size = width, height = 700, 700
screen = pygame.display.set_mode(size)
tile_width = tile_height = 50
fps = 60

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

dop_function.start_screen(screen)

tile_images = {
    'wall': dop_function.load_image('box.png'),
    'empty': dop_function.load_image('grass.png')
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.add(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)



if __name__ == '__main__':
    corgi = Corgi.Corgi(50, 50, all_sprites)
    corgi.add(player_group)
    left = right = False
    jump = False

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Tile('wall', event.pos[0], event.pos[1])
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                jump = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                right = True
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                jump = False
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left = False

        corgi.update(left, right, jump, tiles_group)
        clock.tick(24)
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
