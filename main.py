import os
import random
import sys
import pygame
import pygame_gui

pygame.init()
size = weight, height = (800, 450)
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


class Ball(pygame.sprite.Sprite):
    image = load_image("spear1.png", -1)

    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(Ball.image, (70, 70))
        self.rect = pygame.Rect(self.x, self.y, 2 * radius, 2 * radius)
        self.vx = 0
        self.vy = random.choice([1.2, -1.2])
        self.add(balls_group)

    def update(self):
        self.y += self.vy
        self.x += self.vx
        self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Coin(pygame.sprite.Sprite):
    image = load_image("Coin 64-64.png", -1)

    def __init__(self, radius, points, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.points = points
        self.image = Coin.image
        self.rect = pygame.Rect(self.x, self.y, 2 * radius, 2 * radius)
        self.add(coins_group)


class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.x_size = self.y_size = 50
        self.x = self.y = 10
        self.color = (220, 220, 255)
        self.image = pygame.Surface((self.x_size, self.y_size))
        self.image.fill(self.color)
        self.rect = pygame.Rect(self.x, self.y, self.x_size, self.y_size)
        self.add(char_group)

    def move(self, direction):
        if direction == 'right':
            self.x += 1
        elif direction == 'left':
            self.x -= 1
        elif direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.x_size, self.y_size)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.y = int(self.y) + pygame.sprite.spritecollideany(self, horizontal_borders).coeff
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.x = int(self.x) + pygame.sprite.spritecollideany(self, vertical_borders).coeff
        if pygame.sprite.spritecollideany(self, balls_group):
            self.x = 5
            self.y = 5
        if pygame.sprite.spritecollideany(self, coins_group):
            global score
            score += pygame.sprite.spritecollideany(self, coins_group).points
            pygame.sprite.spritecollide(self, coins_group, True)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, side):
        super().__init__(all_sprites)
        if side == 'right' or side == 'bottom':
            self.coeff = -1
        else:
            self.coeff = 1
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
balls_group = pygame.sprite.Group()
char_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()

char = Character()
motion_keys = {'left': False, 'right': False, 'up': False, 'down': False}

Border(5, 20, weight - 5, 20, 'top')
Border(5, height - 5, weight - 5, height - 5, 'bottom')
Border(5, 20, 5, height - 5, 'left')
Border(weight - 5, 20, weight - 5, height - 5, 'right')

Ball(20, 350, 150)
Ball(20, 300, 150)

Coin(10, 30, 500, 200)
Coin(10, 30, 550, 250)

game_manager = pygame_gui.UIManager(size)  # менеджер для ГИ во время прохождения уровня
pause_manager = pygame_gui.UIManager(size)  # менеджер для ГИ во время паузы

pause_background = pygame.Surface((200, 250))
pause_background.fill(pygame.Color('grey'))

game_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 0), (20, 20)),
    text='||',
    manager=game_manager
)
pause_btn1 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 190), (100, 20)),
    text='Continue',
    manager=pause_manager
)

score = 0
fps = 330
clock = pygame.time.Clock()
running = True
pause = False
game = True
while running:
    screen.fill('white')
    time_delta = clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == pause_btn1:
                    pause = False
                    game = True
                if event.ui_element == game_btn:
                    pause = True
                    game = False
        if game:
            game_manager.process_events(event)
        if pause:
            pause_manager.process_events(event)

    if game:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            char.move('up')
        if keys[pygame.K_LEFT]:
            char.move('left')
        if keys[pygame.K_DOWN]:
            char.move('down')
        if keys[pygame.K_RIGHT]:
            char.move('right')
        all_sprites.update()

    game_manager.update(time_delta)
    game_manager.draw_ui(screen)
    char.move(motion_keys)
    all_sprites.draw(screen)

    if pause:
        screen.blit(pause_background, (300, 100))
        pause_manager.update(time_delta)
        pause_manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
