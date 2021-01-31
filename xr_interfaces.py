#
# working with IOS_XR interfaces
#
#!/usr/bin/env python
import logging
import pprint
import xmltodict

from ncclient import manager
from ncclient.xml_ import *



def get_interfaces(conn):
    filter  = """
		<interfaces xmlns="http://openconfig.net/yang/interfaces">
			<interface>
			</interface>
		</interfaces>
    """
    print(conn.get(("subtree",filter)))

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

def get_interfaces_list(conn):
    #
    # returns a list of all interfaces on device
    #
    filter = """
                <interfaces xmlns="http://openconfig.net/yang/interfaces">
                        <interface>
				
                        </interface>
                </interfaces>
    """
    if_list = []
    xml_res = conn.get(("subtree",filter)).xml
    dict_res = xmltodict.parse(xml_res)
    for i in dict_res["rpc-reply"]["data"]["interfaces"]["interface"]:
        if (i["name"]) in if_list:
            print(".")
        else:
            if_list.append(i["name"])
    return(if_list)

def create_loopback(conn,index):
    config = """
	<config>
	 <interfaces
			xmlns="http://openconfig.net/yang/interfaces">
			<interface operation="create">
				<name>Loopback{0}</name>
				<config>
					<name>Loopback{0}</name>
					<type
						xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:softwareLoopback
					</type>
					<enabled>true</enabled>
				</config>
				
			</interface>
            </interfaces>
    </config>
    """.format(index)
    print(config)
    conn.edit_config(target="candidate",config=config)

def delete_loopback(conn,index):
    config = """
	<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
	 <interfaces
			xmlns="http://openconfig.net/yang/interfaces">
			<interface xc:operation="delete">
				<name>Loopback{0}</name>
				<config>
					<name>Loopback{0}</name>
					<type
						xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:softwareLoopback
					</type>
					<enabled>true</enabled>
				</config>
				
			</interface>
            </interfaces>
    </config>
    """.format(index)
    print(config)
    try:
        conn.edit_config(target="candidate",config=config)
        print("Loopback",index," deleted")
    except Exception as e:
        print("Counld not delete interface due to ",e)

def create_sub(conn,interface,sub,vlan):
    config = """
	      <config>
	      <interfaces
			xmlns="http://openconfig.net/yang/interfaces">
          <interface operation="create">
				<name>{0}</name>
				<config>
					<name>{0}</name>
					<type
						xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:ethernetCsmacd
					</type>
					<enabled>false</enabled>
				</config>
				<ethernet
					xmlns="http://openconfig.net/yang/interfaces/ethernet">
					<config>
						<auto-negotiate>false</auto-negotiate>
					</config>
				</ethernet>
				<subinterfaces>
					<subinterface>
						<index>{1}</index>
						<config>
							<index>{1}</index>
							<name>{0}.{1}</name>
							<enabled>true</enabled>
						</config>
						<ipv6
							xmlns="http://openconfig.net/yang/interfaces/ip">
							<config>
								<enabled>false</enabled>
							</config>
						</ipv6>
						<vlan
							xmlns="http://openconfig.net/yang/vlan">
							<config>
								<vlan-id>{2}</vlan-id>
							</config>
						</vlan>
					</subinterface>
				</subinterfaces>
			</interface>
			</interfaces>
			</config>
            """.format(interface,sub,vlan)
    print(config)
    conn.edit_config(target="candidate",config=config)

def delete_sub(conn,interface,sub):
    config = """
	      <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
	      <interfaces
			xmlns="http://openconfig.net/yang/interfaces">
          <interface operation="create">
				<name>{0}</name>
				<config>
					<name>{0}</name>
					<type
						xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:ethernetCsmacd
					</type>
					<enabled>false</enabled>
				</config>
				<ethernet
					xmlns="http://openconfig.net/yang/interfaces/ethernet">
					<config>
						<auto-negotiate>false</auto-negotiate>
					</config>
				</ethernet>
				<subinterfaces>
					<subinterface xc:operation="delete">
						<index>{1}</index>
						<config>
							<index>{1}</index>
							<name>{0}.{1}</name>
							<enabled>true</enabled>
						</config>
						<ipv6
							xmlns="http://openconfig.net/yang/interfaces/ip">
							<config>
								<enabled>false</enabled>
							</config>
						</ipv6>
						
					</subinterface>
				</subinterfaces>
			</interface>
			</interfaces>
			</config>
            """.format(interface,sub)
    try:
        conn.edit_config(target="candidate",config=config)
        print("sub interface deleted")
    except Exception as e:
        print("sub interface deletion failed due to ",e)
    

	config="""
	<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
	<interface-configurations
		xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
		<interface-configuration>
			<active>act</active>
			<interface-name>{0}</interface-name>
			<interface-virtual></interface-virtual>
			<ipv4-network
				xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
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

def set_if_ipv4_addr_eitf(conn,interface,address,mask):
	# verified on IOS-XR 6.1.3 on Jan 31, 2021
	config="""
	<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
	<interfaces xmlns="http://openconfig.net/yang/interfaces">
	<interface>
		<name>{0}</name>
		<config>
		<name>{0}</name>
		<type xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:ethernetCsmacd</type>
		<enabled>true</enabled>
		</config>
		<subinterfaces>
		<subinterface>
		<index>0</index>
		<ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
		<address>
			<ip>{1}</ip>
			<config>
			<ip>{1}</ip>
			<prefix-length>{2}</prefix-length>
			</config>
		</address>
		</ipv4>
		</subinterface>
		</subinterfaces>
	</interface>
	</interfaces>
	</config>
	""".format(interface,address,mask)
	print(config)
	conn.edit_config(target="candidate",config=config)

def del_if_ipv4_addr_eitf(conn,interface,address,mask):
	# verified on IOS-XR 6.1.3 on Jan 31, 2021
	# note using xmlns:xc namespace and operation="delete"
	config="""
	<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
	<interfaces xmlns="http://openconfig.net/yang/interfaces" xc:operation="delete">
	<interface>
		<name>{0}</name>
		<config>
		<name>{0}</name>
		<type xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:ethernetCsmacd</type>
		<enabled>true</enabled>
		</config>
		<subinterfaces>
		<subinterface>
		<index>0</index>
		<ipv4 xmlns="http://openconfig.net/yang/interfaces/ip" xc:operation="delete">
		<address xc:operation="delete">
			<ip>{1}</ip>
			<config>
			<ip>{1}</ip>
			<prefix-length>{2}</prefix-length>
			</config>
		</address>
		</ipv4>
		</subinterface>
		</subinterfaces>
	</interface>
	</interfaces>
	</config>
	""".format(interface,address,mask)
	print(config)
	conn.edit_config(target="candidate",config=config)

def set_if_ipv6_addr_eitf(conn,interface,address,mask):
	# verified on IOS-XR 6.1.3 on Jan 31, 2021
	config="""
	<config>
	<interfaces xmlns="http://openconfig.net/yang/interfaces" operation="replace">
	<interface>
		<name>{0}</name>
		<config>
		<name>{0}</name>
		<type xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:ethernetCsmacd</type>
		<enabled>true</enabled>
		</config>
		<subinterfaces>
		<subinterface>
		<index>0</index>
		<ipv6 xmlns="http://openconfig.net/yang/interfaces/ip">
        <address>
        <ip xmlns="http://openconfig.net/yang/interfaces">cafe::1</ip>
        <config>
        <ip>{1}</ip>
        <prefix-length>{2}</prefix-length>
        </config>
        </address>
        </ipv6>
		</subinterface>
		</subinterfaces>
	</interface>
	</interfaces>
	</config>
	""".format(interface,address,mask)
	print(config)
	conn.edit_config(target="candidate",config=config)