import json

from prize_parser import PrizeParser
from taiwanlottery_crawler import TaiwanLotteryCrawler

if __name__ == "__main__":
    prize_parser = PrizeParser()
    crawler = TaiwanLotteryCrawler(prize_parser)

    scratches = crawler.run()
    print(json.dumps([scratch.to_dict() for scratch in scratches], ensure_ascii=False, indent=2))
