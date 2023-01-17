import socket
import argparse
import threading
from threading import Thread, Lock
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from Relay import Relay


class Server():
    def __init__(self, addr, port):
        self.addr = addr
        self.port = int(port)
        self.socket = 0
        self.buffer = 4096
        self.addr_list = []
        self.relay = Relay()
        self.target_thread = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.addr, self.port))
        self.mutex = threading.Lock()
        self.switchoff = False

    def start_thread(self):
        while True:
            if self.switchoff:
                print("No clients, server switch off")
                break
            msg, addr = self.socket.recvfrom(self.buffer)
            msg_thread = Thread(target=self.reception, args=(msg.decode("utf-8"), addr), daemon=True)
            msg_thread.start()

    def reception(self, msg, addr):
        reply = ""
        message = ElementTree(ET.fromstring(msg))
        root = message.getroot()
        change = False
        if root[0].text == "switchon":
            self.mutex.acquire()
            num = int(root[1].text) - 1
            result_message, change = self.relay.change_status(num, 1)
            reply = self.prepare_message(result_message)
            print(result_message)
            print('----------------------------------------------------')
            self.mutex.release()
        if root[0].text == "switchoff":
            self.mutex.acquire()
            num = int(root[1].text) - 1
            result_message, change = self.relay.change_status(num, 0)
            reply = self.prepare_message(result_message)
            print(result_message)
            print('----------------------------------------------------')
            self.mutex.release()
        if root[0].text == "get":
            self.mutex.acquire()
            num = int(root[1].text) - 1
            result_message = self.relay.get_status(num)
            reply = self.prepare_message(result_message)
            print(result_message)
            print('----------------------------------------------------')
            self.mutex.release()
        if root[0].text == "connect":
            if self.check_connection(addr):
                reply = self.prepare_message(f'You have already connected to the server')
            else:
                print('Client with address ' + str(addr) + ' was connected')
                reply = self.prepare_message(f'You have successfully connected to the server')
        if root[0].text == "disconnect":
            try:
                self.addr_list.remove(addr)
                if not self.addr_list:
                    self.switchoff = True
                reply = self.prepare_message(f'Client with address' + str(addr) + 'was disconnected')
            except ValueError:
                reply = self.prepare_message(f'Client with address' + str(addr) + 'was not disconnected')
        if reply is not None:
            if root[0].text == "switchon" or root[0].text == "switchoff":
                if change:
                    for address in self.addr_list:
                        self.socket.sendto(reply.encode(), address)
                else:
                        self.socket.sendto(reply.encode(), addr)
            else:
                self.socket.sendto(reply.encode(), addr)


    def prepare_message(self, s, status=None):
        data = ET.Element('reply')
        answer = ET.SubElement(data, 'answer')
        answer.set('name', 'message')
        answer.text = s
        if status is not None:
            answer = ET.SubElement(data, 'answer')
            answer.set('name', 'status')
            answer.text = str(status)
        return ET.tostring(data, encoding='unicode')

    def check_connection(self, addr):
        if addr in self.addr_list:
            print('Client' + str(addr) + 'connected')
            return True
        else:
            self.addr_list.append(addr)
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Server")
    parser.add_argument("-a", "--address", default="localhost")
    parser.add_argument("-p", "--port", default="12345")
    args = parser.parse_args()
    server_addr = args.address
    server_port = args.port
    #server_addr = 'localhost'
    #server_port = '12345'
    server = Server(server_addr, server_port)
    server.start_thread()
