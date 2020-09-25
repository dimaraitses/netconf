#!/usr/bin/env python
import logging

from ncclient import manager
from ncclient.xml_ import *


def connect(host, port, user, password):
    conn = manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           timeout=60,
                           device_params={'name': 'alu'},
                           hostkey_verify=False)

    config  = """
		<config>
                  <drivenets-top>
                          <system>
				<config-items>
				<name>P-8</name>
				</config-items>
                          </system>
                  </drivenets-top>
    		</config>
	"""

    conn.edit_config(target="candidate",config=config)
    conn.commit()
    conn.close_session()

if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

    connect('305C-CS-DT', 830, 'dnroot', 'dnroot')
