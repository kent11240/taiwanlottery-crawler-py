class ScratchStatistics:

    def calculate(self, scratches):
        results = []

        for scratch in scratches:
            total_tickets = scratch.total_amount

            winning_tickets = sum(prize.amount for prize in scratch.prizes)
            winning_rate = f"{round((winning_tickets / total_tickets) * 100, 2):.2f}%"

            break_even_tickets = sum(prize.amount for prize in scratch.prizes if prize.win >= scratch.bet)
            break_even_rate = f"{round((break_even_tickets / total_tickets) * 100, 2):.2f}%"

            profitable_tickets = sum(prize.amount for prize in scratch.prizes if prize.win > scratch.bet)
            profitability_rate = f"{round((profitable_tickets / total_tickets) * 100, 2):.2f}%"

            total_prize_value = sum(prize.win * prize.amount for prize in scratch.prizes)
            expected_value = round(total_prize_value / total_tickets, 2)

            rtp = f"{round((expected_value / scratch.bet) * 100, 2):.2f}%"

            results.append({
                "name": scratch.name,
                "bet": scratch.bet,
                "winning_rate": winning_rate,
                "break_even_rate": break_even_rate,
                "profitability_rate": profitability_rate,
                "expected_value": expected_value,
                "rtp": rtp
            })

        return results
