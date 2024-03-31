import pygame
from dop_function import *


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bonus_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
traps_group = pygame.sprite.Group()
health = pygame.sprite.Group()
sprite_name = {'stay': 10,
               'run': 10,
               'jump': 11,
               'fall': 11,
               'Lstay': 10,
               'Lrun': 10,
               'Ljump': 11,
               'Lfall': 11,
               'turbo': 8,
               'Lturbo': 8,
               'ouch': 10,
               'Louch': 10,
               'hurt': 8,
               'Lhurt': 8}
corgi_size = (100, 100)  # размеры спрайта корги
move = 10


class Corgi(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(player_group)
        self.Vx = 0  # скорость перемещения по оси x
        self.Vy = 0  # скорость перемещения по оси y
        self.x0 = x  # Начальная позиция
        self.y0 = y  # Начальная позиция
        self.a = 0.3  # Ускорение
        self.onGround = False
        self.rect = pygame.Rect(x, y, 90, 100)
        self.point = 0
        self.health = 10
        self.DAMAGE = False

        self.LEFT = False  # показатель того, куда направлен спрайт
        self.RIGHT = True
        # Анимация:
        self.frames = dict()
        for name, num in sprite_name.items():
            motion_frames = list()
            for j in range(1, num + 1):
                motion_frames.append(pygame.transform.smoothscale(load_image(f'corgi_sprites\{name}_{j}.png'), corgi_size))
            self.frames[name] = motion_frames[:]
        self.count = 0
        self.cur_frame = 0  # текущий фрейм
        self.image = self.frames['stay'][self.cur_frame]

    def update(self, left, right, jump, turbo, tiles):
        if jump:
            if self.onGround:  # когда стоим на земле
                # self.Vy = -12.245
                self.Vy = -12.25


        if left:
            self.LEFT, self.RIGHT = True, False
            self.Vx = -10  # скорость влево
            self.cur_frame = ((self.cur_frame + 1) % (2 * len(self.frames['Lrun'])))
            self.image = self.frames['Lrun'][self.cur_frame // 2]

        if right:
            self.LEFT, self.RIGHT = False, True
            self.Vx = 10  # скорость вправо
            self.cur_frame = ((self.cur_frame + 1) % (2 * len(self.frames['run'])))
            self.image = self.frames['run'][self.cur_frame // 2]

        if not(left or right):  # стоим, когда нет указаний идти
            self.Vx = 0
            if self.onGround:
                if self.RIGHT:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames['stay'])
                    self.image = self.frames['stay'][self.cur_frame]
                if self.LEFT:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames['Lstay'])
                    self.image = self.frames['Lstay'][self.cur_frame]

        if not self.onGround:
            self.Vy += self.a
            if abs(self.Vy) > 0.7:
                if self.RIGHT and self.Vy < 0:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames['jump'])
                    self.image = self.frames['jump'][self.cur_frame]
                elif self.LEFT and self.Vy < 0:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames['Ljump'])
                    self.image = self.frames['Ljump'][self.cur_frame]
                if self.RIGHT and self.Vy > 0:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames['fall'])
                    self.image = self.frames['fall'][self.cur_frame]
                elif self.LEFT and self.Vy > 0:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames['Lfall'])
                    self.image = self.frames['Lfall'][self.cur_frame]

        if self.DAMAGE:
            if self.health > 4:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames['ouch'])
                if self.RIGHT:
                    self.image = self.frames['ouch'][self.cur_frame]
                if self.LEFT:
                    self.image = self.frames['Louch'][self.cur_frame]
            else:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames['hurt'])
                if self.RIGHT:
                    self.image = self.frames['hurt'][self.cur_frame]
                if self.LEFT:
                    self.image = self.frames['Lhurt'][self.cur_frame]
            if self.count == 3 * len(self.frames['ouch']) - 1:
                self.DAMAGE = False
                self.health -= 1
            self.count = (self.count + 1) % (3 * len(self.frames['ouch']))

        if turbo:
            if self.RIGHT:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames['turbo'])
                self.image = self.frames['turbo'][self.cur_frame]
                self.Vx = 20
            elif self.LEFT:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames['Lturbo'])
                self.image = self.frames['Lturbo'][self.cur_frame]
                self.Vx = -20

        self.onGround = False
        self.rect.y += self.Vy
        self.collide(0, self.Vy, tiles)

        self.rect.x += self.Vx
        self.collide(self.Vx, 0, tiles)
        self.star_collide()
        self.coin_collide()
        self.traps_collide()

    def collide(self, vx, vy, tiles):
        for tile in tiles:
            if pygame.sprite.collide_rect(self, tile):  # если есть пересечение платформы с игроком
                if vx > 0:  # если движется вправо
                    self.rect.right = tile.rect.left  # то не движется вправо

                if vx < 0:  # если движется влево
                    self.rect.left = tile.rect.right  # то не движется влево

                if vy > 0:  # если падает вниз
                    self.rect.bottom = tile.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.Vy = 0  # и энергия падения пропадает

                if vy < 0:  # если движется вверх
                    self.rect.top = tile.rect.bottom  # то не движется вверх
                    self.Vy = 0  # и энергия прыжка пропадает

    def star_collide(self):
        for star in star_group:
            if pygame.sprite.collide_rect(self, star):  # если есть пересечение звездочки с игроком
                star.kill()
                self.point += 5000

    def coin_collide(self):
        for coin in coin_group:
            if pygame.sprite.collide_rect(self, coin):  # если есть пересечение монетки с игроком
                coin.kill()
                self.point += 50

    def traps_collide(self):
        for trap in traps_group:
            if pygame.sprite.collide_rect(self, trap):  # если есть пересечение ловушки с игроком
                self.DAMAGE = True




