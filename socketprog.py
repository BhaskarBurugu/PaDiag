import json
import socket
from constants import *

class PaSock():
    def __init__(self):
       # print('Hellow Bhaskar')
        self.sock = None
    ##################################################################################################
    def Paconnect(self,IP='192.168.1.10',Port=5003):
        try:
            self.sock = socket.socket()
            self.sock.connect((IP, Port))
            return SUCCESS
        except:
            print('unable to connect to server')
            self.sock = None
            return SERVER_CONNECTION_FAIL
    ###################################################################################################
    def sendcmd(self,cmd={'cmd':None}):
        if self.sock !=None:
            if cmd !=None:
                #print(cmd)
                self.sock.send(bytes(cmd['cmd'],"utf-8"))
                return SUCCESS
            else:
                return NULLCMD
        else:
            return SERVER_CONNECTION_FAIL
    ####################################################################################################
    def receiveresp(self):
        recv_data = self.sock.recv(100)
        #EventData = recv_data
        EventData = json.loads(recv_data)
        #print(EventData)
        return EventData
    ####################################################################################################
    def close(self):
        if self.sock !=None:
            self.sock.close()
    ####################################################################################################