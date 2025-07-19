import threading
from models.data_models import LiveData
import socket
import asyncio
import bluetooth
from bleak import BleakScanner
from dataclasses import dataclass

@dataclass
class BT_Device:
    name: str
    addr: str
    live_data: LiveData
    port: int = 1234

class Bluetooth:
    def __init__(self, device: BT_Device):
        self.device = device
        self.ble_scanner = BleakScanner()
        
        self.connected = False
    
    def get_devices(self):
        return bluetooth.discover_devices(lookup_names=True) + [(bl_info.address, bl_info.name) for bl_info in asyncio.run(self.ble_scanner.discover())]
    
    def send_message(self, msg: str):
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as bt_comm:
            bt_comm.connect((self.device.addr, self.device.port))
            
            self.connected = True
            
            bt_comm.send(msg.encode())
            
            msg_recv = bt_comm.recv(1024).decode()
            if msg_recv:
                self.device.live_data.data_signal.emit(self._process_data(msg_recv))
        
        self.connected = False
        
        return msg_recv
    
    def start_connection(self):
        self.connected = True
        
        self.connection_thread = threading.Thread(target=self._connect)
        self.connection_thread.start()
    
    def stop_connection(self):
        self.connected = False
    
    def _connect(self):
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as bt_comm:
            bt_comm.connect((self.device.addr, self.device.port))
            
            msg_recv = bt_comm.recv(1024).decode()
            while self.connected:
                msg_recv = bt_comm.recv(1024).decode()
                
                if msg_recv:
                    self.device.live_data.data_signal.emit(self._process_data(msg_recv))
    
    def _process_data(self, data: str):
        processed_data = {}
        for sub_data_string in data.split("|"):
            name, data = sub_data_string.strip().split(":")
            
            processed_data[name] = self._process_sub_data(data)
    
    def _process_sub_data(self, data: str):
        data = data.strip()
        
        var_type = data[:data.find("(")].removeprefix(var_type).strip().removeprefix(f"(").removesuffix(")")
        
        data = data.removeprefix(var_type).strip().removeprefix(f"(").removesuffix(")")
        
        if var_type == "collection":
            data = [self._process_sub_data(sub_data) for sub_data in data.split(",")]
        elif var_type == "str":
            data = data
        elif var_type == "number":
            data = float(data)
        else:
            raise Exception(f"Type: ({var_type}) is not a valid type")
        
        return data


