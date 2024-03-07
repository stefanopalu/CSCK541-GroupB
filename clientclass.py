"""Client class"""

import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

class Client:
    """Client class"""
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket()
        self.client_socket.connect((host, port))

    def send_dictionary (self, data_format, data):
        """Send dictionary"""
        serialized_data = self.serialize_dictionary(data_format, data)
        print(serialized_data)
        print(type(serialized_data))
        msg = f"dictionary,{data_format},{serialized_data}"
        #Encoding the string before sending it
        self.client_socket.send(msg.encode())

    def send_text (self, data, encrypt):
        """Send text"""
        #if encrypt:
        #    data = self.encrypt_data(data)

        msg = f"text,{data},{str(encrypt)}"
        self.client_socket.send(msg.encode())

    #def encrypt_data(self, data):
    #    """Encrypt data"""
    #    key = Fernet.generate_key() 
    #    fernet = Fernet(key) 
    #    return fernet.encrypt(data)

    def serialize_dictionary (self, data_format, dictionary):
        """Serialize the data received by the client depending on its format"""
        if data_format == "binary":
            return pickle.dumps(dictionary)
        elif data_format == "json":
            return json.dumps(dictionary)
        elif data_format == "xml":
            root = ET.Element("root")
            for key, value in dictionary.items():
                ET.SubElement(root,key).text = str(value)
            return ET.tostring(root)


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345

    client = Client(HOST, PORT)
    dictionary_data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    TEXT = "hello world!"
    # client.send_text(TEXT, False)
    client.send_dictionary("json", dictionary_data)