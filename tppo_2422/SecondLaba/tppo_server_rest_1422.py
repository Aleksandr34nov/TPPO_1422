import argparse
from threading import Thread, Lock
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from Relay import Relay
from tppo_server_1422 import Server
from multiprocessing import Process
from flask import Flask
from flask_restful import Api, Resource, request, reqparse

class ServerRest(Server):
    def __init__(self):
        self.addr = ''
        self.port = ''
        self.socket = 0
        self.buffer = 4096
        self.addr_list = []
        self.relay = Relay()
        self.target_thread = 0
        

    def start(self, addr, port):
        app.run(debug=True, port=int(port), host=addr)

    def reception(self, action, channel):
        reply = ""
        change = False
        if action == "switchon":
            num = channel - 1
            result_message, change = self.relay.change_status(num, 1)
            reply = {"reply": result_message}
            print(result_message)
            print('----------------------------------------------------')
        elif action == "switchoff":
            num = channel - 1
            result_message, change = self.relay.change_status(num, 0)
            reply = {"reply": result_message}
            print(result_message)
            print('----------------------------------------------------')
        elif action == "get":
            num = channel - 1
            result_message = self.relay.get_status(num)
            reply = {"reply": result_message}
            print(result_message)
            print('----------------------------------------------------')
        else:
            num = channel - 1
            result_message = "Command is not recognized"
            reply = {"reply": result_message}
            print(result_message)
            print('----------------------------------------------------')
        return reply

server = ServerRest()
app = Flask(__name__)
api = Api()

class Main(Resource):
    def get(self, channel):
        return server.reception(f'get', channel)

    def put(self, channel):
        parser = reqparse.RequestParser()
        parser.add_argument("action", type=str)
        par = parser.parse_args()
        return server.reception(par["action"], channel)

api.add_resource(Main, "/api/relay/<int:channel>")
api.init_app(app)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Server")
    parser.add_argument("-a", "--address", default="localhost")
    parser.add_argument("-p", "--port", default="12345")
    args = parser.parse_args()
    server_addr = args.address
    server_port = args.port
    server.start(server_addr, server_port)
