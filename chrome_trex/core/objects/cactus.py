import random

import pygame
from chrome_trex.constants import HEIGHT, WIDTH
from chrome_trex.helpers import load_sprite_sheet


class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet(
            "cacti-small.png", 3, 1, sizex, sizey, -1
        )
        self.rect.bottom = int(0.98 * HEIGHT)
        self.rect.left = WIDTH + self.rect.width
        self.image = self.images[random.randrange(0, 3)]
        self.movement = [-1 * speed, 0]

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()
