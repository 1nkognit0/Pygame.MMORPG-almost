from settings import *
from random import choices
from images import sprites
from math import hypot

item_chances = {
    'nothing': 4,
    'simple_items': 60,
    'iron_items': 20
}
group_items = {
    'simple_items': ['default_sword'],
    'iron_items': ['iron_sword']
}
characteristic_items = {
    'empty_sword': {'type': 'sword', 'damage': 0.1},
    'default_sword': {'type': 'sword', 'damage': 0.5},
    'iron_sword': {'type': 'sword', 'damage': 1},
    'empty_helmet': {'type': 'armor', 'protection': 0.5},
    'empty_armor': {'type': 'armor', 'protection': 0.25},
    'empty_boots': {'type': 'armor', 'protection': 0},
}


class DropItem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(items_group, all_sprites)
        self.name = self.drop_item()
        if self.name != 'nothing':
            self.image = sprites['items'][self.name]
            self.rect = self.image.get_rect()

    def drop_item(self):
        group = choices(list(item_chances.keys()), weights=list(item_chances.values()), k=1)
        if group[0] == 'nothing':
            self.kill()
            return 'nothing'
        else:
            item_name = choices(group_items[group[0]], k=1)
            return item_name[0]

    def pick_up(self, player):
        distance = hypot(abs(player.rect.x - self.rect.x), abs(player.rect.y - self.rect.y))
        if distance < 70:
            mouse_position = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_position) and pygame.event.poll().type == pygame.MOUSEBUTTONDOWN:
                searching_item = 'undefined'
                while searching_item == 'undefined':
                    for cell in player.inventory_draw:
                        if cell:
                            if self.name == cell.name:
                                cell.amount += 1
                                searching_item = 'has already'
                                self.kill()
                    break
                if None in player.inventory_draw and searching_item == 'undefined':
                    item = InventoryItem(self.name)
                    player.amount_items[self.name] = 1
                    player.inventory_draw.insert(player.inventory_draw.index(None), item)
                    player.inventory_draw.remove(None)
                    self.kill()


class InventoryItem:
    def __init__(self, name):
        self.name = name
        self.image = sprites['interface'][self.name]
        self.type = characteristic_items[self.name]['type']
        self.amount = 1
        if self.type == 'sword':
            self.damage = characteristic_items[self.name]['damage']
        elif self.type == 'armor':
            self.protection = characteristic_items[self.name]['protection']


class InventoryMotionItems:
    def __init__(self):
        self.start_cell = 0
        self.end_cell = 0
        self.help = {1: 'backpack', 2: 'helmet', 3: 'cloak', 4: 'weapon1',
                     5: 'armor', 6: 'weapon2', 7: 'potions', 8: 'boots', 9: 'food'}

    def search_cell(self, pos_x, pos_y, state):
        step = 95
        side = 80
        start_x, start_y = 125, 485

        for y in range(2):
            for x in range(8):
                cell_x = start_x + step * x
                cell_y = start_y + step * y
                if cell_x <= pos_x <= cell_x + side and cell_y <= pos_y <= cell_y + side:
                    if state == 'start':
                        self.start_cell = y * 8 + x + 1
                    else:
                        self.end_cell = y * 8 + x + 1
        step = 120
        side = 100
        start_x, start_y = WIDTH // 2 - 170, 125
        for y in range(3):
            for x in range(3):
                cell_x = start_x + step * x
                cell_y = start_y + step * y
                if cell_x <= pos_x <= cell_x + side and cell_y <= pos_y <= cell_y + side:
                    if state == 'start':
                        self.start_cell = y * 3 + x + 1 + 16
                    else:
                        self.end_cell = y * 3 + x + 1 + 16

    def swap_cells(self, player):
        if self.end_cell != 0:
            if self.end_cell < 17:
                temp = player.inventory_draw[self.end_cell - 1]
                if self.start_cell < 17:
                    player.inventory_draw[self.end_cell - 1] = player.inventory_draw[self.start_cell - 1]
                    player.inventory_draw[self.start_cell - 1] = temp
                else:
                    self.start_cell -= 16
                    if player.equipment_draw[self.start_cell - 1]:
                        if 'empty' not in player.equipment_draw[self.start_cell - 1].name:
                            player.inventory_draw[self.end_cell - 1] = player.equipment_draw[self.start_cell - 1]
                            player.equipment_draw[self.start_cell - 1] = temp
                        self.check_empty_items(player)
                        self.change_characteristic(player)
            else:
                self.end_cell -= 16
                temp = player.equipment_draw[self.end_cell - 1]
                if self.start_cell < 17:
                    if player.inventory_draw[self.start_cell - 1]:
                        player.equipment_draw[self.end_cell - 1] = player.inventory_draw[self.start_cell - 1]
                        if 'empty' not in temp.name:
                            player.inventory_draw[self.start_cell - 1] = temp
                        else:
                            player.inventory_draw[self.start_cell - 1] = None
                        self.change_characteristic(player)

    def check_empty_items(self, player):
        if not player.equipment_draw[1]:
            player.equipment_draw[1] = player.empty_items['empty_helmet']
        if not player.equipment_draw[3]:
            player.equipment_draw[3] = player.empty_items['empty_sword']
        if not player.equipment_draw[4]:
            player.equipment_draw[4] = player.empty_items['empty_armor']
        if not player.equipment_draw[7]:
            player.equipment_draw[7] = player.empty_items['empty_boots']

    def change_characteristic(self, player):
        player.damage = player.all_level[player.level][2] + player.equipment_draw[3].damage
        player.protection = player.equipment_draw[1].protection + player.equipment_draw[4].protection + \
                            player.equipment_draw[7].protection