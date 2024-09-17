import random
from typing import Optional, Tuple

import pygame
from chrome_trex.constants import HEIGHT, WIDTH
from chrome_trex.helpers import load_sprite_sheet


class Dino:
    def __init__(
        self, sizex=-1, sizey=-1, color: Optional[Tuple[int, int, int]] = None
    ):
        self.running_dino_images, self.rect = load_sprite_sheet(
            "dino.png", 5, 1, sizex, sizey, -1
        )
        self.ducking_dino_images, self.rect1 = load_sprite_sheet(
            "dino_ducking.png", 2, 1, 59, sizey, -1
        )
        self.rect.bottom = int(0.98 * HEIGHT)
        self.rect.left = WIDTH / 15
        self.image = self.running_dino_images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.is_jumping = False
        self.is_dead = False
        self.is_ducking = False
        self.is_blinking = False
        self.movement = [0, 0]
        self.jump_speed = 11.5
        self.gravity = 0.6

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

        self.colorize(color)

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.98 * HEIGHT):
            self.rect.bottom = int(0.98 * HEIGHT)
            self.is_jumping = False

    def update(self):
        if self.is_jumping:
            self.movement[1] = self.movement[1] + self.gravity

        if self.is_jumping:
            self.index = 0
        elif self.is_blinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1) % 2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1) % 2

        elif self.is_ducking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2

        if self.is_dead:
            self.index = 4

        if not self.is_ducking:
            self.image = self.running_dino_images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.ducking_dino_images[(self.index) % 2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.is_dead and self.counter % 7 == 6 and not self.is_blinking:
            self.score += 1

        self.counter = self.counter + 1

    def colorize(self, color: Optional[Tuple[int, int, int]] = None):
        def _apply_color(image, color):
            color_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            color_surface.fill((color))
            colored_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            colored_image.blit(image, (0, 0))
            colored_image.blit(
                color_surface, (0, 0), special_flags=pygame.BLENDMODE_BLEND
            )
            return colored_image

        def _generate_random_color() -> Tuple:
            color = [
                random.randint(0, 150),
                random.randint(50, 230),
                random.randint(50, 230),
            ]
            random.shuffle(color)
            return tuple(color)

        if not color:
            color = _generate_random_color()

        self.running_dino_images = [
            _apply_color(img, color) for img in self.running_dino_images
        ]
        self.ducking_dino_images = [
            _apply_color(img, color) for img in self.ducking_dino_images
        ]
