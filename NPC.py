from settings import *
from math import hypot
from images import sprites


class Dealer(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(NPC_group, all_sprites)
        self.image = sprites['NPC']['dealer'][0]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)
        self.own_interface = False
        self.frames_stand = 0

    def update(self, player):
        pic_ind = self.frames_stand // (FPS // len(sprites['NPC']['dealer']))
        self.frames_stand = (self.frames_stand + 1) % FPS
        self.image = sprites['NPC']['dealer'][pic_ind]
        if not self.own_interface:
            distance = hypot(abs(player.rect.x - self.rect.x), abs(player.rect.y - self.rect.y))
            if distance < 100:
                mouse_position = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_position) and pygame.event.poll().type == pygame.MOUSEBUTTONDOWN:
                    self.own_interface = True
        else:
            self.interface()

    def interface(self):
        print('right')
        self.own_interface = False
