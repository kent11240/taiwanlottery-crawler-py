import csv
import sys


class CSVPrinter:

    def print(self, data):
        headers = ["Name", "Bet", "Winning Rate", "Break-even Rate", "Break-even Rate", "Expected Value", "RTP"]
        writer = csv.writer(sys.stdout)
        writer.writerow(headers)
        for stat in data:
            writer.writerow([
                stat["name"],
                stat["bet"],
                stat["winning_rate"],
                stat["break_even_rate"],
                stat["profitability_rate"],
                stat["expected_value"],
                stat["rtp"]
            ])
