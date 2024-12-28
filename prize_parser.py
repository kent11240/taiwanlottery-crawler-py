import re

from bs4 import BeautifulSoup


class PrizeParser:

    def parse(self, scratch_id, content):
        soup = BeautifulSoup(content, 'html.parser')
        prize_table_data = self._get_prize_table_data(soup, scratch_id)

        prizes = self._extract_prizes(prize_table_data)
        total_amount = self._extract_total_amount(prize_table_data)

        return {
            "prizes": prizes,
            "total_amount": total_amount
        }

    def _get_prize_table_data(self, soup, scratch_id):
        anchor = soup.find('a', id=str(scratch_id))
        if not anchor:
            raise Exception(f"No anchor found with id: {scratch_id}")
        return anchor.find_parent().find_parent().find_all('td')

    def _extract_prizes(self, prize_table_data):
        if len(prize_table_data) < 4:
            return []

        win_indices = [0, 2]
        amount_indices = [1, 3]

        all_wins = self._extract_wins(prize_table_data, win_indices)
        all_amounts = self._extract_amounts(prize_table_data, amount_indices)

        return [
            {"win": win, "amount": amount} for win, amount in zip(all_wins, all_amounts)
        ]

    def _extract_wins(self, prize_table_data, indices):
        return [
            int(match.group(1).replace(",", ""))
            for index in indices
            for li in prize_table_data[index].find_all("li")
            if (match := re.search(r"NT\$([\d,]+)", li.get_text(strip=True)))
        ]

    def _extract_amounts(self, prize_table_data, indices):
        return [
            int(li.get_text(strip=True).replace(",", ""))
            for index in indices
            for li in prize_table_data[index].find_all("li")
            if li.get_text(strip=True)
        ]

    def _extract_total_amount(self, prize_table_data):
        for i, td in enumerate(prize_table_data):
            if td.get_text(strip=True) == "發行張數":
                return int(prize_table_data[i + 1].get_text(strip=True).replace(",", ""))
        return 0
