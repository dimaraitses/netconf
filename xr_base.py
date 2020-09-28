#
# basic operations - connect, disconnect, commit
#
#!/usr/bin/env python
import logging
import pprint
import xmltodict

from ncclient import manager
from ncclient.xml_ import *


def xr_connect(host, port, user, password):
    conn = manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           timeout=60,
                           device_params={'name': 'iosxr'},
                           hostkey_verify=False)
    try:
       return(conn)
    except Exception as e:
        print("Connection to ",host,":",port," failed due to ",e)

def xr_commit(conn):
    try:
        conn.commit()
        print("Commit performed.")
    except Exception as e:
        print("Commit failed due to ",e)

def xr_disconnect(conn):
    try:
        conn.close_session()
        print("Connection closed.")
    except Exception as e:
        print("Failed to close connection due to ",e)


