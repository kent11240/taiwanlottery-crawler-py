from typing import List

from model.prize import Prize


class Scratch:
    def __init__(self, sid: str, name: str, bet: int, prizes: List[Prize], total_amount: int):
        self.sid = sid
        self.name = name
        self.bet = bet
        self.prizes = prizes
        self.total_amount = total_amount

    def to_dict(self):
        return {
            "sid": self.sid,
            "name": self.name,
            "bet": self.bet,
            "prizes": [prize.to_dict() for prize in self.prizes],
            "total_amount": self.total_amount
        }
