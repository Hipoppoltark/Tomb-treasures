import pygame
import sys
import os


FPS = 30
SIZE = WIDTH, HEIGHT = 900, 585
CELL_SIZE = 50
WIDTH_FIELD = 18
HEIGHT_FIELD = 8
margin = 185
tile_width = tile_height = 50
pygame.init()
screen = pygame.display.set_mode(SIZE)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    """Заставка, пока нерабочая"""
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


def load_image(name, color_key=None, format="jpg"):
    """Загрузка изображения, измененная версия из учебника, нужно уазывать формат, если картинка png"""
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
    return image


def load_level(filename):
    """Загрузка уровня, так же, как и в учебнике"""
    filename = os.path.join('data', filename)
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    """Генерация уровня, берется из текстового файла в папке data"""
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass  # ничего не делаем, так как у нас есть фон, и поэтому свободные клетки не надо ни как обозначивать
            elif level[y][x] == 'c':
                Tile('cactus', x, y)
            elif level[y][x] == 't':
                Tile('tumbleweed', x, y)
            elif level[y][x] == '@':
                new_player = Hero(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x + 1, y + 1


class TombWall(pygame.sprite.Sprite):
    """Загрзука стены, в дальнейшем будем использовать"""
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("wall.png")
        self.rect = self.image.get_rect()


class Entry(pygame.sprite.Sprite):
    """Вход, так же в последствии будем использовать"""
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("entry.png")
        self.rect = self.image.get_rect()
        self.rect.x = 380
        self.rect.y = 43


class Background(pygame.sprite.Sprite):
    """Фон игры"""
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("background.jpg")
        self.rect = self.image.get_rect()
        self.rect.y = 185


class Hero(pygame.sprite.Sprite):
    """Главный герой"""
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = load_image("hero.png", format="png")
        self.rect = self.image.get_rect().move(
            CELL_SIZE * pos_x, margin + CELL_SIZE * pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
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
                if event.key == pygame.K_UP:
                    new_pos_y -= 1
                elif event.key == pygame.K_DOWN:
                    new_pos_y += 1
                elif event.key == pygame.K_LEFT:
                    new_pos_x -= 1
                elif event.key == pygame.K_RIGHT:
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
    """Класс из учебника, для реализации 'стенок'"""
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.update_rect()


    def update_rect(self):
        self.rect.topleft = (
            tile_width * self.pos_x + (tile_width - self.rect.width) // 2,
            margin + tile_height * self.pos_y + (tile_height - self.rect.height) // 2
        )



clock = pygame.time.Clock()
tile_images = {
    'cactus': load_image('cactus.png', format="png"),
    'tumbleweed': load_image('tumbleweed.png', format="png")
}
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
TombWall()
Entry()
Background()
level = load_level("level1.txt")
player, level_x, level_y = generate_level(level)
board = pygame.sprite.Group()
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            terminate()
    player.update(events)
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
terminate()
