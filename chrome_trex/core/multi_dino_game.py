import itertools
import random

import pygame
from chrome_trex.constants import (  # noqa: F401
    ACTION_DOWN,
    ACTION_FORWARD,
    ACTION_UP,
    BACKGROUND_COL,
    HEIGHT,
    SPRITE_SCALE_Y,
    WIDTH,
)
from chrome_trex.core.objects.cactus import Cactus
from chrome_trex.core.objects.cloud import Cloud
from chrome_trex.core.objects.dino import Dino
from chrome_trex.core.objects.ground import Ground
from chrome_trex.core.objects.ptera import Ptera
from chrome_trex.core.objects.scoreboard import Scoreboard
from chrome_trex.helpers import load_sprite_sheet


class MultiDinoGame:
    def __init__(self, dino_count, fps=60):
        self.high_score = 0
        self.fps = fps
        self.dino_count = dino_count
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("T-Rex Rush")
        self.reset()

    def reset(self):
        self.gamespeed = 4
        self.game_over = False
        self.new_ground = Ground(-1 * self.gamespeed)
        self.scb = Scoreboard()
        self.highsc = Scoreboard(WIDTH * 0.78)
        self.counter = 0

        self.player_dinos = [Dino(44, 47) for _ in range(self.dino_count)]
        self.alive_players = self.player_dinos[:]
        self.last_dead_player = None
        self.cacti = pygame.sprite.Group()
        self.pteras = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.last_obstacle = pygame.sprite.Group()

        Cactus.containers = self.cacti
        Ptera.containers = self.pteras
        Cloud.containers = self.clouds

        temp_images, temp_rect = load_sprite_sheet(
            "numbers.png", 12, 1, 11, SPRITE_SCALE_Y, -1
        )
        self.HI_image = pygame.Surface((22, SPRITE_SCALE_Y))
        self.HI_rect = self.HI_image.get_rect()
        self.HI_image.fill(BACKGROUND_COL)
        self.HI_image.blit(temp_images[10], temp_rect)
        temp_rect.left += temp_rect.width
        self.HI_image.blit(temp_images[11], temp_rect)
        self.HI_rect.top = HEIGHT * 0.1
        self.HI_rect.left = WIDTH * 0.73

        # Update the screen
        self.step([ACTION_FORWARD for _ in range(self.dino_count)])

    def get_image(self):
        return pygame.surfarray.array3d(self.screen)

    def step(self, actions):
        if pygame.display.get_surface() is None:
            print("Couldn't load display surface")
            self.game_over = True
            return

        for player, action in zip(self.player_dinos, actions):
            if player.is_dead:
                continue
            if action == ACTION_FORWARD:
                player.is_ducking = False
            if action == ACTION_UP:
                if player.rect.bottom == int(0.98 * HEIGHT):
                    player.is_jumping = True
                    player.movement[1] = -player.jump_speed
            elif action == ACTION_DOWN:
                if not (player.is_jumping and player.is_dead):
                    player.is_ducking = True

        for sprite in itertools.chain(self.cacti, self.pteras):
            sprite.movement[0] = -self.gamespeed
            for player in self.alive_players[:]:
                if pygame.sprite.collide_mask(player, sprite):
                    player.is_dead = True
                    self.alive_players.remove(player)
                    self.last_dead_player = player

        if len(self.cacti) < 2:
            if len(self.cacti) == 0:
                self.last_obstacle.empty()
                self.last_obstacle.add(Cactus(self.gamespeed, 40, 40))
            else:
                for last_obstacle in self.last_obstacle:
                    if (
                        last_obstacle.rect.right < WIDTH * 0.7
                        and random.randrange(0, 50) == 10
                    ):
                        self.last_obstacle.empty()
                        self.last_obstacle.add(Cactus(self.gamespeed, 40, 40))

        if (
            len(self.pteras) == 0
            and random.randrange(0, 200) == 10
            and self.counter > 500
        ):
            for last_obstacle in self.last_obstacle:
                if last_obstacle.rect.right < WIDTH * 0.8:
                    self.last_obstacle.empty()
                    self.last_obstacle.add(Ptera(self.gamespeed, 46, 40))

        if len(self.clouds) < 5 and random.randrange(0, 300) == 10:
            Cloud(WIDTH, random.randrange(HEIGHT / 5, HEIGHT / 2))

        for player in self.alive_players:
            player.update()
        self.cacti.update()
        self.pteras.update()
        self.clouds.update()
        self.new_ground.update()
        self.scb.update(max(self.get_scores()))
        self.highsc.update(self.high_score)

        self.screen.fill(BACKGROUND_COL)
        self.new_ground.draw()
        self.clouds.draw(self.screen)
        self.scb.draw()
        if self.high_score != 0:
            self.highsc.draw()
            self.screen.blit(self.HI_image, self.HI_rect)
        self.cacti.draw(self.screen)
        self.pteras.draw(self.screen)

        for player in self.alive_players:
            player.draw()
        if len(self.alive_players) == 0:
            self.last_dead_player.draw()

        pygame.display.update()
        self.clock.tick(self.fps)

        if len(self.alive_players) == 0:
            self.game_over = True
            max_score = max(self.get_scores())
            if max_score > self.high_score:
                self.high_score = max_score

        if self.counter % 700 == 699:
            self.new_ground.speed -= 1
            self.gamespeed += 1

        self.counter = self.counter + 1

    def get_state(self):
        """
        There can be up to 02 Cacti and 01 Ptera at the screen at a time.
        Each cactus/ptera sprite is represented as a tuple (X, Y, H).

        This function returns a list of states with 11 values for each dino:
        [[DY, X1, Y1, H1, X2, Y2, H2, X3, Y3, H3, GS]]


        X: is the distance of a Cactus or Ptero from the dinossaur in the X axis;
        Y: is the position of a Cactus or Ptero in screen for the Y axis; and
        H: is the height of the sprite.

        DY is the position of the dinossaur in the Y axis (the only difference
        between each dinossaur).

        GS is the Game Speed.

        The nearest object is in X1, Y1, H1. The farthest is X3, Y3, H3.
        """

        def _get_state(dino_number):
            w = self.screen.get_width()
            h = self.screen.get_height()

            def get_coords(sprites, min_size):
                cs = []
                for sprite in sprites:
                    X_distance_from_dino = (
                        sprite.rect.centerx
                        - self.player_dinos[dino_number].rect.centerx
                    ) / w
                    Y_position_in_screen = sprite.rect.centery / h
                    Height = sprite.rect.height / h
                    if (
                        sprite.rect.centerx
                        > self.player_dinos[dino_number].rect.centerx
                    ):
                        cs += [(X_distance_from_dino, Y_position_in_screen, Height)]
                return cs + [(1, 0, 0)] * (min_size - len(cs))

            coords = get_coords(self.cacti, 2) + get_coords(self.pteras, 1)
            ordered_coords = sorted(coords, key=lambda x: x[0])
            state = (
                [self.player_dinos[dino_number].rect.centery / h]
                + [c for cs in ordered_coords for c in cs]
                + [self.gamespeed / w]
            )
            return state

        return [_get_state(dino_number) for dino_number in range(self.dino_count)]

    def get_scores(self):
        return [player.score for player in self.player_dinos]

    def close(self):
        pygame.quit()
