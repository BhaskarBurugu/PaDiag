import time

from constants import *
from socketprog import PaSock

if __name__ == '__main__':
    PaCntrl = PaSock()
    PaCntrl.Paconnect(IP='172.232.50.9',Port=20108)
    #PaCntrl.sendcmd(cmd={'cmd':DISABLE_PA})
    PaCntrl.sendcmd(cmd={'cmd':GET_DATA_PA1})
    time.sleep(1)
    PaCntrl.receiveresp()
    PaCntrl.close()