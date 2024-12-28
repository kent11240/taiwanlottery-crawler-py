from csv_printer import CSVPrinter
from prize_parser import PrizeParser
from scratch_statistics import ScratchStatistics
from taiwanlottery_crawler import TaiwanLotteryCrawler

if __name__ == "__main__":
    prize_parser = PrizeParser()
    crawler = TaiwanLotteryCrawler(prize_parser)
    statistics = ScratchStatistics()
    csv_printer = CSVPrinter()

    scratches = crawler.run()
    statistics_data = statistics.calculate(scratches)
    csv_printer.print(statistics_data)
