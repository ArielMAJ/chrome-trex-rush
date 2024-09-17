import pygame
from chrome_trex.constants import BACKGROUND_COL, HEIGHT, SPRITE_SCALE_Y, WIDTH
from chrome_trex.helpers import extract_digits, load_sprite_sheet


class Scoreboard:
    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.tempimages, self.temprect = load_sprite_sheet(
            "numbers.png", 12, 1, 11, SPRITE_SCALE_Y, -1
        )
        self.image = pygame.Surface((55, SPRITE_SCALE_Y))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = WIDTH * 0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = HEIGHT * 0.1
        else:
            self.rect.top = y

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)

    def update(self, score):
        score_digits = extract_digits(score)
        self.image.fill(BACKGROUND_COL)
        for s in score_digits:
            self.image.blit(self.tempimages[s], self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0
