import random

import pygame
from chrome_trex.constants import HEIGHT, WIDTH
from chrome_trex.helpers import load_sprite_sheet


class Ptera(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet("ptera.png", 2, 1, sizex, sizey, -1)
        self.ptera_height = [HEIGHT * 0.82, HEIGHT * 0.75, HEIGHT * 0.60]
        self.rect.centery = self.ptera_height[random.randrange(0, 3)]
        self.rect.left = WIDTH + self.rect.width
        self.image = self.images[0]
        self.movement = [-1 * speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = self.counter + 1
        if self.rect.right < 0:
            self.kill()
