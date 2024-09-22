import io
import os
import pkgutil
from typing import List

import pygame


def load_image(name, sizex=-1, sizey=-1, colorkey=None):
    fullname = os.path.join("sprites", name)
    image = pygame.image.load(
        io.BytesIO(pkgutil.get_data("chrome_trex", fullname)), fullname
    )
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())


def load_sprite_sheet(sheetname, nx, ny, scalex=-1, scaley=-1, colorkey=None):
    fullname = os.path.join("sprites", sheetname)
    sheet = pygame.image.load(
        io.BytesIO(pkgutil.get_data("chrome_trex", fullname)), fullname
    )
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width / nx
    sizey = sheet_rect.height / ny

    for i in range(0, ny):
        for j in range(0, nx):
            rect = pygame.Rect((j * sizex, i * sizey, sizex, sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet, (0, 0), rect)

            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pygame.RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image, (scalex, scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect


def extract_digits(number: int) -> List[int]:
    return list(map(int, list(str(number).zfill(5))))
