#
# working with IOS_XR interfaces
#
#!/usr/bin/env python
import logging
import pprint
import xmltodict

from ncclient import manager
from ncclient.xml_ import *

def delete_isis(conn,instance):
    #
    # Delete ISIS instance 
    # Vefiried on IOS-XR 6.1.3
    #
    config = """
     <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <isis xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-clns-isis-cfg">
       <instances>
        <instance xc:operation="delete">
         <instance-name>{0}</instance-name>
        </instance>
       </instances>
      </isis>
     </config>
    """.format(instance)
    try:
        conn.edit_config(target="candidate",config=config)
        print("ISIS instance ",instance," removed.")
    except Exception as e:
        print("Removal of ISIS instance failed due to ",e)

def create_isis(conn,instance,net,level):
    #
    # Create ISIS instance 
    # 
    #
    config = """
     <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <isis xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-clns-isis-cfg">
       <instances>
        <instance>
         <instance-name>{0}</instance-name>
         <running></running>
        <is-type>{2}</is-type>
        <nets>
        <net>
        <net-name>{1}</net-name>
        </net>
        </nets>
        <afs>
        <af>
        <af-name>ipv4</af-name>
        <saf-name>unicast</saf-name>
        <af-data>
            <metric-styles>
            <metric-style>
            <level>not-set</level>
            <style>new-metric-style</style>
            <transition-state>disabled</transition-state>
            </metric-style>
            </metric-styles>
        </af-data>
        </af>
        </afs>
       </instance>
       </instances>
      </isis>
     </config>
    """.format(instance,net,level)
    try:
        conn.edit_config(target="candidate",config=config)
        print("ISIS instance ",instance," created.")
    except Exception as e:
        print("Creation of ISIS instance failed due to ",e)