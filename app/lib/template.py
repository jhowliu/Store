import sys
import time
import hashlib

from schema import WEB_STORED
from schema import WEB_AGENT

from utils import split_address

class StoreParser(object):
    def __init__(self):
        self.date = time.strftime("%Y-%m-%d")
        self.init()

    def init(self):
        pass

    def start_parse(self):
        pass

    # employee primary key
    def get_employee_hash_id(self):
        pass
    def get_store_hash_id(self):
        pass
    def get_store_link(self):
        pass
    def get_store_id(self):
        pass
    def get_store_name(self):
        pass
    def get_address(self):
        pass
    def get_tel_number(self):
        pass
    def get_mail(self):
        pass
    def get_fax_number(self):
        pass
    def get_case_system(self):
        pass

    def get_employee(self, soup):
        return fill_out_webagent(soup)

    def get_employee_name(self, soup):
        pass
    def get_employee_mail(self, soup):
        pass
    def get_employee_mobile(self, soup):
        pass
    def get_employee_license(self, soup):
        pass
    def get_employee_title(self, soup):
        pass

    def get_splited_address(self):
        addr = self.get_address()
        target = split_address(addr)

        city = target['city'] if 'city' in target else ''
        area = target['area'] if 'area' in target else ''
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

        return WEB_STORED.copy()


    def fill_out_webagent(self, soup):
        # WEB_AGENT
	WEB_AGENT['id'] = self.get_employee_hash_id(soup)
        WEB_AGENT['KeyinDate'] = self.date
        WEB_AGENT['CaseFrom'] = self.casefrom
	WEB_AGENT['ContactStore'] = self.get_store_name()
	WEB_AGENT['ContactStoreID'] = self.get_store_id()
	WEB_AGENT['EmpName'] = self.get_employee_name(soup)
	WEB_AGENT['EmpMobile'] = self.get_employee_mobile(soup)
	WEB_AGENT['EmpEMail'] = self.get_employee_mail(soup)
	WEB_AGENT['EmpTitle'] = self.get_employee_title(soup)
	WEB_AGENT['LicenseB'] = self.get_employee_license(soup)
	WEB_AGENT['District'] = WEB_STORED['District']
	WEB_AGENT['City'] = WEB_STORED['City']

        return WEB_AGENT.copy()
