import argparse
import socket
import xml.etree.ElementTree as ET
from threading import Thread, Lock
from xml.etree.ElementTree import ElementTree

from Exceptions import NumberArgumentException, CreationSocketException


class Client():
    def __init__(self, address, port):
        self.receiver_thread = None
        self.IO_mutex = Lock()
        self.buffer = 4096
        self.socket = 0
        self.server_addr = address
        self.server_port = port
        self.server_addr_port = (self.server_addr, int(self.server_port))
        #self.server_addr_port = ("localhost", 12345)
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if self.socket == -1:
                raise CreationSocketException("Failed to create UDP socket")
        except CreationSocketException as e:
            print(e)
        message = self.prepare_message(f'connect')
        self.socket.sendto(message.encode("utf-8"), self.server_addr_port)

    def __del__(self):
        message = self.prepare_message(f'disconnect')
        self.socket.sendto(message.encode(), self.server_addr_port)
        reply = self.socket.recv(self.buffer)
        reply = ElementTree(ET.fromstring(reply))
        root = reply.getroot()
        if int(root[1].text) == 1:
            print("Connection closed")
            self.socket.close()
        else:
            print("Connection didn't closed")

    def start_thread(self):
        self.notice()
        self.receiver_thread = Thread(target=self.reciever, daemon=True)
        self.receiver_thread.start()
        self.sending()

    def sending(self):
        while True:
            try:
                str = input()
                self.check_args(str)
                str_split = str.split()
                if str_split[0] == "switchon":
                    self.switchon(str_split[1])
                elif str_split[0] == "switchoff":
                    self.switchoff(str_split[1])
                elif str_split[0] == "get":
                    self.get_status(str_split[1])
                elif str_split[0] == "disconnect":
                    self.disconnect()
                    print('You were disconnected from the server')
                    print('----------------------------------------------------')
                    break
                else:
                    print('The command is not recognized')
                    print('----------------------------------------------------')
            except NumberArgumentException as e:
                print(e)
                print('----------------------------------------------------')

    def reciever(self):
        while True:
            try:
                msg = self.socket.recv(self.buffer)
                msg = msg.decode()
                message = ElementTree(ET.fromstring(msg))
                root = message.getroot()
                print(root[0].text)
                print('----------------------------------------------------')
            except ConnectionResetError as e:
                print(e)
                print('Server is not active')
                print('----------------------------------------------------')

    def prepare_message(self, string, status=None):
        data = ET.Element('request')
        answer = ET.SubElement(data, 'query')
        answer.set('name', 'message')
        answer.text = string
        if status is not None:
            answer = ET.SubElement(data, 'query')
            answer.set('name', 'status')
            answer.text = str(status)
        return ET.tostring(data, encoding='unicode')

    def check_args(self, str):
        str_split = str.split()
        if len(str_split) > 3 or len(str_split) == 0:
            raise NumberArgumentException("Error with number of arguments")
        if str_split[0] == 'get' and len(str_split) != 2:
            raise NumberArgumentException("Error with number of arguments for command get")

    def switchon(self, number):
        message = self.prepare_message(f'switchon', number)
        self.socket.sendto(message.encode(), self.server_addr_port)

    def switchoff(self, number):
        message = self.prepare_message(f'switchoff', number)
        self.socket.sendto(message.encode(), self.server_addr_port)

    def get_status(self, channel):
        message = self.prepare_message(f'get', channel)
        self.socket.sendto(message.encode(), self.server_addr_port)

    def disconnect(self):
        message = self.prepare_message(f'disconnect')
        self.socket.sendto(message.encode(), self.server_addr_port)

    def notice(self):
        print("switchon with channel number - to switch on the channel")
        print("switchon with channel number - to switch off the channel")
        print("get with channel number - to get the status of the channel")
        print("disconnect with channel number - to get the status of the channel")
        print('----------------------------------------------------')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Client")
    parser.add_argument("-a", "--address", default="localhost")
    parser.add_argument("-p", "--port", default="12345")
    args = parser.parse_args()
    server_addr = args.address
    server_port = args.port
    #server_addr = 'localhost'
    #server_port = '12345'
    client = Client(server_addr, server_port)
    client.start_thread()