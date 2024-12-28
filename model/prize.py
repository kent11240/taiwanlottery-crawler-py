class Prize:
    def __init__(self, win: int, amount: int):
        self.win = win
        self.amount = amount

    def to_dict(self):
        return {
            "win": self.win,
            "amount": self.amount
        }
