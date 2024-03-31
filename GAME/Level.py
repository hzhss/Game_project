import pygame
import dop_function
import Corgi


pygame.init()
pygame.display.set_caption("КОРГИ КОРГИ КОРГИ")
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
tile_width = tile_height = 50
tiles_group = pygame.sprite.Group()
bonus_group = Corgi.bonus_group
coin_group = Corgi.coin_group
star_group = Corgi.star_group
traps = Corgi.traps_group
all_sprites = Corgi.all_sprites
heart_pos = [(0, 0), (50, 0), (100, 0), (150, 0), (200, 0),
             (250, 0), (300, 0), (350, 0), (400, 0), (450, 0), (500, 0)]

fon = dop_function.load_image('fon.jpg')

tile_images = {
    'earth_2_right': dop_function.load_image('earth_2_r.png'),
    'earth_2_left': dop_function.load_image('earth_2_l.png'),
    'earth_dop': dop_function.load_image('earth_dop.png'),
    'earth_2': dop_function.load_image('earth_2(ver2).png'),
    'earth': dop_function.load_image('earth.png'),
    'wall': dop_function.load_image('box.png')
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.add(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)


spike_image = {
    'spike_right': dop_function.load_image('spike_2_r.png'),
    'spike_left': dop_function.load_image('spike_2_l.png'),
    'spike': dop_function.load_image('spike_2.png')
}


class Spikes(pygame.sprite.Sprite):
    def __init__(self, spike_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.add(traps, all_sprites)
        self.image = spike_image[spike_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Star(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.add(bonus_group, star_group, all_sprites)
        self.image = pygame.transform.smoothscale(dop_function.load_image('star.png'), (200, 200))
        self.rect = self.image.get_rect().move(pos_x + tile_width/2 - 10, pos_y + tile_width/2 - 10)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '^':
                Spikes('spike', x * tile_width, y * tile_width + tile_height - 30)
            if level[y][x] == '>':
                Spikes('spike_right', x * tile_width, y * tile_width)
            if level[y][x] == '<':
                Spikes('spike_left', x * tile_width + 20, y * tile_width)
            if level[y][x] == '*':
                Star(x * tile_width, y * tile_width)
            elif level[y][x] == 'o':
                Coin(x * tile_width, y * tile_width)
            elif level[y][x] == '#':
                Tile('earth_2', x * tile_width, y * tile_width)
            elif level[y][x] == 'L':
                Tile('earth_2_left', x * tile_width, y * tile_width)
            elif level[y][x] == 'R':
                Tile('earth_2_right', x * tile_width, y * tile_width)
            elif level[y][x] == '~':
                Tile('earth_dop', x * tile_width, y * tile_width)
            elif level[y][x] == '@':
                new_player = Corgi.Corgi(x * tile_width, y * tile_width)
    for pos in heart_pos[:5]:
        Health(pos[0], pos[1])
    return new_player


def Score(point, hp):
    font = pygame.font.Font(None, 50)
    score = font.render(f"Score: {point}", True, (100, 255, 100))
    health_text = font.render(f"Hp: {hp}", True, (100, 255, 100))
    text_x = width // 2 - score.get_width() // 2
    text_y = 10
    text_w = score.get_width()
    text_h = score.get_height()
    screen.blit(score, (text_x, text_y))
    screen.blit(health_text, (20, 100))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)
    if len(Corgi.health) != hp:
        if Corgi.health:
            for heart in Corgi.health:
                heart.kill()
        for pos in range(hp):
            Health(heart_pos[pos][0], heart_pos[pos][1])


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.add(coin_group, bonus_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.coin_size = [(44, 44), (40, 44), (20, 44), (7, 44), (20, 44), (40, 44)]
        self.frames = [pygame.transform.smoothscale(dop_function.load_image(f'coin_{i}.png'), siz)
                       for i, siz in enumerate(self.coin_size)]

        self.cur_frame = 0  # текущий фрейм
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x + tile_width/2 - self.coin_size[self.cur_frame][0] // 2,
                            pos_y + tile_width/2 - self.coin_size[self.cur_frame][1] // 2)

    # Анимация монетки
    def coin_update(self):
        new_cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.rect.centerx = (self.rect.centerx + self.coin_size[self.cur_frame][0] // 2
                             - self.coin_size[new_cur_frame][0] // 2)

        self.rect.centery = (self.rect.centery + self.coin_size[self.cur_frame][1] // 2
                             - self.coin_size[new_cur_frame][1] // 2)
        self.cur_frame = new_cur_frame
        self.image = self.frames[self.cur_frame]


class Health(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(Corgi.health)
        self.add(Corgi.health)
        self.image = dop_function.load_image('heart.png')
        self.rect = self.image.get_rect().move(pos_x, pos_y)


