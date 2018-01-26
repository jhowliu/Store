import logging

from .engine import sess
from .schema import WebAgent, WebStore

def insert_store(item):
    value = WebStore(**item)
    row = sess.query(WebStore).filter_by(idx=item['idx']).first()

    if (not row):
        sess.add(value)
        sess.commit()

def insert_employee(item):
    value = WebAgent(**item)
    row = sess.query(WebAgent).filter_by(id=item['id']).first()

    if (not row):
        sess.add(value)
        sess.commit()
