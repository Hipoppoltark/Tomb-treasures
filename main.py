import pygame
import sys
import os
import random
from math import fabs
from config import *


pygame.init()
screen = pygame.display.set_mode((CAM_X * tile_width, CAM_Y * tile_height))


def setle(x, s=True):
    if s:
        return int((x * tile_width) / 50)
    return int((x * tile_height) / 50)


def load_image(name, color_key=None, format="jpg"):
    fullname = os.path.join('img', name)
    image = pygame.image.load(fullname)
    if format != "png":
        image = image.convert()
    if color_key is not None and format != "png":
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    elif format == "png":
        image = image.convert_alpha()
    return pygame.transform.scale(image, (setle(image.get_width(), 1),
                                          setle(image.get_height(), 0)))


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    key_coors = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                Tile(random.choice(['cactus', 'tumbleweed']), x, y)
            elif level[y][x] == 's':
                InteractionObjects("sand", "shovel", x, y)
                key_coors.append((x, y))
            elif level[y][x] == 't':
                Things('shovel', x, y)
            elif level[y][x] == 'c':
                InteractionObjects('chest', 'key', x, y)
            elif level[y][x] == '_':
                Tile('invisible', x, y)
            elif level[y][x] == '@':
                new_player = Hero(x, y)
    key_coors = random.choice(key_coors)
    # вернем игрока, а также размер поля в клетках
    return new_player, x + 1, y + 1, key_coors


class TombWall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("wall.png")
        self.rect = self.image.get_rect()
        self.type = "wall"
        self.image_entry = load_image("entry.png")
        self.rect_entry = self.image_entry.get_rect()
        self.pos_x = self.pos_y = 0


class Entry(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("entry.png")
        self.rect = self.image.get_rect()
        self.rect.x = setle(380, 1)
        self.rect.y = 16
        self.type = "entry"
        self.pos_x = self.rect.x // tile_width
        self.pos_y = self.rect.y / tile_height


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("background.jpg")
        self.rect = self.image.get_rect()
        self.rect.y = setle(185, 0)
        self.type = "background"
        self.pos_x = self.rect.x // tile_width
        self.pos_y = self.rect.y // tile_height


class Hero(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = load_image("hero.png", format="png")
        self.rect = self.image.get_rect().move(
            CELL_SIZE * pos_x, margin + CELL_SIZE * pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.type = "hero"
        self.update_rect()

    def update_rect(self):
        self.rect.topleft = (
            tile_width * self.pos_x + (tile_width - self.rect.width) // 2,
            margin + tile_height * self.pos_y + (tile_height - self.rect.height) // 2
        )

    def update(self, events):
        new_pos_x = self.pos_x
        new_pos_y = self.pos_y
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    new_pos_y -= 1
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    new_pos_y += 1
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    new_pos_x -= 1
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    new_pos_x += 1
        ok = True
        if new_pos_x >= level_x or new_pos_y >= level_y or new_pos_x < 0 or new_pos_y < 0:
            ok = False
        new_pos_x %= level_x
        new_pos_y %= level_y
        if level[new_pos_y][new_pos_x] in ['.', '@'] and ok:
            self.pos_x = new_pos_x
            self.pos_y = new_pos_y
            self.update_rect()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.type = tile_type
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.update_rect()

    def update_rect(self):
        self.rect.topleft = (
            tile_width * self.pos_x + (tile_width - self.rect.width) // 2,
            margin + tile_height * self.pos_y + (tile_height - self.rect.height) // 2)


class Inventory(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(inventory_group)
        self.image = pygame.Surface((175, 70), pygame.SRCALPHA, 32)
        self.content = []
        self.image.fill(pygame.Color(188, 209, 50, 0))
        self.font = pygame.font.Font("fonts/konstanting.ttf", 28)
        text = self.font.render("инвентарь", True, (250, 232, 142))
        text_x = 3
        text_y = 0
        self.image.blit(text, (text_x, text_y))
        for i in range(4):
            pygame.draw.rect(self.image, (184, 165, 73), (3 + 43 * i, 28, 40, 40))
            pygame.draw.rect(self.image, (133, 123, 76), (3 + 43 * i, 28, 40, 40), 2)
        self.rect = self.image.get_rect()
        self.rect.x = 15
        self.rect.y = 0

    def add_thing(self, obj):
        self.content.append(obj.type)
        obj.rect.x = 18 + (len(self.content) - 1) * 43
        obj.rect.y = 28
        image = load_image(f"{obj.type}_inventory.png", format="png")
        obj.image = image
        obj.image_orig = image


class InteractionObjects(pygame.sprite.Sprite):
    def __init__(self, obj_type, thing_for_action, x, y):
        super().__init__(all_sprites, interaction_objects)
        self.thing = thing_for_action
        self.image = interaction_objects_images[obj_type]
        self.type = obj_type
        self.rect = self.image.get_rect()
        self.pos_x = x
        self.pos_y = y
        self.update_rect()

    def update_rect(self):
        self.rect.topleft = (
            tile_width * self.pos_x + (tile_width - self.rect.width) // 2,
            margin + tile_height * self.pos_y + (tile_height - self.rect.height) // 2)

    def check_need_thing(self):
        if self.thing in inventory.content:
            return True
        return False

    def die(self):
        if self.check_need_thing():
            pygame.sprite.Sprite.kill(self)
            level_y = level[self.pos_y]
            list_level = list(level_y)
            list_level[self.pos_x] = "."
            level[self.pos_y] = "".join(list_level)

    def add_to_inventory(self, thing):
        if self.check_need_thing() and thing.type not in inventory.content:
            inventory.add_thing(thing)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] // tile_width == self.rect.x // tile_width and \
                   event.pos[1] // tile_height == self.rect.y // tile_height and \
                   fabs(player.pos_x - self.pos_x) in [0, 1] and fabs(player.pos_y - self.pos_y) in [0, 1]:
                    if self.type == "sand":
                        if self.pos_x == things_dict['key'].pos_x and self.pos_y == things_dict['key'].pos_y:
                            self.add_to_inventory(things_dict['key'])
                        self.die()
                    elif self.type == "chest":
                        if self.pos_x == things_dict['note'].pos_x and self.pos_y == things_dict['note'].pos_y:
                            self.add_to_inventory(things_dict['note'])


class Things(pygame.sprite.Sprite):
    def __init__(self, things_type, x, y, state=True):
        super().__init__(all_sprites, things)
        self.image = thing_images[things_type]
        self.image_orig = thing_images[things_type]
        self.image_magnified = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
        self.state = state
        self.type = things_type
        self.rect = self.image.get_rect()
        self.rect_magnified = self.image_magnified.get_rect()
        self.pos_x = x
        self.pos_y = y
        self.update_rect()

    def update_rect(self):
        self.rect.topleft = (
            tile_width * self.pos_x + (tile_width - self.rect.width) // 2,
            margin + tile_height * self.pos_y + (tile_height - self.rect.height) // 2)

    def change_surface(self):
        if self.image == self.image_orig:
            self.image = self.image_magnified
            self.rect, self.rect_magnified = self.rect_magnified, self.rect
            if self.type == "note":
                self.image.fill(pygame.Color(122, 121, 121, 150))
                self.font = pygame.font.Font(None, 35)
                self.string_rendered = self.font.render(NOTE_TEXT, True, pygame.Color('black'))
                self.intro_rect = self.string_rendered.get_rect()
                self.intro_rect.top = 230
                self.intro_rect.x = 340
                pygame.draw.rect(self.image, pygame.Color(250, 232, 142), (320, 130, 250, 240))
                self.image.blit(self.string_rendered, self.intro_rect)
        else:
            self.image = self.image_orig
            self.rect, self.rect_magnified = self.rect_magnified, self.rect


    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] // tile_width == self.rect.x // tile_width and self.state and \
                   event.pos[1] // tile_height == self.rect.y // tile_height and \
                   fabs(player.pos_x - self.pos_x) in [0, 1] and fabs(player.pos_y - self.pos_y) in [0, 1]:
                    inventory.add_thing(self)
                    if level[self.pos_y][self.pos_x] == 't':
                        level_y = level[self.pos_y]
                        list_level = list(level_y)
                        list_level[self.pos_x] = "."
                        level[self.pos_y] = "".join(list_level)
                elif self.rect.collidepoint(event.pos) and self.type in inventory.content and \
                        self.type in THINGS_MAGNIFIED:
                    self.change_surface()


class Camera():
    def __init__(self):
        self.cx = self.cy = 0

    def move(self, object):
        object.rect.x = object.pos_x * tile_width - self.cx
        object.rect.y = object.pos_y * tile_width - self.cy

    def update(self, target):
        self.cx = target.pos_x * tile_width + target.rect.w // 2 - WIDTH // 2
        self.cy = target.pos_y * tile_height + target.rect.h // 2 - HEIGHT // 2
        if self.cx + WIDTH >= level_x * tile_width:
            self.cx = level_x * tile_width - WIDTH
        if self.cx < 0:
            self.cx = 0
        if self.cy + HEIGHT >= level_y * tile_height:
            self.cy = level_y * tile_height - HEIGHT
        if self.cy < 0:
            self.cy = 0
        for obj in all_sprites:
            if not(obj.type in inventory.content):
                self.move(obj)


class TinyHelper(pygame.sprite.Sprite):
    def __init__(self, helper_type, way, speed=0):
        super().__init__(all_sprites)
        self.type = helper_type
        self.image = tiny_helpers[self.type]
        self.rect = self.image.get_rect().move(0, 0)
        self.way = way
        self.step = 1
        self.speed = speed
        self.pos_x, self.pos_y = self.way[self.step][0], self.way[self.step][1]
        self.alive = True

    def update_rect(self):
        self.rect.topleft = (
            self.rect.x + (tile_width - self.rect.width) // 2,
            margin + self.rect.y + (tile_height - self.rect.height) // 2
        )

    def update(self, time, events):
        xsign = ysign = 1
        if self.way[self.step][0] - self.way[self.step - 1][0]:
            xs1 = self.way[self.step][0] - self.way[self.step - 1][0]
            xsign = (xs1 // abs(xs1))
            self.pos_x += self.speed * time * xsign
        if self.way[self.step][1] - self.way[self.step - 1][1]:
            ys1 = self.way[self.step][1] - self.way[self.step - 1][1]
            ysign = (ys1 // abs(ys1))
            self.pos_y += self.speed * time * ysign
        if (self.pos_x * xsign > self.way[self.step][0] * xsign or
                self.pos_y * ysign > self.way[self.step][1] * ysign):
            self.step = (self.step + 1) % len(self.way)
            self.pos_x, self.pos_y = self.way[self.step - 1][0], self.way[self.step - 1][1]
        if self.alive and self.way[self.step - 1][2]:
            fon = pygame.transform.scale(load_image('scarabeum_question-1.png'), (WIDTH, HEIGHT))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] // tile_width == self.rect.x // tile_width and \
                            event.pos[1] // tile_height == self.rect.y // tile_height and \
                            (player.pos_x - self.pos_x) ** 2 + (player.pos_y - self.pos_y) ** 2 <= 2:
                        if self.type == 'scarabeus':
                            bttdo = Button(fon,
                                           220, 390, 135, 50,
                                           'Далее',
                                           (0, 0, 0), (200, 200, 200), (255, 255, 255),
                                           5,
                                           [pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_RIGHT])
                            bttdo.draw()
                            bttca = Button(fon,
                                           60, 390, 135, 50,
                                           'Назад',
                                           (0, 0, 0), (200, 200, 200), (255, 255, 255),
                                           5,
                                           [pygame.K_ESCAPE, pygame.K_DELETE])
                            word_taker = WordTaker(fon, (0, 0, 0), 60, 300, 210, 100, 7)
                            bttca.draw()
                            screen.blit(fon, (0, 0))
                            font = pygame.font.Font(None, 30)
                            page, pages = 1, 3
                            main_rect = (60, 60, 300, 300)
                            s = []
                            magic_word = 'ЧЕЛОВЕК'
                            while True:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        terminate()
                                    if page == 1:
                                        bttdo.draw()
                                        bttca.draw()
                                        for line in textes['scarabeus first'].split('\n'):
                                            s.append(font.render(line, 5, (0, 0, 0)))
                                        button_do = bttdo.check(event)
                                        button_ca = bttca.check(event)
                                    elif page == 2:
                                        bttca.draw()
                                        button_ca = bttca.check(event)
                                        button_do = False
                                        for line in textes['scarabeus second'].split('\n'):
                                            s.append(font.render(line, 5, (0, 0, 0)))
                                        word_taker.check(event)
                                        word_taker.draw()
                                        if word_taker == magic_word:
                                            bttdo.draw()
                                            button_do = bttca.check(event)
                                    elif page == 3:
                                        bttca.draw()
                                        button_ca = bttca.check(event)
                                        button_do = False
                                        for line in textes['scarabeus third'].split('\n'):
                                            s.append(font.render(line, 5, (0, 0, 0)))
                                        if 1:
                                            bttdo.draw()
                                            button_do = bttca.check(event)
                                    if button_do:
                                        page += 1
                                        if page == 2:
                                            pygame.draw.rect(screen, pygame.Color(0, 0, 0, 127), bttdo.rect, 0)
                                    if button_ca or page > pages:
                                        return
                                    pygame.draw.rect(screen, (255, 206, 127), main_rect, 0)
                                    for n, i in enumerate(s):
                                        screen.blit(i, pygame.Rect(210 - i.get_width() // 2,
                                                                   110 - len(s) * (i.get_height() + 10) * n // 2 +
                                                                   (i.get_height() + 60) * n,
                                                                   i.get_width() // 2, i.get_height() + 10))
                                    s = []
                                pygame.display.flip()
        self.update_rect()


class Button():
    def __init__(self, screen, x, y, w, h, txt, col1, col2, colt, line_width, eq_type=[]):
        self.rect = pygame.Rect(x, y, w, h)
        self.line_width = line_width
        self.screen = screen
        self.cols = [col1, col2, colt]
        self.text = txt
        self.string_rendered = pygame.font.Font(None, 30).render(self.text, 5, self.cols[2])
        self.textRect = pygame.Rect(x + w // 2 - self.string_rendered.get_width() // 2,
                                    y + h // 2 - self.string_rendered.get_height() // 2,
                                    self.string_rendered.get_width(),
                                    self.string_rendered.get_height())
        self.eq_keys = eq_type

    def draw(self):
        pygame.draw.rect(self.screen, self.cols[0], self.rect, 0)
        pygame.draw.rect(self.screen, self.cols[1], self.rect, self.line_width)
        self.screen.blit(self.string_rendered, self.textRect)

    def check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.pos[1] > self.rect.top and event.pos[1] < self.rect.bottom and
                    event.pos[0] > self.rect.left and event.pos[0] < self.rect.right):
                return True
        if event.type == pygame.KEYDOWN:
            if event.key in self.eq_keys:
                return True
        return False

    def change_cols(self, col1, col2, colt):
        self.cols = [col1, col2, colt]
        self.string_rendered = pygame.font.Font(None, 30).render(self.text, True, colt)


class WordTaker():
    def __init__(self, screen, color, x, y, w, h, n):
        self.text = '_' * n
        self.rect = pygame.Rect(x, y, w, h)
        self.screen = screen
        self.color = color

    def draw(self):
        self.screen.blit(pygame.font.Font(None, 30).render(self.text, True, self.color), self.rect)

    def check(self, event):
        if event.type == pygame.KEYDOWN:
            if event.unicode <= 'z' and event.unicode >= 'A' and self.text.count('_'):
                self.text = (self.text[:(len(self.text) - self.text.count('_'))] + pygame.key.name(event.key).upper() +
                             self.text[(len(self.text) - self.text.count('_') + 1):])
            if event.key == pygame.K_BACKSPACE and len(self.text) != self.text.count('_'):
                self.text = (self.text[:(len(self.text) - self.text.count('_')) - 1] + '_' * (self.text.count('_') + 1))

clock = pygame.time.Clock()
all_sprites         = pygame.sprite.Group()
tiles_group         = pygame.sprite.Group()
things              = pygame.sprite.Group()
interaction_objects = pygame.sprite.Group()
inventory_group     = pygame.sprite.Group()
board               = pygame.sprite.Group()

tile_images = {
    'cactus': load_image('cactus.png', format="png"),
    'tumbleweed': load_image('tumbleweed.png', format="png"),
    'invisible': pygame.Surface((50, 50), pygame.SRCALPHA, 32)
}
thing_images = {
    'shovel': load_image('shovel.png', format="png"),
    'key': pygame.Surface((50, 50), pygame.SRCALPHA, 32),
    'note': pygame.Surface((50, 50), pygame.SRCALPHA, 32)
}
interaction_objects_images = {
    'sand': load_image('sand.png', format="png"),
    'chest': load_image('chest.png', format="png")
}
tiny_helpers = {
    'scarabeus': load_image('scarabeus.png', format="png")
}
textes = {
    'scarabeus first': """Один мой знакомый \n рассказал мне эту загадку""",
    'scarabeus second': 'Кто утром ходит на четырех ногах\n Днем на двух \n А вечером на трех?',
    'scarabeus third': 'Да \n Это -человек'
}

TombWall()
Entry()
background = Background()
inventory = Inventory()
camera = Camera()
scarabeus = TinyHelper('scarabeus', [(1, 3, True), (1, 5, True), (4, 5, True), (4, 3, True)], 1 / 1000)

level = load_level("level1.txt")
player, level_x, level_y, key_coors = generate_level(level)
things_dict = {
    'key': Things("key", key_coors[0], key_coors[1], state=False),
    'note': Things("note", *COOR_NOTE, state=False)
}
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            terminate()
    time = clock.tick(FPS)
    player.update(events)
    scarabeus.update(time, events)
    camera.update(player)
    things.update(events)
    interaction_objects.update(events)
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    inventory_group.draw(screen)
    interaction_objects.draw(screen)
    things.draw(screen)
    pygame.display.flip()
terminate()
