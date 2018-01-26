from app.crawler import CenturyCrawler
from app.parser import CenturyParser
from app.orm import insert_store, insert_employee

if __name__ == '__main__':
    crawler = CenturyCrawler()
    stores = crawler.start()
    parser = CenturyParser()

    for ix, store in enumerate(stores):
        print('No. %d', ix)
        parser.set_content(store['link'], store['html'])
        store, employees = parser.start_parse()

        insert_store(store)
        for emp in employees:
            insert_employee(emp)
