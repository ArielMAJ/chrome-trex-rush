import pygame
from chrome_trex.constants import HEIGHT
from chrome_trex.helpers import load_image


class Ground:
    def __init__(self, speed=-5):
        self.image, self.rect = load_image("ground.png", -1, -1, -1)
        self.image1, self.rect1 = load_image("ground.png", -1, -1, -1)
        self.rect.bottom = HEIGHT
        self.rect1.bottom = HEIGHT
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)
        pygame.display.get_surface().blit(self.image1, self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right
