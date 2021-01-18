import pygame
import sys
import os
import random
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
    intro_text = ["Tomb Treasures", "", "", "", "", "",
                  "Начни путь приключений",
                  "Нажми на кнопку для начала"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("fonts/konstanting.ttf", 30)
    text_coord = 60
    margin_text = 370
    colors = ["black", (181, 184, 26)]
    for i, line in enumerate(intro_text):
        if i < 2:
            string_rendered = font.render(line, 1, pygame.Color(colors[0]))
        else:
            string_rendered = font.render(line, 1, pygame.Color(colors[1]))
        intro_rect = string_rendered.get_rect()
        text_coord += 15
        intro_rect.top = text_coord
        intro_rect.x = margin_text
        if i > 3:
            margin_text -= 20
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
                if len(level) == 11:
                    InteractionObjects("sand", "shovel", x, y)
                    key_coors.append((x, y))
                else:
                    InteractionObjects("sarcophag", "crowbar", x, y - 1)
                    key_coors.append((x, y - 1))
            elif level[y][x] == 't':
                Things('shovel', x, y)
            elif level[y][x] == 'c':
                InteractionObjects('chest', 'key', x, y)
            elif level[y][x] == '_':
                Tile('invisible', x, y)
            elif level[y][x] == '@':
                new_player = Hero(x, y)
            elif level[y][x] == "b":
                Things('crowbar', x, y)
    if key_coors:
        key_coors = random.choice(key_coors)
    # вернем игрока, а также размер поля в клетках
    return new_player, x + 1, y + 1, key_coors


def fin(number):
    global all_sprites, tiles_group, things, interaction_objects, inventory_group, helpers_group
    global player, level_x, level_y, key_coors, margin, level, things_dict
    margin = 0
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    things = pygame.sprite.Group()
    interaction_objects = pygame.sprite.Group()
    inventory_group = pygame.sprite.Group()
    helpers_group = pygame.sprite.Group()
    if number == 1:
        Background("level2.jpg", 0)
        inventory = Inventory()
        level = load_level("level2.txt")
        entry = Entry('entry2', 'lense', 380, 16)
        player, level_x, level_y, key_coors = generate_level(level)
        things_dict = {
            'key': Things("key", *key_coors, state=False),
            'note2': Things("note", *COOR_NOTE_ROOM_2, state=False),
            'level_n': 2
        }
    if number == 2:
        Background("Treasure Room.png", 0)
        level = load_level("level3.txt")
        player, level_x, level_y, key_coors = generate_level(level)
        text1 = "Создали: Полтавина Елизавета и Сафонов Борис"
        text2 = "КОНЕЦ"

        font = pygame.font.Font(None, 50)
        string_rendered1 = font.render(text1, 1, (255, 255, 255))
        string_rendered2 = font.render(text2, 1, (255, 255, 255))
        intro_rect1 = string_rendered1.get_rect()
        intro_rect1.top = 425
        intro_rect1.x = 900
        intro_rect2 = string_rendered2.get_rect()
        intro_rect2.top = 425
        intro_rect2.x = WIDTH // 2 - intro_rect2.w // 2
        clock_last = pygame.time.Clock()
        TIME = 0
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    terminate()
            player.update(events)
            all_sprites.draw(screen)
            time = clock_last.tick()
            TIME += time
            if TIME < 10000:
                if intro_rect1.x > 20:
                    intro_rect1.x -= time * 2 / 1000
                screen.blit(string_rendered1, intro_rect1)
            elif TIME > 13000:
                break
            else:
                screen.blit(string_rendered2, intro_rect2)
            pygame.display.flip()


        intro_text = ["Tomb Treasures", "", "", "", "", "",
                      "Спасибо за прохождение игры!",
                      "В дальнейшем вас ждет больше уровней!"]

        fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font("fonts/konstanting.ttf", 30)
        text_coord = 60
        margin_text = 370
        colors = ["black", (181, 184, 26)]
        for i, line in enumerate(intro_text):
            if i < 2:
                string_rendered = font.render(line, 1, pygame.Color(colors[0]))
            else:
                string_rendered = font.render(line, 1, pygame.Color(colors[1]))
            intro_rect = string_rendered.get_rect()
            text_coord += 15
            intro_rect.top = text_coord
            intro_rect.x = margin_text
            if i > 3:
                margin_text -= 20
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    terminate()
            pygame.display.flip()
            clock.tick(FPS)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        player.update(events)
        things.update(events)
        interaction_objects.update(events)
        interaction_objects.draw(screen)
        all_sprites.draw(screen)
        tiles_group.draw(screen)
        inventory_group.draw(screen)
        things.draw(screen)
        pygame.display.flip()
    terminate()
    return


class TombWall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("wall.png")
        self.rect = self.image.get_rect()
        self.type = "wall"
        self.image_entry = load_image("entry.png")
        self.rect_entry = self.image_entry.get_rect()
        self.pos_x = self.pos_y = 0


class Background(pygame.sprite.Sprite):
    def __init__(self, name, margin_top):
        super().__init__(all_sprites)
        self.image = load_image(name)
        self.rect = self.image.get_rect()
        self.rect.y = setle(margin_top, 0)
        self.type = "background"
        self.pos_x = self.rect.x // tile_width
        self.pos_y = self.rect.y // tile_height


class Hero(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = self.r_image = load_image("hero.png", format="png")
        self.l_image = pygame.transform.flip(self.r_image, True, False)
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
                    self.image = self.l_image
                    new_pos_x -= 1
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.image = self.r_image
                    new_pos_x += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] < self.rect.x + self.rect.w // 2:
                    self.image = self.l_image
                elif event.pos[0] > self.rect.x + self.rect.w // 2:
                    self.image = self.r_image
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

    def remove(self, obj):
        if obj.type in self.content:
            del self.content[self.content.index(obj.type)]
            things.remove(obj)
            all_sprites.remove(obj)

    def clear(self):
        for i in all_sprites:
            self.remove(i)


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
            tile_width * self.pos_x + abs(tile_width - self.rect.width) // 2,
            margin + tile_height * self.pos_y)

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
            if self.type == "chest" and things_dict['level_n'] == 1:
                scarabeus.live()

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] // tile_width == self.rect.x // tile_width and \
                   event.pos[1] // tile_height == self.rect.y // tile_height and \
                   abs(player.pos_x - self.pos_x) in [0, 1] and abs(player.pos_y - self.pos_y) in [0, 1]:
                    if self.type == "sand":
                        if self.pos_x == things_dict['key'].pos_x and self.pos_y == things_dict['key'].pos_y:
                            self.add_to_inventory(things_dict['key'])
                        self.die()
                    elif self.type == "chest":  # На доработку
                        if things_dict['level_n'] == 1:
                            if self.pos_x == things_dict['note'].pos_x and self.pos_y == things_dict['note'].pos_y:
                                self.add_to_inventory(things_dict['note'])
                        elif things_dict['level_n'] == 2:
                            if self.pos_x == things_dict['note2'].pos_x and self.pos_y == things_dict['note2'].pos_y:
                                self.add_to_inventory(things_dict['note2'])
                    elif self.type == "sarcophag":
                        if self.pos_x == things_dict['key'].pos_x and self.pos_y == things_dict['key'].pos_y:
                            self.add_to_inventory(things_dict['key'])


class Entry(InteractionObjects):
    def __init__(self, obj_type, thing_for_action, x, y):
        super().__init__(obj_type, thing_for_action, x, y)
        if self.type == 'entry':
            self.image = load_image("entry1.png")
            self.rect = self.image.get_rect()
            self.rect.x = setle(380, 1)
            self.rect.y = 8
            self.pos_x = self.rect.x // tile_width
            self.pos_y = self.rect.y / tile_height
            self.big_image, self.open_image = load_image("big entry.jpg"), load_image("big entry2.jpg")
            self.lense_pX, self.lense_pY, self.lense_pR = 450, 90, 30
        elif self.type == 'entry2':
            self.image = load_image("entry2.png", format='png')
            self.rect = self.image.get_rect()
            self.rect.x = setle(400, 1)
            self.rect.y = 225
            self.pos_x = self.rect.x // tile_width
            self.pos_y = self.rect.y / tile_height
            self.big_image, self.open_image = load_image("big entry 3.0.jpg"), load_image("big entry 3.jpg")
            self.wall_wheels = [WallWheel(107, 45, 15, True, 208, 80, [f"plates\plate1.{str(i + 1)}.png" for i in range(7)]),
                           WallWheel(107, 45, 15, True, 334, 80, [f"plates\plate2.{str(i + 1)}.png" for i in range(7)]),
                           WallWheel(107, 45, 15, True, 460, 80, [f"plates\plate3.{str(i + 1)}.png" for i in range(7)]),
                           WallWheel(107, 45, 15, True, 586, 80, [f"plates\plate4.{str(i + 1)}.png" for i in range(7)])]

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] <= self.rect.right and event.pos[0]  >= self.rect.left and \
                        event.pos[1] <= self.rect.bottom and event.pos[0] >= self.rect.top:
                    if  (player.pos_x in [7, 8, 9] and player.pos_y in [3] and self.type == 'entry') or\
                            (player.pos_x in [8, 9] and player.pos_y in [6] and self.type == 'entry2'):
                        self.closer_view()
                    return

    def closer_view(self):
        fon = pygame.transform.scale(self.big_image, (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        if self.type == 'entry':
            bttca = Button(screen,
                           60, 390, 135, 50,
                           'Назад',
                           (0, 0, 0), (200, 200, 200), (255, 255, 255),
                           5,
                           [pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_DELETE])
            while True:
                bttca.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif bttca.check(event):
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if 'lense' in inventory.content:
                            if ((event.pos[0] - self.lense_pX) ** 2 + (event.pos[1] - self.lense_pY) ** 2 <=
                                    self.lense_pR ** 2):
                                bttca.close()
                                self.open(1)
                                return
                pygame.display.flip()
        elif self.type == 'entry2':
            bttca = Button(screen,
                           60, 390, 135, 50,
                           'Назад',
                           (0, 0, 0), (200, 200, 200), (255, 255, 255),
                           5,
                           [pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_DELETE])
            while True:
                bttca.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif bttca.check(event):
                        return
                    for wall_wheel in self.wall_wheels:
                        wall_wheel.check(event)
                        if wall_wheel.current:
                            wwc = self.wall_wheels.index(wall_wheel)
                for wall_wheel in self.wall_wheels:
                    wall_wheel.update()
                if tuple(map(lambda x: x.number, self.wall_wheels)) == (3, 5, 4, 1):
                    self.open(2)
                plate_sprites.draw(screen)
                pygame.display.flip()

    def open(self, n):
        inventory.clear()
        fon = pygame.transform.scale(self.open_image, (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        bttgo = Button(screen,
                       WIDTH // 2 - 70, 390, 150, 100,
                       'Войти',
                       (0, 0, 0), (200, 200, 200), (255, 255, 255),
                       5,
                       [13, pygame.K_SPACE, pygame.K_RIGHT, pygame.K_UP])
        while True:
            bttgo.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif bttgo.check(event):
                    fin(n)
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] <= 550 and event.pos[0] >= 360 and event.pos[1] <= HEIGHT and event.pos[1] >= 215:
                        fin(n)
                        return
            pygame.display.flip()


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
                if things_dict['level_n'] == 1:
                    self.string_rendered = self.font.render(NOTE_TEXT, True, pygame.Color('black'))
                    self.intro_rect = self.string_rendered.get_rect()
                    self.intro_rect.top = 230
                    self.intro_rect.x = 340
                    pygame.draw.rect(self.image, pygame.Color(250, 232, 142), (320, 130, 250, 240))
                    self.image.blit(self.string_rendered, self.intro_rect)
                elif things_dict['level_n'] == 2:
                    self.string_rendered = load_image('note2_inventory.png', format='png')
                    self.intro_rect = self.string_rendered.get_rect()
                    self.intro_rect.top = 80
                    self.intro_rect.x = 180
                    pygame.draw.rect(self.image, pygame.Color(250, 232, 142), (180, 70, 400, 360))
                    self.image.blit(self.string_rendered, self.intro_rect)
        else:
            self.image = self.image_orig
            self.rect, self.rect_magnified = self.rect_magnified, self.rect

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] // tile_width == self.rect.x // tile_width and self.state and \
                   event.pos[1] // tile_height == self.rect.y // tile_height and \
                   abs(player.pos_x - self.pos_x) in [0, 1] and abs(player.pos_y - self.pos_y) in [0, 1]:
                    inventory.add_thing(self)
                    if level[self.pos_y][self.pos_x] == 't':
                        level_y = level[self.pos_y]
                        list_level = list(level_y)
                        list_level[self.pos_x] = "."
                        level[self.pos_y] = "".join(list_level)
                elif self.rect.collidepoint(event.pos) and self.type in inventory.content and \
                        self.type in THINGS_MAGNIFIED:
                    self.change_surface()


class Camera:
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
        super().__init__(helpers_group)
        self.type = helper_type
        self.image = self.origimage = tiny_helpers[self.type]
        self.rect = self.image.get_rect().move(0, 0)
        self.way = way
        self.step = 1
        self.speed = speed
        self.pos_x, self.pos_y = self.way[self.step][0], self.way[self.step][1]
        self.alive = self.subAlive = False

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
            if xsign < 0:
                self.image = pygame.transform.rotate(self.origimage, 90)
            if xsign > 0:
                self.image = pygame.transform.rotate(self.origimage, 270)
        if self.way[self.step][1] - self.way[self.step - 1][1]:
            ys1 = self.way[self.step][1] - self.way[self.step - 1][1]
            ysign = (ys1 // abs(ys1))
            self.pos_y += self.speed * time * ysign
            if ysign > 0:
                self.image = pygame.transform.rotate(self.origimage, 180)
            if ysign < 0:
                self.image = pygame.transform.rotate(self.origimage, 0)
        if (self.pos_x * xsign > self.way[self.step][0] * xsign or
                self.pos_y * ysign > self.way[self.step][1] * ysign):
            self.step = (self.step + 1) % len(self.way)
            self.pos_x, self.pos_y = self.way[self.step - 1][0], self.way[self.step - 1][1]
        self.subAlive = self.way[self.step - 1][2]
        if self.alive and self.subAlive:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] // tile_width == self.rect.x // tile_width and \
                            event.pos[1] // tile_height == self.rect.y // tile_height and \
                            (player.pos_x - self.pos_x) ** 2 + (player.pos_y - self.pos_y) ** 2 <= 2:
                        if self.type == 'scarabeus':
                            fon = pygame.transform.scale(load_image('scarabeum_question-1.png'), (WIDTH, HEIGHT))
                            bttdo = Button(screen,
                                           220, 390, 135, 50,
                                           'Далее',
                                           (0, 0, 0), (200, 200, 200), (255, 255, 255),
                                           5,
                                           [13, pygame.K_SPACE, pygame.K_RIGHT])
                            bttdo1 = Button(screen,
                                           620, 390, 135, 50,
                                           'Далее',
                                           (0, 0, 0), (200, 200, 200), (255, 255, 255),
                                           5,
                                           [13, pygame.K_SPACE, pygame.K_RIGHT])
                            bttdo.draw()
                            bttca = Button(screen,
                                           60, 390, 135, 50,
                                           'Назад',
                                           (0, 0, 0), (200, 200, 200), (255, 255, 255),
                                           5,
                                           [pygame.K_ESCAPE, pygame.K_DELETE])
                            word_taker = WordTaker(screen, (0, 0, 0), 100, 320, 295, 65, 7, 'ЧЕЛОВЕК')
                            bttca.draw()
                            screen.blit(fon, (0, 0))
                            font = pygame.font.Font(None, 30)
                            page, pages = 1, 4
                            main_rect = (40, 75, 341, 350)
                            s = []
                            while True:
                                for event in pygame.event.get():
                                    pygame.draw.rect(screen, (255, 206, 127), main_rect, 0)
                                    pygame.draw.rect(screen, (255, 206, 127), (55, 275, 315, 170), 0)
                                    if event.type == pygame.QUIT:
                                        terminate()
                                    if page == 1:
                                        for line in textes['scarabeus first'].split('\n'):
                                            s.append(font.render(line, 5, (0, 0, 0)))
                                        button_do = bttdo.check(event)
                                        button_ca = bttca.check(event)
                                    elif page == 2:
                                        word_taker.check(event)
                                        word_taker.draw()
                                        for line in textes['scarabeus second'].split('\n'):
                                            s.append(font.render(line, 5, (0, 0, 0)))
                                        if word_taker.text == word_taker.magic_word:
                                            bttdo.open()
                                        else:
                                            bttdo.close()
                                        button_do = bttdo.check(event)
                                        button_ca = bttca.check(event)
                                    elif page == 3:
                                        for line in textes['scarabeus third'].split('\n'):
                                            s.append(font.render(line, 5, (0, 0, 0)))
                                        button_do = bttdo.check(event)
                                        bttca.close()
                                    elif page == 4:
                                        # На доработку
                                        bttdo.close()
                                        fon = pygame.transform.scale(load_image('scarabeum_question-1.1.png'),
                                                                     (WIDTH, HEIGHT))
                                        screen.blit(fon, (0, 0))
                                        i = pygame.font.Font(None, 50).render(textes['lense getting'], True,
                                                                              (230, 200, 255))
                                        screen.blit(i, pygame.Rect(120, bttdo1.rect.top + i.get_height() // 2 - 10,
                                                                  i.get_width() // 2, i.get_height() + 10))
                                        bttdo1.draw()
                                        button_do = bttdo1.check(event)
                                    if button_do:
                                        page += 1
                                    if button_ca:
                                        return
                                    if page > pages:
                                        inventory.add_thing(Things('lense', 0, 0))
                                        self.die()
                                        return
                                    for n, i in enumerate(s):
                                        screen.blit(i, pygame.Rect(210 - i.get_width() // 2,
                                                                   110 - len(s) * (i.get_height() + 10) * n // 2 +
                                                                   (i.get_height() + 60) * n,
                                                                   i.get_width() // 2, i.get_height() + 10))
                                    bttdo.draw()
                                    bttca.draw()
                                    s = []
                                pygame.display.flip()
        self.update_rect()

    def die(self):
        self.alive = False

    def live(self):
        self.alive = True


class Button:
    def __init__(self, screen, x, y, w, h, txt, col1, col2, colt, line_width, eq_type=[]):
        self.rect = pygame.Rect(x, y, w, h)
        self.line_width = line_width
        self.screen = screen
        self.cols = [col1, col2, colt]
        self.text = txt
        self.string_rendered = pygame.font.Font(None, 30).render(self.text, True, self.cols[2])
        self.textRect = pygame.Rect(x + w // 2 - self.string_rendered.get_width() // 2,
                                    y + h // 2 - self.string_rendered.get_height() // 2,
                                    self.string_rendered.get_width(),
                                    self.string_rendered.get_height())
        self.eq_keys = eq_type
        self.alive = True

    def draw(self):
        if not(self.alive):
            return
        pygame.draw.rect(self.screen, self.cols[0], self.rect, 0)
        pygame.draw.rect(self.screen, self.cols[1], self.rect, self.line_width)
        self.screen.blit(self.string_rendered, self.textRect)

    def check(self, event):
        if not(self.alive):
            return False
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

    def close(self):
        self.alive = False

    def open(self):
        self.alive = True


class WordTaker:
    def __init__(self, screen, color, x, y, w, h, n=3, magic_word=''):
        self.text = '_' * n
        self.rect = pygame.Rect(x, y, w, h)
        self.screen = screen
        self.color = color
        self.font =  pygame.font.SysFont('Courier New', 48)
        self.magic_word = magic_word

    def draw(self):
        self.screen.blit(self.font.render(self.text, True, self.color), self.rect)

    def check(self, event):
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha() and self.text.count('_'):
                letter = event.unicode.upper()
                self.text = (self.text[:(len(self.text) - self.text.count('_'))] + letter +
                             self.text[(len(self.text) - self.text.count('_') + 1):])
            if event.key == pygame.K_BACKSPACE and len(self.text) != self.text.count('_'):
                self.text = (self.text[:(len(self.text) - self.text.count('_')) - 1] + '_' * (self.text.count('_') + 1))


class WallWheel:
    def __init__(self, w, h, d, hv, x, y, plates):
        self.plates = []
        self.x, self.y = x, y
        self.plate_width, self.plate_height = w, h
        self.dist = d
        self.hv = hv
        for plate in plates:
            plate_sprite = pygame.sprite.Sprite(plate_sprites)
            plate_sprite.image = load_image(plate)
            plate_sprite.rect = plate_sprite.image.get_rect()
            plate_sprite.rect.x, plate_sprite.rect.y = x, y
            self.plates.append(plate_sprite)
        self.current = False
        self.plates_number = len(self.plates)
        self.number = 0

    def update(self):
        if self.hv:
            for plate in self.plates:
                plate.rect.y = self.y + (self.dist + self.plate_height) * self.plates.index(plate)
        else:
            for plate in self.plates:
                plate.rect.x = self.x + (self.dist + self.plate_width) * self.plates.index(plate)

    def check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] <= (self.x + self.plate_width + (self.plate_width + self.dist) *
                                (self.plates_number - 1) * (not(self.hv))) and \
                    event.pos[0] >= self.x and \
                    event.pos[1] <= (self.y + self.plate_height + (self.plate_height + self.dist) *
                                     (self.plates_number - 1) * self.hv) and \
                    event.pos[1] >= self.y:
                self.current = True
            else:
                self.current = False
        if event.type == pygame.KEYDOWN and self.current:
            if (event.key == pygame.K_UP or event.type == pygame.K_w):
                self.number = (self.number - 1) % self.plates_number
                self.plates = list(self.plates[1:]) + [self.plates[0]]
            if (event.key == pygame.K_DOWN or event.type == pygame.K_s):
                self.number = (self.number + 1) % self.plates_number
                self.plates = [self.plates[-1]] + list(self.plates[:-1])


clock = pygame.time.Clock()
all_sprites         = pygame.sprite.Group()
tiles_group         = pygame.sprite.Group()
things              = pygame.sprite.Group()
interaction_objects = pygame.sprite.Group()
inventory_group     = pygame.sprite.Group()
board               = pygame.sprite.Group()
helpers_group       = pygame.sprite.Group()
plate_sprites       = pygame.sprite.Group()

tile_images = {
    'cactus': load_image('cactus.png', format="png"),
    'tumbleweed': load_image('tumbleweed.png', format="png"),
    'invisible': pygame.Surface((50, 50), pygame.SRCALPHA, 32),
    'lense': load_image('lense_inventory.png', format="png")
}
thing_images = {
    'shovel': load_image('shovel.png', format="png"),
    'key': pygame.Surface((50, 50), pygame.SRCALPHA, 32),
    'note': pygame.Surface((50, 50), pygame.SRCALPHA, 32),
    'note2': pygame.Surface((50, 50), pygame.SRCALPHA, 32),
    'lense': pygame.Surface((50, 50), pygame.SRCALPHA, 32),
    'scarabeus with lense': pygame.Surface((50, 50), pygame.SRCALPHA, 32),
    'crowbar': load_image('crowbar.png', format="png")
}
interaction_objects_images = {
    'sand': load_image('sand.png', format="png"),
    'chest': load_image('chest.png', format="png"),
    'entry': load_image('entry1.png', format="png"),
    'sarcophag': load_image('sarc.png', format="png"),
    'entry2': load_image('entry2.png', format="png")
}
tiny_helpers = {
    'scarabeus': load_image('scarabeus.png', format="png")
}
textes = {
    'scarabeus first': """Если ты скажешь\n мне ключевое слово\n Я дам тебе ключ \nдля входа в гробницу""",
    'scarabeus second': 'Используй все то, что у тебя есть',
    'scarabeus third': 'Да \n Человек - ключ ко всему!',
    'lense getting': 'Вы получили линзу'
}
scarabeus_way = [(15, 6, False), (15, 9, True), (15, 6, True), (12, 6, False), (16, 6, False),
                 (16, 4, True), (16, 7, True), (18, 7, False), (18, 5, True),
                 (15, 5, True), (15, 6, True), (12, 6, False)]

TombWall()
Entry('entry', 'lense', 380, 16)
background = Background("background.jpg", 185)
inventory = Inventory()
camera = Camera()
scarabeus = TinyHelper('scarabeus', scarabeus_way, 1 / 1000)

start_screen()
level = load_level("level1.txt")
player, level_x, level_y, key_coors = generate_level(level)
things_dict = {
    'key': Things("key", key_coors[0], key_coors[1], state=False),
    'note': Things("note", *COOR_NOTE, state=False),
    'level_n': 1
}
pygame.display.set_caption('Tomb-treasures')
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            terminate()
    time = clock.tick(FPS)
    helpers_group.update(time, events)
    if scarabeus.subAlive and scarabeus.alive:
        all_sprites.add(helpers_group)
    else:
        all_sprites.remove(helpers_group)
    all_sprites.add(player)
    player.update(events)
    camera.update(player)
    things.update(events)
    interaction_objects.update(events)
    all_sprites.draw(screen)
    all_sprites.remove(player)
    tiles_group.draw(screen)
    inventory_group.draw(screen)
    interaction_objects.draw(screen)
    things.draw(screen)
    pygame.display.flip()
terminate()
