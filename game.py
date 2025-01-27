import random

class BloodyDotty:
    def __init__(self):
        self.players = {}
        self.sums = {}
        self.turn = None
        self.game_active = False

    def is_valid_guess(self, player_id, guess):
        return 1000 <= guess <= 9999 and guess not in self.sums[player_id]
