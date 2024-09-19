import os
import random
import pkgutil
import io
import contextlib
import itertools

with contextlib.redirect_stdout(None):
    import pygame
    from pygame import *

__author__ = "Shivam Shekhar"

ACTION_FORWARD = 2
ACTION_UP = 0
ACTION_DOWN = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND_COL = WHITE

WIDTH, HEIGHT = 600, 150


def load_image(name, sizex=-1, sizey=-1, colorkey=None):
    fullname = os.path.join('sprites', name)
    image = pygame.image.load(io.BytesIO(
        pkgutil.get_data('chrome_trex', fullname)), fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())


def load_sprite_sheet(sheetname, nx, ny, scalex=-1, scaley=-1, colorkey=None):
    fullname = os.path.join('sprites', sheetname)
    sheet = pygame.image.load(io.BytesIO(
        pkgutil.get_data('chrome_trex', fullname)), fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0, ny):
        for j in range(0, nx):
            rect = pygame.Rect((j*sizex, i*sizey, sizex, sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet, (0, 0), rect)

            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image, (scalex, scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect


def extract_digits(number):
    if number > -1:
        digits = []
        i = 0
        while(number/10 != 0):
            digits.append(number % 10)
            number = int(number/10)

        digits.append(number % 10)
        for i in range(len(digits), 5):
            digits.append(0)
        digits.reverse()
        return digits


class Dino():
    def __init__(self, sizex=-1, sizey=-1):
        self.images, self.rect = load_sprite_sheet(
            'dino.png', 5, 1, sizex, sizey, -1)
        self.images1, self.rect1 = load_sprite_sheet(
            'dino_ducking.png', 2, 1, 59, sizey, -1)
        self.rect.bottom = int(0.98*HEIGHT)
        self.rect.left = WIDTH/15
        self.image = self.images[0]
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

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.98*HEIGHT):
            self.rect.bottom = int(0.98*HEIGHT)
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
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[(self.index) % 2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.is_dead and self.counter % 7 == 6 and not self.is_blinking:
            self.score += 1

        self.counter = (self.counter + 1)


class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet(
            'cacti-small.png', 3, 1, sizex, sizey, -1)
        self.rect.bottom = int(0.98*HEIGHT)
        self.rect.left = WIDTH + self.rect.width
        self.image = self.images[random.randrange(0, 3)]
        self.movement = [-1*speed, 0]

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()


class Ptera(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet(
            'ptera.png', 2, 1, sizex, sizey, -1)
        self.ptera_height = [HEIGHT*0.82, HEIGHT*0.75, HEIGHT*0.60]
        self.rect.centery = self.ptera_height[random.randrange(0, 3)]
        self.rect.left = WIDTH + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1) % 2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()


class Ground():
    def __init__(self, speed=-5):
        self.image, self.rect = load_image('ground.png', -1, -1, -1)
        self.image1, self.rect1 = load_image('ground.png', -1, -1, -1)
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


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image('cloud.png', int(90*30/42), 30, -1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed, 0]

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Scoreboard():
    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.tempimages, self.temprect = load_sprite_sheet(
            'numbers.png', 12, 1, 11, int(11*6/5), -1)
        self.image = pygame.Surface((55, int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = WIDTH*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = HEIGHT*0.1
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


class MultiDinoGame:
    def __init__(self, dino_count, fps=60):
        self.high_score = 0
        self.fps = fps
        self.obstacles = []
        self.dino_count = dino_count
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("T-Rex Rush")
        self.font = pygame.font.Font(None, 24)  # Inicializa a fonte padrão com tamanho 24
        self.reset()

    def reset(self):
        self.gamespeed = 4
        self.game_over = False
        self.obstacles = []
        self.new_ground = Ground(-1*self.gamespeed)
        self.scb = Scoreboard()
        self.highsc = Scoreboard(WIDTH*0.78)
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
            'numbers.png', 12, 1, 11, int(11*6/5), -1)
        self.HI_image = pygame.Surface((22, int(11*6/5)))
        self.HI_rect = self.HI_image.get_rect()
        self.HI_image.fill(BACKGROUND_COL)
        self.HI_image.blit(temp_images[10], temp_rect)
        temp_rect.left += temp_rect.width
        self.HI_image.blit(temp_images[11], temp_rect)
        self.HI_rect.top = HEIGHT*0.1
        self.HI_rect.left = WIDTH*0.73

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
            player.is_ducking = False    
            if action == ACTION_UP:
                if player.rect.bottom == int(0.98*HEIGHT):
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

        obstaculos = len(self.cacti) + len(self.pteras)
        #print(obstaculos)
        MIN_DISTANCE = 200 * self.gamespeed  # Distância mínima entre os obstáculos
        if obstaculos < 3:
            if obstaculos == 0:
                self.last_obstacle.empty()
                randomvalor = random.randrange(0, 50)
                if randomvalor > 24:
                    self.last_obstacle.add(Cactus(self.gamespeed, 40, 40))
                elif randomvalor <= 24:
                    self.last_obstacle.add(Ptera(self.gamespeed, 46, 40))
            else:
                for l in self.last_obstacle:
                    if l.rect.right < WIDTH*0.7 and random.randrange(0, 50) > 24 and l.rect.left < WIDTH - MIN_DISTANCE:
                        self.last_obstacle.empty()
                        self.last_obstacle.add(Cactus(self.gamespeed, 40, 40))
                    elif l.rect.right < WIDTH*0.7 and random.randrange(0, 50) <= 24 and l.rect.left < WIDTH - MIN_DISTANCE:
                        self.last_obstacle.empty()
                        self.last_obstacle.add(Ptera(self.gamespeed, 46, 40))
        

        if len(self.clouds) < 5 and random.randrange(0, 300) == 10:
            Cloud(WIDTH, random.randrange(HEIGHT//5, HEIGHT//2))

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

        # Renderiza o gamespeed
        gamespeed_text = self.font.render(f'Game Speed: {self.gamespeed}', True, (0, 0, 0))
        self.screen.blit(gamespeed_text, (10, 10))  # Posição (10, 10) na tela

        pygame.display.update()
        self.clock.tick(self.fps)
        if max(self.get_scores()) > 10000:
            self.game_over = True
        if len(self.alive_players) == 0:
            self.game_over = True
            max_score = max(self.get_scores())
            if max_score > self.high_score:
                self.high_score = max_score

        if self.counter % 700 == 699 and self.gamespeed < 12:
            self.new_ground.speed -= 1
            self.gamespeed += 1

        self.counter = (self.counter + 1)

    
    def get_state(self):
        """
        This function returns a list of states with 8 values for each dino:
        [[DY, X1, Y1, H1, W1, X2, Y2, H2, W2, GS]]
            
        DY: Distance in Y of the dinosaur.
        X1, Y1: Distance in X and Y from the first closest obstacle.
        H1: Height of the first closest obstacle.
        X2, Y2: Distance in X and Y from the second closest obstacle.
        H2: Height of the second closest obstacle.
        GS: Game speed.
        """
        
        def _get_state(dino_number):
            w = self.screen.get_width()
            h = self.screen.get_height()

            def get_coords(sprites, max_obstacles):
                coords = []
                for sprite in sprites:
                    X_distance_from_dino = (sprite.rect.centerx - self.player_dinos[dino_number].rect.centerx) / w
                    Y_distance_from_dino = (sprite.rect.centery - self.player_dinos[dino_number].rect.centery) / h
                    Height = sprite.rect.height / h
                    Width = sprite.rect.width / w
                    # Consider only obstacles that are in front of the dino
                    if X_distance_from_dino > 0:
                        coords.append((X_distance_from_dino, Y_distance_from_dino, Height, Width))

                # Return at most max_obstacles, padding if necessary
                coords = sorted(coords, key=lambda x: x[0])[:max_obstacles]
                return coords + [(1, 0, 0,0)] * (max_obstacles - len(coords))  # Pad with dummy values if less obstacles

            # Get the closest two obstacles (cacti and pteras combined)
            obstacles = get_coords(self.cacti, 2) + get_coords(self.pteras, 2)
            ordered_coords = sorted(obstacles, key=lambda x: x[0])[:2]  # Take the closest two obstacles
            
            # Flatten the obstacle coordinates
            state = [self.player_dinos[dino_number].rect.centery / h] + \
                    [c for obstacle in ordered_coords for c in obstacle] + \
                    [self.gamespeed / w]
            
            return state

        return [_get_state(dino_number) for dino_number in range(self.dino_count)]


    def get_scores(self):
        return [player.score for player in self.player_dinos]

    def close(self):
        pygame.quit()



class DinoGame(MultiDinoGame):
    def __init__(self, fps=60):
        super().__init__(1, fps)

    def step(self, action):
        return super().step([action])

    def get_score(self):
        return self.get_scores()[0]

    def get_state(self):
        return super().get_state()[0]
