import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE, pygame.DOUBLEBUF)
FPS = 120
clock = pygame.time.Clock()
tile_width = tile_height = 75

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
items_group = pygame.sprite.Group()
NPC_group = pygame.sprite.Group()
groups = [all_sprites, boxes_group, player_group, enemies_group, ground_group, border_group, portal_group, attack_group]
