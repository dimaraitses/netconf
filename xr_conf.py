import logging
import xmltodict
import xr_base
import xr_system
import xr_interfaces

from ncclient import manager
from ncclient.xml_ import *

def main():
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format=LOG_FORMAT)
    
    conn=xr_base.xr_connect('XR1-AUTO', 830, 'ccie', 'ccieauto')
    #xr_interfaces.get_interface(conn,'GigabitEthernet0/0/0/0')
    #xr_interfaces.set_if_ipv4_addr_eitf(conn,'GigabitEthernet0/0/0/0','10.0.0.1','24')
    #xr_interfaces.del_if_ipv4_addr_eitf(conn,'GigabitEthernet0/0/0/0','10.0.0.1','24')
    xr_base.xr_commit(conn)
    xr_base.xr_disconnect(conn)

if __name__ == '__main__':
    main()


