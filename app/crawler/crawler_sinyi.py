# -*- coding:utf8 -*-
import re
import requests

from bs4 import BeautifulSoup


class SinYiCrawler(object):
    def __init__(self):
        self.__BASE_URL__ = "http://branch.sinyi.com.tw/index.php"
        self.__LAST_PAGE_REGEX = re.compile('index.php\/([0-9])+\/')

    # entry point
    def _get_cities_links(self):
        # magic number
        city_ids = xrange(1, 8)
        city_links = [
            '/'.join([self.__BASE_URL__, '1', str(id_) ])
            for id_ in city_ids
        ]

        return city_links

    # get pages which has list of stores
    def _get_all_page_links(self, page, city_code):
        last_page_num = 1
        soup = BeautifulSoup(page, "html.parser")

        last_page_tag = soup.find(class_='next')

        if last_page_tag:
            last_page_num = self.__LAST_PAGE_REGEX.search(last_page_tag.find('a')['href']).group(1)

        return [
            '/'.join([self.__BASE_URL__, str(page_num), str(city_code)])
            for page_num in range(1, int(last_page_num)+1)
        ]

    def _get_page(self, url):
        resp = requests.get(url)
        resp.encoding = 'utf-8'

        return resp.text

    def _get_store_links(self, page):
        store_links = []
        store_path_rex = re.compile('info.php\/([A-Za-z0-9]+)\/')
        store_baseURL = "http://branch.sinyi.com.tw/info.php/"

        soup = BeautifulSoup(page, "html.parser")
        stores = soup.tbody.find_all('a')

        for store in stores:
            match = store_path_rex.search(store['href'])
            if match:
                store_links.append(store_baseURL+match.group(1))

        return store_links


    def start(self):
        # First: Get all pages for city
        city_links = self._get_cities_links()
        print(city_links)
        print("Start crawling list of store pages")
        # Second: Get all list of store page
        all_page_links = []
        for id_, city_link in enumerate(city_links):
            print(city_link)
            page = self._get_page(city_link)
            all_page_links.extend(self._get_all_page_links(page, id_+1))

        # Third: Get all store pages
        print("Start crawling store pages")
        store_links = []
        for page_link in all_page_links:
            print(page_link)
            page = self._get_page(page_link)
            links = self._get_store_links(page)
            store_links.extend(links)

        print("Start crawling html")
        # Final: Create the htmls
        stores = []
        for store_link in store_links:
            print(store_link)
            page = self._get_page(store_link)
            stores.append({ 'link': store_link, 'html': page })

        return stores
