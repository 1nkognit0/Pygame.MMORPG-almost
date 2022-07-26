import os
import sys
from settings import *


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):  # если файл не существует, то выходим
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


sprites = {
    'slime':
        {'left_go': [pygame.transform.scale(load_image(f'slime_left\slime_go_{i}.png', color_key=-1),
                                            (38, 56)) for i in range(1, 13)],
         'left_stand': [pygame.transform.scale(load_image(f'slime_left\slime_stand_{i}.png', color_key=-1),
                                               (38, 56)) for i in range(1, 3)],
         'left_death': [pygame.transform.scale(load_image(f'slime_left\slime_dead_{i}.png', color_key=-1),
                                               (38, 56)) for i in range(1, 6)],
         'right_go': [pygame.transform.scale(load_image(f'slime_right\slime_go_{i}.png', color_key=-1),
                                             (38, 56)) for i in range(1, 13)],
         'right_stand': [pygame.transform.scale(load_image(f'slime_right\slime_stand_{i}.png', color_key=-1),
                                                (38, 56)) for i in range(1, 3)],
         'right_death': [pygame.transform.scale(load_image(f'slime_right\slime_dead_{i}.png', color_key=-1),
                                                (38, 56)) for i in range(1, 6)]},
    'bear':
        {'left_go': [pygame.transform.scale(load_image(f'bear_right/bear_go_{i}.png', color_key=-1),
                                            (60, 65)) for i in range(1, 5)],
         'left_stand': [pygame.transform.scale(load_image(f'bear_right/bear_{i}.png', color_key=-1),
                                               (60, 65)) for i in range(1, 5)],
         'left_death': [pygame.transform.scale(load_image(f'bear_right/bear_death_{i}.png', color_key=-1),
                                               (60, 56)) for i in range(1, 4)],
         'right_go': [pygame.transform.scale(load_image(f'bear_left/bear_go_{i}.png', color_key=-1),
                                             (60, 65)) for i in range(1, 5)],
         'right_stand': [pygame.transform.scale(load_image(f'bear_left/bear_{i}.png', color_key=-1),
                                                (60, 65)) for i in range(1, 5)],
         'right_death': [pygame.transform.scale(load_image(f'bear_left/bear_death_{i}.png', color_key=-1),
                                                (60, 56)) for i in range(1, 4)]},
    'hero':
        {'left_go': [pygame.transform.scale(load_image(f'hero_left\hero_go_{i}.png', color_key=-1),
                                            (32, 50)) for i in range(1, 7)],
         'left_attack': [pygame.transform.scale(load_image(f'hero_left\hero_attack_{i}.png', color_key=-1),
                                                (32, 50)) for i in range(1, 2)],
         'left_stand': [pygame.transform.scale(load_image(f'hero_left\hero_stand_{i}.png', color_key=-1),
                                               (32, 50)) for i in range(1, 7)],
         'left_death': [pygame.transform.scale(load_image(f'hero_left\hero_dead_left_{i}.png', color_key=-1),
                                               (32, 50)) for i in range(1, 2)],
         'right_go': [pygame.transform.scale(load_image(f'hero_right\hero_go_{i}.png', color_key=-1),
                                             (32, 50)) for i in range(1, 7)],
         'right_attack': [pygame.transform.scale(load_image(f'hero_right\hero_attack_{i}.png', color_key=-1),
                                                 (32, 50)) for i in range(1, 2)],
         'right_stand': [pygame.transform.scale(load_image(f'hero_right\hero_stand_{i}.png', color_key=-1),
                                                (32, 50)) for i in range(1, 7)],
         'right_death': [pygame.transform.scale(load_image(f'hero_right\hero_dead_{i}.png', color_key=-1),
                                                (32, 50)) for i in range(1, 4)]},
    'interface':
        {
            'money': pygame.transform.scale(load_image('interface/money.png', color_key=-1), (60, 60))
         },
    'items':
        {
            'iron_sword': pygame.transform.scale(load_image('money.png', color_key=-1), (60, 60))
        }
}

sprites['slime']['left_stand'].append(
    pygame.transform.scale(load_image(f'slime_left\slime_stand_{3}.png', color_key=-1), (40, 70)))
sprites['slime']['left_stand'].append(
    pygame.transform.scale(load_image(f'slime_left\slime_stand_{4}.png', color_key=-1), (40, 75)))
sprites['slime']['right_stand'].append(
    pygame.transform.scale(load_image(f'slime_right\slime_stand_{3}.png', color_key=-1), (40, 70)))
sprites['slime']['right_stand'].append(
    pygame.transform.scale(load_image(f'slime_right\slime_stand_{4}.png', color_key=-1), (40, 75)))

sprites['hero']['left_attack'].append(
    pygame.transform.scale(load_image(f'hero_left\hero_attack_{1}.png', color_key=-1), (32, 50)))
sprites['hero']['left_attack'].append(
    pygame.transform.scale(load_image(f'hero_left\hero_attack_{2}.png', color_key=-1), (45, 52)))
sprites['hero']['right_attack'].append(
    pygame.transform.scale(load_image(f'hero_right\hero_attack_{1}.png', color_key=-1), (32, 50)))
sprites['hero']['right_attack'].append(
    pygame.transform.scale(load_image(f'hero_right\hero_attack_{2}.png', color_key=-1), (45, 52)))
