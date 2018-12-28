from ..DinoGame import DinoGame
import gym

class ChromeTrexEnv(gym.Env):
    def __init__(self):
        self.game = DinoGame(FPS=0)
    def step(self, action):
        if not self.game.gameOver:
            self.game.step(action)
        reward = -1 if self.game.gameOver else 1
        ob = self.game.get_image()
        return ob, reward, self.game.gameOver, {}
    def reset(self):
        self.game.reset()

    def __enters__(self):
        return self
    
    def __exits__(self, type, value, traceback):
        self.game.close()
