from chrome_trex.core.multi_dino_game import MultiDinoGame


class DinoGame(MultiDinoGame):
    def __init__(self, fps=60):
        super().__init__(1, fps)

    def step(self, action):
        return super().step([action])

    def get_score(self):
        return self.get_scores()[0]

    def get_state(self):
        return super().get_state()[0]
