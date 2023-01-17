import threading
from threading import Thread
import xml.etree.ElementTree as ET
from Exceptions import ValueError

class Relay:
    def __init__(self):
        self.channel_0 = 0
        self.channel_1 = 0
        self.channel_2 = 0
        self.channel_3 = 0
        self.channel_4 = 0
        self.channel_5 = 0
        self.file_path = "./relay.xml"
        self.mutex = threading.Lock()
        self.relay_file_tree = None
        self.root = None
        self.relay_initialization()

    def relay_initialization(self):
        try:
            self.relay_file_tree = ET.parse('relay.xml')
            self.root = self.relay_file_tree.getroot()
            if len(self.root) == 6:
                self.channel_0 = int(self.root[0].text)
                self.channel_1 = int(self.root[1].text)
                self.channel_2 = int(self.root[2].text)
                self.channel_3 = int(self.root[3].text)
                self.channel_4 = int(self.root[4].text)
                self.channel_5 = int(self.root[5].text)
            else:
                print("File structure are broken, file overwritten")
                print('----------------------------------------------------')
                self.create_file()
                self.relay_file_tree = ET.parse('relay.xml')
                self.root = relay_file_tree.getroot()
        except FileNotFoundError as e:
            print(e)
            print("File will be created")
            print('----------------------------------------------------')
            self.create_file()
            self.relay_file_tree = ET.parse('relay.xml')
            self.root = self.relay_file_tree.getroot()

    def create_file(self):
        data = ET.Element('relay')
        channel_0 = ET.SubElement(data, 'channel')
        channel_1 = ET.SubElement(data, 'channel')
        channel_2 = ET.SubElement(data, 'channel')
        channel_3 = ET.SubElement(data, 'channel')
        channel_4 = ET.SubElement(data, 'channel')
        channel_5 = ET.SubElement(data, 'channel')
        channel_0.set('name', 'channel0')
        channel_1.set('name', 'channel1')
        channel_2.set('name', 'channel2')
        channel_3.set('name', 'channel3')
        channel_4.set('name', 'channel4')
        channel_5.set('name', 'channel5')
        channel_0.text = '0'
        channel_1.text = '0'
        channel_2.text = '0'
        channel_3.text = '0'
        channel_4.text = '0'
        channel_5.text = '0'
        xml_str = ET.tostring(data, encoding='unicode')
        self.relay_file = open('relay.xml', 'w')
        self.relay_file.write(xml_str)
        self.relay_file.close()

    def get_status(self, channel_number):
        print("Request for get status of " + str(channel_number + 1) + " channel")
        try:
            if channel_number > 5 or channel_number < 0:
                raise ValueError("Error with number of channel")
            if int(self.root[channel_number].text) == 1:
                res = "Channel " + str(channel_number + 1) + " is turned on(status: 1)"
            else:
                res = "Channel " + str(channel_number + 1) + " is turned off(status: 0)"
            return res
        except ValueError as e:
                print(e)
                res = "Wrong number of channel"
                return res

    def change_status(self, channel_number, to_status):
        print("Request change status of " + str(channel_number + 1) + " channel")
        if channel_number is not None and to_status is not None:
            if channel_number == 0:
                if self.channel_0 == to_status:
                    if to_status == 0:
                        result = "First channel is already turned off"
                    if to_status == 1:
                        result = "First channel is already turned on"
                    change = False
                else:
                    self.channel_0 = to_status
                    self.root[0].text = str(to_status)
                    if to_status == 0:
                        result = "First channel turned off"
                    if to_status == 1:
                        result = "First channel turned on"
                    change = True
            if channel_number == 1:
                if self.channel_1 == to_status:
                    if to_status == 0:
                        result = "Second channel is already turned off"
                    if to_status == 1:
                        result = "Second channel is already turned on"
                    change = False
                else:
                    self.channel_1 = to_status
                    self.root[1].text = str(to_status)
                    if to_status == 0:
                        result = "Second channel turned off"
                    if to_status == 1:
                        result = "Second channel turned on"
                    change = True
            if channel_number == 2:
                if self.channel_2 == to_status:
                    if to_status == 0:
                        result = "Three channel is already turned off"
                    if to_status == 1:
                        result = "Three channel is already turned on"
                    change = False
                else:
                    self.channel_2 = to_status
                    self.root[2].text = str(to_status)
                    if to_status == 0:
                        result = "Third channel turned off"
                    if to_status == 1:
                        result = "Third channel turned on"
                    change = True
            if channel_number == 3:
                if self.channel_3 == to_status:
                    if to_status == 0:
                        result = "Fourth channel is already turned off"
                    if to_status == 1:
                        result = "Fourth channel is already turned on"
                    change = False
                else:
                    self.channel_3 = to_status
                    self.root[3].text = str(to_status)
                    if to_status == 0:
                        result = "Fourth channel turned off"
                    if to_status == 1:
                        result = "Fourth channel turned on"
                    change = True
            if channel_number == 4:
                if self.channel_4 == to_status:
                    if to_status == 0:
                        result = "Fifth channel is already turned off"
                    if to_status == 1:
                        result = "Fifth channel is already turned on"
                    change = False
                else:
                    self.channel_4 = to_status
                    self.root[4].text = str(to_status)
                    if to_status == 0:
                        result = "Fifth channel turned off"
                    if to_status == 1:
                        result = "Fifth channel turned on"
                    change = True
            if channel_number == 5:
                if self.channel_5 == to_status:
                    if to_status == 0:
                        result = "Sixth channel is already turned off"
                    if to_status == 1:
                        result = "Sixth channel is already turned on"
                    change = False
                else:
                    self.channel_5 = to_status
                    self.root[5].text = str(to_status)
                    if to_status == 0:
                        result= "Sixth channel turned off"
                    if to_status == 1:
                        result = "Sixth channel turned on"
                    change = True
        self.relay_file_tree.write('relay.xml')
        self.relay_file_tree = ET.parse('relay.xml')
        self.root = self.relay_file_tree.getroot()
        self.channel_0 = int(self.root[0].text)
        self.channel_1 = int(self.root[1].text)
        self.channel_2 = int(self.root[2].text)
        self.channel_3 = int(self.root[3].text)
        self.channel_4 = int(self.root[4].text)
        self.channel_5 = int(self.root[5].text)
        return result, change

