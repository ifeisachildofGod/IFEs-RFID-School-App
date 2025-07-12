
from models import BT_Device
import socket
import asyncio
import time
from typing import Callable
from bleak import BleakScanner
import bluetooth



class Bluetooth:
    def __init__(self, device: BT_Device):
        self.device = device
        self.ble_scanner = BleakScanner()
    
    def get_devices(self):
        return bluetooth.discover_devices(lookup_names=True) + [(bl_info.address, bl_info.name) for bl_info in asyncio.run(self.ble_scanner.discover())]
    
    def send_message(self, msg: str):
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as bt_comm:
            bt_comm.connect((self.device.addr, self.device.port))
            
            bt_comm.send(msg.encode())
            
            msg_recv = bt_comm.recv(1024).decode()
        
        return msg_recv
    
    def connect_until(self, keep_connect: Callable[[str], None], do: Callable[[str, socket.socket], None]):
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as bt_comm:
            bt_comm.connect((self.device.addr, self.device.port))
            
            msg_recv = bt_comm.recv(1024).decode()
            while keep_connect(msg_recv):
                do(msg_recv, bt_comm)
                msg_recv = bt_comm.recv(1024).decode()
                
            
        
