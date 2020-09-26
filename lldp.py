#
# working with IOS_XR interfaces
#
#!/usr/bin/env python
import logging
import xmltodict

from ncclient import manager
from ncclient.xml_ import *


def connect(host, port, user, password):
    print("Opening connection to ",host,":",port)
    conn = manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           timeout=60,
                           device_params={'name': 'iosxr'},
                           hostkey_verify=False)
    return(conn)

def disconnect(conn):
    print("Closing connection.")
    conn.close_session()

def commit_changes(conn):
    print("Committing changes..")
    conn.commit()

def get_lldp(conn):
    filter  = """
		<lldp
			xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ethernet-lldp-oper">
		</lldp>
    """
    result = conn.get(("subtree",filter))
    return(result)

def get_lldp_summ(conn):
    print("Get LLDP summary data")
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
    result = conn.get(("subtree",filter))
    return(result)
    
def set_if_desc_from_lldp(conn):
    result=get_lldp_summ(conn).xml
    print("Starting to work")
    print(type(result))
    dict_lldp=xmltodict.parse(result)
    for i in (dict_lldp["rpc-reply"]["data"]["lldp"]["nodes"]["node"]["neighbors"]["summaries"]["summary"]):
        print("Found neighbor ",i["device-id"]," on interface ",i["interface-name"])
        print("Setting port description.")
        description=("Link to "+i["device-id"]+" "+i["lldp-neighbor"]["port-id-detail"])
        set_description(conn,i["interface-name"],description)
        print("next neighbor\n")
    print("Done")

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
    
    print("Setting port description ..")
    conn.edit_config(target="candidate",config=config)
    

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

def main():
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format=LOG_FORMAT)

    m=connect('100.64.9.21', 830, 'cs', 'cs')
    set_if_desc_from_lldp(m)
    commit_changes(m)
    disconnect(m)

if __name__ == '__main__':
    main()
