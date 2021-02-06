import logging
import xmltodict
import xr_base
import xr_system
import xr_interfaces
import xr_isis
import jinja_test

from ncclient import manager
from ncclient.xml_ import *

def main():
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format=LOG_FORMAT)
    
    conn=xr_base.xr_connect('XR1-AUTO', 830, 'ccie', 'ccieauto')
    #xr_isis.create_isis(conn,'POP-2','49.0000.0000.0001.00','level2')
    full_conf=xr_base.xr_full_config(conn)
    print(full_conf)
    #xr_base.xr_commit(conn)
    xr_base.xr_disconnect(conn)

if __name__ == '__main__':
    main()


