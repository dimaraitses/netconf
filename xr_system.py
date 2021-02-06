#
# IOX-XR system level configuration 
#
#!/usr/bin/env python
import logging
import xmltodict
import xr_base

from ncclient import manager
from ncclient.xml_ import *

def set_hostname(conn,hostname):
    # verified on 6.1.3 Feb 1 2021
    config="""
    <config>
    <host-names
			xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-shellutil-cfg">
			<host-name>{0}</host-name>
		</host-names>
    </config>
    """.format(hostname)
    try:
        conn.edit_config(target="candidate",config=config)
        print("Setting hostmane to ",hostname)
    except Exception as e:
        print("Failed to set hostname due to ",e)
    
def delete_hostname(conn):
    # verified on 6.1.3 Feb 1 2021
    config="""
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <host-names
			xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-shellutil-cfg">
			<host-name xc:operation="delete"/>
		</host-names>
    </config>
    """
    try:
        conn.edit_config(target="candidate",config=config)
        print("Hostname deleted")
    except Exception as e:
        print("Failed to delete hostname due to ",e)

def add_ntp_server(conn,address):
    config="""
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <ntp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ip-ntp-cfg">
    <peer-vrfs>
    <peer-vrf>
     <vrf-name>default</vrf-name>
     <peer-ipv4s>
      <peer-ipv4>
       <address-ipv4>{0}</address-ipv4>
       <peer-type-ipv4>
        <peer-type>server</peer-type>
       </peer-type-ipv4>
      </peer-ipv4>
    </peer-ipv4s>
    </peer-vrf>
    </peer-vrfs>
    </ntp>
    </config>""".format(address)
    try:
        print(config)
        conn.edit_config(target="candidate",config=config)
        print("NTP server added")
    except Exception as e:
        print("Failed to delete hostname due to ",e)

def delete_ntp_server(conn,address):
    config="""
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <ntp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ip-ntp-cfg">
    <peer-vrfs>
    <peer-vrf>
     <vrf-name>default</vrf-name>
     <peer-ipv4s>
      <peer-ipv4 xc:operation='remove'>
       <address-ipv4>{0}</address-ipv4>
       <peer-type-ipv4>
        <peer-type>server</peer-type>
       </peer-type-ipv4>
      </peer-ipv4>
    </peer-ipv4s>
    </peer-vrf>
    </peer-vrfs>
    </ntp>
    </config>""".format(address)
    try:
        print(config)
        conn.edit_config(target="candidate",config=config)
        print("NTP server deleted")
    except Exception as e:
        print("Failed to delete NTP server due to ",e)

def ntp_status(conn):
    filter = """
    <ntp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ip-ntp-oper">
    </ntp>
    """
    try:
        #print(config)
        res = conn.get(("subtree",filter)).xml
        print(res)
    except Exception as e:
        print("Failed to get ntp inforation due to  ",e)

def main():
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format=LOG_FORMAT)
    
    conn=xr_base.xr_connect('100.64.9.21', 830, 'cs', 'cs')
    ntp_status(conn)

    #xr_base.xr_commit(conn)
    xr_base.xr_disconnect(conn)

if __name__ == '__main__':
    main()
