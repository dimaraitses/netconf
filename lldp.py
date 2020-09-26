#
# working with IOS_XR interfaces
#
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
                           device_params={'name': 'iosxr'},
                           hostkey_verify=False)
    return(conn)

def get_lldp(conn):
    filter  = """
		<lldp
			xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ethernet-lldp-oper">
		</lldp>
    """
    print(conn.get(("subtree",filter)))
    conn.close_session()

def get_lldp_summ(conn):
    filter  = """
                <lldp
                        xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ethernet-lldp-oper">
                 <nodes>
                  <node>
                   <node-name>0/0/CPU0</node-name>
                    <neighbors>
                     <summaries>
                     </summaries>
                    </neighbors>
                   </node>
                 </nodes>
		</lldp>
    """
    print(conn.get(("subtree",filter)))
    conn.close_session()

def get_interface(conn,interface):
    filter = """
                <interfaces xmlns="http://openconfig.net/yang/interfaces">
                        <interface>
				<name>{0}</name>
                        </interface>
                </interfaces>
    """.format(interface)
    print(conn.get(("subtree",filter)))
    conn.close_session()

def set_description(conn,interface,description):
    config = """
	<config>
	 <interface-configurations
			xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
          <interface-configuration>
          <active>act</active>
          <interface-name>{0}</interface-name>
				<description>{1}</description>
          </interface-configuration>
         </interface-configurations>
        </config>
    """.format(interface,description)
    print(config)
    conn.edit_config(target="candidate",config=config)
    conn.commit()

def set_ipv4_address(conn,interface,address,mask):
    config = """
        <config>
         <interface-configurations
                        xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
          <interface-configuration>
          <active>act</active>
          <interface-name>{0}</interface-name>
           <ipv4-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
	    <addresses>
	     <primary>
              <address>{1}</address>
              <netmask>{2}</netmask>
	     </primary>
            </addresses>
           </ipv4-network>
          </interface-configuration>
         </interface-configurations>
        </config>
    """.format(interface,address,mask)
    print(config)
    conn.edit_config(target="candidate",config=config)
    conn.commit()

if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

    m=connect('P-1', 830, 'ccie', 'ccie')
    get_lldp_summ(m)
