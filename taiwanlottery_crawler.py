import requests

from model.prize import Prize
from model.raw_scratch import RawScratch
from model.scratch import Scratch
from prize_parser import PrizeParser


class TaiwanLotteryCrawler:
    MAX_SCRATCHES_SIZE = 20
    SCRATCHES_URL_TEMPLATE = 'https://api.taiwanlottery.com/TLCAPIWeB/Instant/Result?ScratchName&Start_ListingDate&End_ListingDate&PageNum=1&PageSize={}&Type=1'
    NEWS_URL_TEMPLATE = 'https://api.taiwanlottery.com/TLCAPIWeB/News/Detail/{}'

    def __init__(self, prize_parser: PrizeParser):
        self.__prize_parser = prize_parser

    def run(self):
        raw_scratches = self._get_raw_scratches()
        return self._process_scratches(raw_scratches)

    def _get_raw_scratches(self):
        url = self.SCRATCHES_URL_TEMPLATE.format(self.MAX_SCRATCHES_SIZE)
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data: {response.status_code}")

        data = response.json()
        raw_scratches = []
        for item in data['content']['resultList']:
            raw_scratch = RawScratch(
                sid=item['gameVol'],
                name=item['scratchName'].replace(',', ''),
                bet=item['money'],
                news_id=item['newsId']
            )
            raw_scratches.append(raw_scratch)
        return raw_scratches

    def _process_scratches(self, raw_scratches):
        processed_scratches = []
        news_content_cache = {}

        for raw_scratch in raw_scratches:
            news_content = self._get_news_content(raw_scratch.news_id, news_content_cache)
            parsed_data = self.__prize_parser.parse(raw_scratch.sid, news_content)

            scratch = Scratch(
                sid=raw_scratch.sid,
                name=raw_scratch.name,
                bet=raw_scratch.bet,
                prizes=[Prize(prize['win'], prize['amount']) for prize in parsed_data['prizes']],
                total_amount=parsed_data['total_amount']
            )
            processed_scratches.append(scratch)

        return processed_scratches

    def _get_news_content(self, news_id, cache):
        if news_id not in cache:
            news_url = self.NEWS_URL_TEMPLATE.format(news_id)
            response = requests.get(news_url)
            if response.status_code != 200:
                raise Exception(f"Failed to retrieve news details for {news_id}: {response.status_code}")

            cache[news_id] = response.json()['content']['content']
        return cache[news_id]
