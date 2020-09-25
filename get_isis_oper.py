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

    filter  = """
		<dn-top:drivenets-top xmlns:dn-top="http://drivenets.com/ns/yang/dn-top">
			<protocols>
				<protocols-isis>
					<protocol-isis>
					</prototol-isis>
				</protocols-isis>
			</protocols>
		</dn-top:drivenets-top>
    """

    filter_adj  = """
                <dn-top:drivenets-top xmlns:dn-top="http://drivenets.com/ns/yang/dn-top">
 			<protocols>
                                <protocols-isis>
                                        <protocol-isis>
                                                <oper-items>
							<adjacencies>
							</adjacencies>
						</oper-items>
						<area-tag>CORE</area-tag>
					</protocol-isis>
				</protocols-isis>
			</protocols>
                </dn-top:drivenets-top>
    """ 
    print(conn.get(("subtree",filter_adj)))
    conn.close_session()

if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

    connect('305C-CS-DT', 830, 'dnroot', 'dnroot')
