# -*- coding:utf8 -*-
import re
import hashlib
import requests

from bs4 import BeautifulSoup

from app.lib.template import StoreParser
from app.lib.schema import *
from app.lib.utils import split_address
from app.lib.log import Logger

class CenturyParser(StoreParser):

    def init(self):
        self.casefrom = 'Century21'
        self.logger = Logger('Century21.log')

    def set_content(self, url, html):
        self.html = html
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.url = url

    def start_parse(self):
        self.logger.info('Start parse %s.' % self.url)
        store_infos = self.fill_out_webstored()
        emp_list = []
        tags = self.soup.select('.team-mem')

        self.logger.info('There has %d employees in %s.' % (len(tags), self.get_store_name()))
        for ix, tag in enumerate(tags):
            emp_list.append(self.fill_out_webagent(tag, ix+1))

        return store_infos, emp_list

    # employee primary key
    def get_employee_hash_id(self, soup):
        concated = u"-".join([self.get_store_id(), self.get_employee_name(soup), self.date])
        return hashlib.sha1(concated.encode('utf8')).hexdigest()

    # store primary key
    def get_store_hash_id(self):
        hashid = hashlib.sha1('%s-%s-%s' % (self.casefrom, self.get_store_id(), self.date)).hexdigest()
        return hashid

    def get_store_link(self):
        return self.url

    def get_store_id(self):
        store_id_regex = re.compile('http:\/\/([0-9A-Za-z]+)\.century21\.com\.tw')
        m = store_id_regex.search(self.url)
        store_id = m.group(1) if m else ''
        return store_id

    def get_store_name(self):
        tags = self.soup.select('h3')
        store_name = tags[0].text if len(tags) else ''
        return store_name

    def get_address(self):
        tags = self.soup.select('.store-add')
        addr = tags[0].text if len(tags) else ''
        return addr

    def get_tel_number(self):
        tags = self.soup.select('.store-tel')
        tel = tags[0].text if len(tags) else ''
        return tel

    def get_mail(self):
        tags = self.soup.select('.small-12.xlarge-11.columns span a')
        mail = tags[1].text if len(tags)>1 else ''
        return mail.replace('\n', '')

    def get_fax_number(self):
        tags = self.soup.select('.small-12.xlarge-11.columns span')
        fax = tags[3].text if len(tags)>3 else ''
        fax = fax.replace(u'傳真：', '')
        return fax

    def get_case_system(self):
        tags = self.soup.select('.small-12.xlarge-11.columns span')
        system = tags[0].text if len(tags) else ''
        return system

    def get_employee(self, soup):
        return fill_out_webagent(soup)

    def get_employee_name(self, soup):
        tags = soup.select('h6')
        name = tags[0].text if len(tags) else ''
        # need to replace license if there has license
        license = self.get_employee_license(soup)
        return name.replace(license, '')

    def get_employee_mail(self, soup, ix):
        tags = soup.select('#mail-box%d'%ix)
        mail = tags[0].text if len(tags) else ''
        return mail.replace('\n', '')

    def get_employee_mobile(self, soup, ix):
        tags = soup.select('#cell-box%d'%ix)
        mobile = tags[0].text if len(tags) else ''
        return mobile.replace('\n', '')

    def get_employee_license(self, soup):
        tags = soup.select('h6 span')
        tmp = tags[0].text if len(tags) else ''
        license = tags[1].text if len(tags)>1 else tmp
        return license

    def get_employee_title(self, soup):
        tags = soup.select('p.text-center span')
        title = tags[0].text if len(tags) else u'營業員'
        return title

    def get_splited_address(self):
        addr = self.get_address()
        target = split_address(addr)

        city = target['city'] if 'city' in target else ""
        area = target['area'] if 'area' in target else ""

        return city, area


    def fill_out_webstored(self):

        # WEB_STORED
        city, area = self.get_splited_address()

        WEB_STORED['idx'] = self.get_store_hash_id()
        WEB_STORED['KeyinDate'] = self.date
        WEB_STORED['CaseFrom'] = self.casefrom
    	WEB_STORED['ContactStore'] = self.get_store_name()
    	WEB_STORED['ContactStoreID'] = self.get_store_id()
    	WEB_STORED['ContactTel'] = self.get_tel_number()
    	WEB_STORED['ContactUrl'] = self.get_store_link()
    	WEB_STORED['ContactAddr'] = self.get_address()
    	WEB_STORED['CaseSystem'] = self.get_case_system()
        WEB_STORED['ContactFAX'] = self.get_fax_number()
        WEB_STORED['ContactEMail'] = self.get_mail()
    	WEB_STORED['District'] = area
    	WEB_STORED['City'] = city

        return dict(WEB_STORED)


    def fill_out_webagent(self, soup, ix):
        # WEB_AGENT
    	WEB_AGENT['id'] = self.get_employee_hash_id(soup)
        WEB_AGENT['KeyinDate'] = self.date
        WEB_AGENT['CaseFrom'] = self.casefrom
    	WEB_AGENT['ContactStore'] = self.get_store_name()
    	WEB_AGENT['ContactStoreID'] = self.get_store_id()
    	WEB_AGENT['EmpMobile'] = self.get_employee_mobile(soup, ix)
    	WEB_AGENT['EmpEMail'] = self.get_employee_mail(soup, ix)
    	WEB_AGENT['EmpTitle'] = self.get_employee_title(soup)
    	WEB_AGENT['LicenseB'] = self.get_employee_license(soup)
    	WEB_AGENT['EmpName'] = self.get_employee_name(soup)
    	WEB_AGENT['District'] = WEB_STORED['District']
    	WEB_AGENT['City'] = WEB_STORED['City']

        return dict(WEB_AGENT)
