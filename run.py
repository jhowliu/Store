from app.crawler import CenturyCrawler, SinYiCrawler
from app.parser import CenturyParser, SinYiParser
from app.orm import insert_store, insert_employee

if __name__ == '__main__':

    # 21 Century
    century_crawler = CenturyCrawler()
    century_stores = century_crawler.start()
    century_parser = CenturyParser()

    for ix, store in enumerate(century_stores):
        print('No. %d' % ix)
        century_parser.set_content(store['link'], store['html'])
        store, employees = century_parser.start_parse()

        insert_store(store)
        for emp in employees:
            insert_employee(emp)

    # SinYi
    sinyi_crawler = SinYiCrawler()
    sinyi_stores = sinyi_crawler.start()
    sinyi_parser = SinYiParser()

    for ix, store in enumerate(sinyi_stores):
        print('No. %d' % (ix+1))
        sinyi_parser.set_content(store['link'], store['html'])
        store = sinyi_parser.start_parse()

        insert_store(store)
