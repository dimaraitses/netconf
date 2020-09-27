#!/usr/bin/env python
#
# 
#
import logging

from lxml import etree
from ncclient import manager
from ncclient.xml_ import *


def connect(host, port, user, password):
    conn = manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           timeout=60,
                           device_params={'name': 'iosxr'},
                           hostkey_verify=False)


    logging.info('Retrieving full config, please wait ...')

    result = conn.get_config(source='running').xml
    logging.info(result)

    conn.close_session()


if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

    connect('100.64.9.21', 830, 'cs', 'cs')

