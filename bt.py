import threading
from typing import Callable
from models.data_models import LiveData
import socket
import asyncio
import bluetooth
from bleak import BleakScanner
from dataclasses import dataclass
from others import Thread

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
        self.connection_message = ""
        self.data_points = {}
    
    def set_data_point(self, key: str | list[str], func: Callable):
        if isinstance(key, str):
            self.data_points[key] = func
        elif isinstance(key, (list, set, tuple)):
            self.data_points[list[key]] = func
        else:
            raise Exception(f"Bad key type: {type(key)}")
    
    def get_devices(self):
        return bluetooth.discover_devices(lookup_names=True) + [(bl_info.address, bl_info.name) for bl_info in asyncio.run(self.ble_scanner.discover())]
    
    def send_message(self, msg: str):
        self.connection_message = ""
        
        if not self.connected:
            with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as bt_comm:
                bt_comm.connect((self.device.addr, self.device.port))
                
                self.connected = True
                
                bt_comm.send(msg.encode())
                
                msg_recv = bt_comm.recv(1024).decode()
                if msg_recv:
                    self.device.live_data.data_signal.emit(self._process_data(msg_recv))
            
            self.connected = False
        else:
            self.connection_message = msg
        
        return msg_recv
    
    def start_connection(self):
        if self.connected:
            raise Exception("Bluetooth already connected")
        
        self.connected = True
        
        self.connection_thread = Thread(self._connect)
        self.connection_thread.start()
    
    def stop_connection(self):
        self.connected = False
    
    def _connect(self):
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as bt_comm:
            bt_comm.connect((self.device.addr, self.device.port))
            
            while self.connected:
                bt_comm.send(self.connection_message.encode())
                msg_recv = bt_comm.recv(1024).decode()
                
                if msg_recv:
                    full_data = self._process_data(msg_recv)
                    
                    data_key_mapping = {}
                    for key, info in full_data.items():
                        for d_k, d_func in self.data_points.items():
                            if isinstance(d_k, str):
                                if key == d_k:
                                    d_func(info)
                                    break
                            elif isinstance(d_k, list):
                                if key in d_k:
                                    if d_k not in data_key_mapping:
                                        data_key_mapping[d_k] = [None for _ in range(len(d_k))]
                                    data_key_mapping[d_k][d_k.index(key)] = info
                                    if None not in data_key_mapping[d_k]:
                                        d_func(*data_key_mapping[d_k])
                                break
                    
                    self.device.live_data.data_signal.emit(full_data)
    
    def _process_data(self, data: str):
        processed_data = {}
        for sub_data_string in data.split("|"):
            name, data = sub_data_string.strip().split(":")
            
            processed_data[name] = self._process_sub_data(data)
        
        return processed_data
    
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


