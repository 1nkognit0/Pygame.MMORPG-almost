import sys
import csv
from random import choice, randint
import os
from math import hypot
from images import sprites, load_image
from settings import *


def terminate():
    pygame.quit()
    sys.exit()


def get_map_name():
    filename = ['map1.txt', 'map2.txt', 'map3.txt']
    global count_level_game
    if not os.path.isfile("data/" + filename[count_level_game]):
        print("ERROR")
        terminate()
    return filename[count_level_game]


def load_map(filename):
    file = "data/" + filename
    with open(file, 'r') as mapFile:
        level_map = mapFile.readlines()

    max_width = max(map(len, level_map)) - 1

    return list(map(lambda x: x.strip().ljust(max_width, '.'), level_map))


def start_screen():
    font_path = os.path.join('data', 'joystix monospace.ttf')
    params = (True, (255, 255, 255))
    font = pygame.font.Font(font_path, 25)
    fon = pygame.transform.scale(load_image('background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    global count_level_game

    with open('info.csv', "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lvl_game = int(row["lvl_game"])
            lvl_hero = int(row['lvl_hero'])
            exp_hero = int(row['exp_hero'])

    pygame.draw.rect(screen, (0, 31, 92), (440, 310, 150, 70), 30)
    pygame.draw.rect(screen, (255, 0, 0), (440, 430, 150, 70), 30)

    if lvl_game == 0 and lvl_hero == 1 and exp_hero == 0:
        text_surface = font.render('Играть', *params)
        screen.blit(text_surface, (450, 265))
    else:
        text_surface = font.render('Продолжить', *params)
        screen.blit(text_surface, (420, 265))
        pygame.draw.rect(screen, (255, 186, 0), (50, 700, 120, 70), 30)
        text_surface = font.render('Новая игра', *params)
        screen.blit(text_surface, (15, 650))

    text_surface = font.render('Выход', *params)
    screen.blit(text_surface, (460, 515))

    pygame.display.flip()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 430:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 500:
                        terminate()
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 310:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 380:
                        with open('info.csv', "r", newline="") as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                count_level_game = int(row["lvl_game"])
                                info = generate_map(load_map(get_map_name()))
                                info[0].level = int(row['lvl_hero'])
                                info[0].exp = int(row['exp_hero'])
                                return info[0], info[1], info[2]
                if not (lvl_game == 0 and lvl_hero == 1 and exp_hero == 0):
                    if pygame.mouse.get_pos()[0] >= 50 and pygame.mouse.get_pos()[1] >= 700:
                        if pygame.mouse.get_pos()[0] <= 170 and pygame.mouse.get_pos()[1] <= 770:
                            with open('info.csv', 'w', newline='') as f:
                                columns = ['lvl_game', 'lvl_hero', 'exp_hero']
                                writer = csv.DictWriter(f, fieldnames=columns)
                                writer.writeheader()
                                count_level_game = 0
                                info = {"lvl_game": 0, "lvl_hero": 1, 'exp_hero': 0}
                                writer.writerow(info)
                            info = generate_map(load_map(get_map_name()))
                            return info[0], info[1], info[2]
        pygame.display.flip()
        clock.tick(FPS)


def dead_screen():
    font_path = os.path.join('data', 'joystix monospace.ttf')
    params = (True, (255, 0, 0))
    font = pygame.font.Font(font_path, 50)
    fon = pygame.transform.scale(load_image('lose.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    pygame.draw.rect(screen, (0, 255, 0), (440, 350, 150, 70), 30)
    pygame.draw.rect(screen, (255, 0, 0), (440, 480, 150, 70), 30)

    text_surface = font.render('Игра окончена', *params)
    screen.blit(text_surface, (275, 180))

    params = (True, (255, 255, 255))
    font = pygame.font.Font(font_path, 25)

    text_surface = font.render('Возродиться', *params)
    screen.blit(text_surface, (410, 300))
    text_surface = font.render('Выход', *params)
    screen.blit(text_surface, (460, 570))

    pygame.display.flip()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 480:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 550:
                        terminate()
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 350:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 420:
                        for group in groups:
                            for sp in group:
                                sp.kill()
                        global player, level_x, level_y
                        player, level_x, level_y = generate_map(load_map(get_map_name()))
                        return
        pygame.display.flip()
        clock.tick(FPS)


def win_screen():
    font_path = os.path.join('data', 'joystix monospace.ttf')
    params = (True, (255, 255, 255))
    font = pygame.font.Font(font_path, 40)
    fon = pygame.transform.scale(load_image('win.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    global count_level_game, player, level_x, level_y

    pygame.draw.rect(screen, (255, 0, 0), (440, 550, 150, 70), 30)

    text_surface = font.render('Поздравляю!', *params)
    screen.blit(text_surface, (350, 150))

    with open('info.csv', 'w', newline='') as f:
        columns = ['lvl_game', 'lvl_hero', 'exp_hero']
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()

        if count_level_game == 1 or count_level_game == 0:
            info = {"lvl_game": count_level_game + 1, "lvl_hero": player.level, 'exp_hero': player.exp}
        else:
            count_level_game = -1
            info = {"lvl_game": count_level_game, "lvl_hero": 1, 'exp_hero': 0}
        writer.writerow(info)

    if count_level_game == 1 or count_level_game == 0:
        pygame.draw.rect(screen, (128, 0, 255), (440, 370, 150, 70), 30)

        font = pygame.font.Font(font_path, 20)
        text_surface = font.render(f'Ты прошел {count_level_game + 1} уровень', *params)
        screen.blit(text_surface, (355, 210))

        font = pygame.font.Font(font_path, 25)
        text_surface = font.render('Следующий уровень', *params)
        screen.blit(text_surface, (350, 320))

        count_level_game += 1

    else:
        pygame.draw.rect(screen, (255, 186, 0), (440, 370, 150, 70), 30)

        font = pygame.font.Font(font_path, 20)
        text_surface = font.render(f'Ты прошел игру', *params)
        screen.blit(text_surface, (415, 210))

        font = pygame.font.Font(font_path, 25)
        text_surface = font.render('Новая игра', *params)
        screen.blit(text_surface, (405, 320))

    text_surface = font.render('Выход', *params)
    screen.blit(text_surface, (460, 640))

    pygame.display.flip()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 550:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 620:
                        terminate()
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 370 and count_level_game != -1:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 440:
                        for group in groups:
                            for sp in group:
                                sp.kill()
                        player, level_x, level_y = generate_map(load_map(get_map_name()))
                        with open('info.csv', "r", newline="") as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                player.level = int(row['lvl_hero'])
                                player.exp = int(row['exp_hero'])
                        return
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 370 and count_level_game == -1:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 440:
                        with open('info.csv', 'w', newline='') as f:
                            columns = ['lvl_game', 'lvl_hero', 'exp_hero']
                            writer = csv.DictWriter(f, fieldnames=columns)
                            writer.writeheader()

                            info = {"lvl_game": 0, "lvl_hero": 1, 'exp_hero': 0}
                            writer.writerow(info)
                        count_level_game = 0
                        info = generate_map(load_map(get_map_name()))
                        return info[0], info[1], info[2]
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(boxes_group, all_sprites)
        elif tile_type == 'border':
            super().__init__(border_group, all_sprites)
        elif tile_type == 'portal':
            super().__init__(portal_group, all_sprites)
        else:
            super().__init__(ground_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Hero(pygame.sprite.Sprite):
    all_level = {1: [0, 30, 1],
                 2: [10, 4, 1],
                 3: [30, 5, 2],
                 4: [50, 6, 2],
                 5: [100, 7, 3]}

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = sprites['hero']['right_stand'][0]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)

        self.left = True
        self.attack = False
        self.f = True
        self.shield = False
        self.death = False
        self.change_x = 0
        self.change_y = 0

        self.level = 1
        self.hp = self.all_level[self.level][1]
        self.max_hp = self.hp
        self.speed = 2
        self.attack_radius = 0
        self.exp = 0
        self.money = 0
        self.damage = self.all_level[self.level][2]

        self.frames = 0
        self.frames_attack = 0
        self.frames_shield = (FPS * 3) + 1
        self.frames_death = 0

    def update(self):
        self.change_x = self.change_y = 0
        # задается изменение картинки через каждые FPS // len(Hero.left_go) фреймов
        pic_ind = self.frames // (FPS // len(sprites['hero']['left_go']))
        self.frames = (self.frames + 1) % FPS  # получаем числа из [0, FPS)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.attack = True

        if self.death:
            if self.frames_death < FPS:
                pic_ind = self.frames_death // (FPS // len(sprites['hero']['left_death']))
                self.frames_death += 1
                self.image = sprites['hero']['left_death'][pic_ind] if self.left else sprites['hero']['left_death'][
                    pic_ind]
            else:
                self.frames_death += 1
                if self.frames_death == FPS * 2:
                    self.death = False
                    dead_screen()

        elif self.attack:
            pic_ind = self.frames_attack // ((FPS // 2) // len(sprites['hero']['left_attack']))
            if (not self.attack_radius) and self.f:
                self.attack_radius = AttackRadius(self.left)
                self.f = False

            self.frames_attack = (self.frames_attack + 1) % (FPS // 2)
            self.image = sprites['hero']['left_attack'][pic_ind] if self.left else sprites['hero']['right_attack'][
                pic_ind]
            if self.frames_attack == (FPS // 4):
                if self.attack_radius:
                    self.attack_radius.kill()
            if self.frames_attack == (FPS // 2) - 1:
                self.attack = False
                self.f = True
                self.frames_attack = 0
                self.attack_radius = 0

        else:
            if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
                self.image = sprites['hero']['left_go'][pic_ind]
                self.left = True
                self.change_x = -self.speed
            if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                self.image = sprites['hero']['right_go'][pic_ind]
                self.left = False
                self.change_x = self.speed
            if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
                self.image = sprites['hero']['left_go'][pic_ind] if self.left else sprites['hero']['right_go'][pic_ind]
                self.change_y = -self.speed
            if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
                self.image = sprites['hero']['left_go'][pic_ind] if self.left else sprites['hero']['right_go'][pic_ind]
                self.change_y = self.speed
            if not (pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]) and \
                    not (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]) and \
                    not (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]) and \
                    not (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]):
                self.image = sprites['hero']['left_stand'][pic_ind] if self.left else sprites['hero']['right_stand'][
                    pic_ind]
            self.rect.x += self.change_x
            self.collide_block('x')
            self.rect.y += self.change_y
            self.collide_block('y')
            if pygame.sprite.spritecollideany(self, portal_group):
                win_screen()

        if self.shield:
            self.presence_shield()

    def collide_block(self, direction):
        if direction == 'x':
            collision = pygame.sprite.spritecollide(self, boxes_group, False)
            if collision:
                if self.change_x > 0:
                    self.rect.x = collision[0].rect.left - self.rect.width
                if self.change_x < 0:
                    self.rect.x = collision[0].rect.right
        elif direction == 'y':
            collision = pygame.sprite.spritecollide(self, boxes_group, False)
            if collision:
                if self.change_y > 0:
                    self.rect.y = collision[0].rect.top - self.rect.height
                if self.change_y < 0:
                    self.rect.y = collision[0].rect.bottom

    def presence_shield(self):
        # щит, спасающий игрока от постоянного получения урона
        self.frames_shield -= 1
        if self.frames_shield == FPS * 3:
            self.shield = True
            return True
        if self.frames_shield == 0:
            self.frames_shield = (FPS * 3) + 1
            self.shield = False
            return False
        else:
            return False

    def level_up(self):
        # увеличение уровня игрока
        if self.level == 5:
            return
        if self.exp >= Hero.all_level[self.level + 1][0]:
            if self.exp == Hero.all_level[self.level + 1][0]:
                self.exp = 0
            else:
                self.exp -= Hero.all_level[self.level + 1][0]
            self.level += 1
            self.max_hp = Hero.all_level[self.level][1]
            self.hp = self.max_hp
            self.damage = Hero.all_level[self.level][2]

    def indicators(self):
        # отрисовка текущего количества хп, появляется только если очки здоровья не фулл
        if self.max_hp != self.hp:
            weight_hp_strip = round((40 / self.max_hp) * self.hp)
            pygame.draw.rect(screen, (pygame.Color('red')), (self.rect.x, self.rect.y - 9, 40, 4))
            pygame.draw.rect(screen, (pygame.Color('green')), (self.rect.x, self.rect.y - 9, weight_hp_strip, 4))

        # отрисовка опыта оставшегося до следующего уровня
        if self.level == 5:
            pygame.draw.rect(screen, (pygame.Color('white')), (self.rect.x, self.rect.y - 3, 40, 2))
        else:
            weight_exp_strip = round((40 / Hero.all_level[self.level + 1][0]) * self.exp)
            pygame.draw.rect(screen, (pygame.Color('black')), (self.rect.x, self.rect.y - 3, 40, 2))
            pygame.draw.rect(screen, (pygame.Color('white')), (self.rect.x, self.rect.y - 3, weight_exp_strip, 2))

        # отрисовка уровня персонажа
        font_path = os.path.join('data', 'joystix monospace.ttf')
        params = (True, (255, 255, 255))
        font = pygame.font.Font(font_path, 10)
        text_surface = font.render(f'{self.level}lv.', *params)
        screen.blit(text_surface, (self.rect.x - 35, self.rect.y - 9))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, name):
        super().__init__(enemies_group, all_sprites)
        self.route = choice(['right', 'left', 'up', 'down'])
        self.len_way = randint(100, 300)

        self.name = name
        self.image = sprites[name]['left_stand'][0]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)

        self.stand = False
        if self.route == 'right':
            self.left = False
        else:
            self.left = True
        self.death = False
        self.reclining = False
        self.x_change = 0
        self.y_change = 0

        self.hp = 0
        self.damage = 0
        self.exp_give = 0
        self.money_give = 0
        self.max_hp = self.hp
        self.passed_now = 0
        self.speed = 1
        self.cycle_stand = 0

        self.frames = 0
        self.frames_stand = 0
        self.frames_death = 0
        self.frames_reclining = 0

    def update(self):
        self.x_change = self.y_change = 0
        pic_ind = self.frames // (FPS // len(sprites[self.name]['left_go']))
        self.frames = (self.frames + 1) % FPS

        distance = hypot(abs(player.rect.x - self.rect.x), abs(player.rect.y - self.rect.y))

        if self.death:
            pic_ind = self.frames_death // ((FPS // 3) // len(sprites[self.name]['left_death']))
            self.frames_death += 1
            self.image = sprites[self.name]['left_death'][pic_ind] if self.left else sprites[self.name]['left_death'][
                pic_ind]
            if self.frames_death == (FPS // 3) - 1:
                player.exp += self.exp_give
                player.money += self.money_give
                player.level_up()
                self.kill()

        elif self.reclining:
            if self.frames_reclining == 20:
                self.reclining = False
                self.frames_reclining = 0
            else:
                self.frames_reclining += 1
                self.x_change -= 3 if player.left else -3
                self.rect.x += self.x_change
                self.collide_block('x', '')

        elif distance < 200:
            if player.rect.x > self.rect.x:
                self.x_change += self.speed
                self.left = False
                self.image = sprites[self.name]['right_go'][pic_ind]
            if player.rect.x < self.rect.x:
                self.x_change -= self.speed
                self.left = True
                self.image = sprites[self.name]['left_go'][pic_ind]
            if player.rect.y > self.rect.y:
                self.y_change += self.speed
                self.image = sprites[self.name]['left_go'][pic_ind] if self.left else sprites[self.name]['right_go'][
                    pic_ind]
            if player.rect.y < self.rect.y:
                self.y_change -= self.speed
                self.image = sprites[self.name]['left_go'][pic_ind] if self.left else sprites[self.name]['right_go'][
                    pic_ind]
            self.rect.x += self.x_change
            self.collide_block('x', '')
            self.rect.y += self.y_change
            self.collide_block('y', '')
            if pygame.sprite.spritecollideany(self, attack_group):
                self.reclining = True
                self.hp -= player.damage
                if self.hp <= 0:
                    self.death = True
            if pygame.sprite.spritecollideany(self, player_group):
                self.rect.x -= self.x_change
                self.rect.y -= self.y_change
                if player.presence_shield():
                    player.hp -= self.damage
                    if player.hp <= 0:
                        player.death = True

        else:
            if self.route == 'left' and not self.stand:
                self.x_change -= self.speed
                self.image = sprites[self.name]['left_go'][pic_ind]
                self.passed_now += self.speed
            elif self.route == 'up' and not self.stand:
                self.y_change -= self.speed
                self.image = sprites[self.name]['left_go'][pic_ind] if self.left else sprites[self.name]['right_go'][
                    pic_ind]
                self.passed_now += self.speed
            elif self.route == 'right' and not self.stand:
                self.x_change += self.speed
                self.image = sprites[self.name]['right_go'][pic_ind]
                self.passed_now += self.speed
            elif self.route == 'down' and not self.stand:
                self.y_change += self.speed
                self.image = sprites[self.name]['left_go'][pic_ind] if self.left else sprites[self.name]['right_go'][
                    pic_ind]
                self.passed_now += self.speed
            self.rect.x += self.x_change
            self.collide_block('x', '+')
            self.rect.y += self.y_change
            self.collide_block('y', '+')

            if self.passed_now >= self.len_way:
                self.passed_now = 0
                self.route = choice(['right', 'left', 'up', 'down'])
                self.len_way = randint(200, 400)
                if self.route == 'right':
                    self.left = False
                if self.route == 'left':
                    self.left = True
                self.stand = True

            if self.stand:
                pic_ind = self.frames_stand // ((FPS - 40) // len(sprites[self.name]['left_stand']))
                self.cycle_stand += 1
                self.frames_stand = (self.frames_stand + 1) % (FPS - 40)
                self.image = sprites[self.name]['left_stand'][pic_ind] if self.left else \
                    sprites[self.name]['right_stand'][pic_ind]
                if self.cycle_stand >= 360:
                    self.stand = False
                    self.cycle_stand = 0
                    self.frames_stand = 0

    def collide_block(self, direction, purpose):
        if direction == 'x':
            collision = pygame.sprite.spritecollide(self, boxes_group, False)\
                        + pygame.sprite.spritecollide(self, border_group, False)
            if collision:
                if self.x_change > 0:
                    self.rect.x = collision[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = collision[0].rect.right
                if purpose:
                    self.route = choice(['right', 'left', 'up', 'down'])
                    self.len_way = randint(200, 400)
        elif direction == 'y':
            collision = pygame.sprite.spritecollide(self, boxes_group, False)\
                        + pygame.sprite.spritecollide(self, border_group, False)
            if collision:
                if self.y_change > 0:
                    self.rect.y = collision[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = collision[0].rect.bottom
                if purpose:
                    self.route = choice(['right', 'left', 'up', 'down'])
                    self.len_way = randint(200, 400)

    def hp_strip(self):
        if self.max_hp != self.hp:
            weight_green_strip = round((40 / self.max_hp) * self.hp)
            pygame.draw.rect(screen, (pygame.Color('red')), (self.rect.x - 5, self.rect.y - 5, 40, 5))
            pygame.draw.rect(screen, (pygame.Color('green')), (self.rect.x - 5, self.rect.y - 5, weight_green_strip, 5))


class Bear(Enemy, pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, name):
        Enemy.__init__(self, pos_x, pos_y, name)
        pygame.sprite.Sprite.__init__(self, enemies_group, all_sprites)
        self.hp = 15
        self.damage = 1.5
        self.max_hp = self.hp
        self.exp_give = 10
        self.money_give = randint(4, 7)


class Slime(Enemy, pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, name):
        Enemy.__init__(self, pos_x, pos_y, name)
        pygame.sprite.Sprite.__init__(self, enemies_group, all_sprites)
        self.hp = 5
        self.damage = 1
        self.max_hp = self.hp
        self.exp_give = 3
        self.money_give = randint(1, 4)


class AttackRadius(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__(attack_group, all_sprites)
        self.left = side
        if self.left:
            self.rect = pygame.Rect(player.rect.x - 30, player.rect.y, 30, player.rect.height)
        else:
            self.rect = pygame.Rect(player.rect.x + player.rect.width, player.rect.y, 30, player.rect.height)


def generate_map(level):
    new_player, x, y = None, None, None
    x_player = y_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'E':
                Tile('empty', x, y)
                x_enemy = x
                y_enemy = y
                Slime(x_enemy, y_enemy, 'slime')
            elif level[y][x] == 'B':
                Tile('empty', x, y)
                x_enemy = x
                y_enemy = y
                Bear(x_enemy, y_enemy, 'bear')
            elif level[y][x] == '|':
                Tile('border', x, y)
            elif level[y][x] == 'P':
                Tile('portal', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                x_player = x
                y_player = y
    new_player = Hero(x_player, y_player)

    return new_player, x, y  # объект спрайт игрока, а также размер поля в клетках


class Camera:
    # зададим начальные значения смещения
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на значения смещения
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # задать смещению значения равные расстоянию от центра target до центра экрана
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Interface:
    def draw(self):
        self.money()

    def money(self):
        font_path = os.path.join('data', 'joystix monospace.ttf')
        params = (True, (255, 255, 255))
        font = pygame.font.Font(font_path, 25)
        screen.blit(sprites['interface']['money'], (10, 10))

        text_surface = font.render(str(player.money), *params)
        screen.blit(text_surface, (70, 25))


tile_images = {'wall': load_image('crate.png'),
               'border': load_image('grass3.png'),
               'empty': load_image('grass3.png'),
               'portal': load_image('portal.png')}

# группы спрайтов
all_sprites = pygame.sprite.Group()
boxes_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
attack_group = pygame.sprite.Group()
ground_group = pygame.sprite.Group()
border_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
interface_group = pygame.sprite.Group()
groups = [all_sprites, boxes_group, player_group, enemies_group, ground_group, border_group, portal_group, attack_group]

tile_width = tile_height = 75

camera = Camera()

with open('info.csv', "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        count_level_game = int(row['lvl_game'])

# Вызов стартового окна
if count_level_game != -1:
    player, level_x, level_y = start_screen()
else:
    player, level_x, level_y = win_screen()

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    enemies_group.update()  # изменяем координаты всех врагов на карте
    player.update()  # изменить координаты персонажа (если нажата клавиша движения)

    ground_group.draw(screen)
    boxes_group.draw(screen)
    border_group.draw(screen)
    enemies_group.draw(screen)
    for i in enemies_group:
        i.hp_strip()
    player_group.draw(screen)
    attack_group.update()
    player.indicators()
    portal_group.draw(screen)
    Interface().draw()

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
