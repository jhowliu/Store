# -*-coding:utf8 -*-
import re
import requests

from bs4 import BeautifulSoup

class CenturyCrawler(object):
    def __init__(self):
        self.__LAST_PAGE_REGEX__ = re.compile(u'共([0-9 ]+)頁')
        self.__BASE_URL__ = 'http://www.century21.com.tw/index/About/Store'

    def start(self):
        stores = []
        store_links = []
        page_links = self._get_all_page_links(self.__BASE_URL__)

        # get all store links
        for link in page_links:
            page, _ = self._get_page(link)
            links = self._get_store_link(page)
            store_links.extend(links)

        # get all store pages
        for link in store_links:
            if link=='': continue
            print('Start crawling %s' % link)
            _, url = self._get_page(link)
            page, _ = self._get_page('/'.join([url, '/AboutUS/Team']))
            stores.append({ 'link': link, 'html': page })

        print('There has %d stores' % len(stores))

        return stores

    def _get_store_link(self, page):
        store_links = []
        soup = BeautifulSoup(page, 'html.parser')

        for div in soup.select('div.w-1'):
            info = div.select('.infoBox h3 a')
            if len(info):
                store_link = info[0]['href']
                store_links.append(store_link)

        return store_links

    def _get_page(self, url):
        resp = requests.get(url)
        resp.encoding = 'utf-8'

        return resp.text, resp.url

    def _get_all_page_links(self, home_url):
        links = []
        last_page_num = 1
        page, _ = self._get_page(home_url)
        soup = BeautifulSoup(page, 'html.parser')
        # get total number of pages
        total_page = self.__LAST_PAGE_REGEX__.search(soup.select(".totalPage")[0].text)

        if total_page:
        	last_page_num = int(total_page.group(1).strip())

        for page_num in xrange(1, last_page_num+1):
        	links.append(home_url+'?page='+str(page_num))

        return links
