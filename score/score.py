class Score:

    def __init__(self):
        self.score = 0
        self.pellet_score = 25

    def add_score(self):
        self.score += self.pellet_score

    def add_spec_score(self, score: int):
        self.score += score

    def __str__(self):
        return "Score: " + str(self.score)


