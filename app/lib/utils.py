# -*- coding: utf8 -*-
import os
import json

__DATAPATH__ = os.path.join(os.path.dirname(__file__), '../data/data.json')

def load_data():
    with open(__DATAPATH__) as fp:
        data = json.load(fp)

    area_list = [[area['AreaName'] for area in city['AreaList']] for city in data]
    city_list = [city['CityName'] for city in data]

    return city_list, area_list


CITY_LIST, AREA_LIST = load_data()

def split_address(address):
    target = {}

    address = _formalize_address(address)

    for ix, city in enumerate(CITY_LIST):
        if city in address:
            target['city'] = city
            address=address.replace(city, '')
            for area in AREA_LIST[ix]:
                if area in address:
                    target['area'] = area
                    address = address.replace(area, '')
                    break

    target['road'] = address

    return target

def _formalize_address(address):
    return address.replace(u'台', u'臺')
