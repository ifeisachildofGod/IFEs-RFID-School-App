
import time
import serial
import socket
from others import Thread
from typing import Callable
from dataclasses import dataclass
from models.data_models import LiveData

@dataclass
class CommDevice:
    live_data: LiveData
    port: int | str
    addr: str | None = None
    baud_rate: int | None = None

class BaseCommSystem:
    def __init__(self, device: CommDevice, error_func: Callable[[Exception], None]):
        self.device = device
        self.error_func = error_func
        
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
    
    def send_message(self, msg: str):
        self.connection_message = msg.strip()
    
    def start_connection(self):
        if self.connected:
            raise Exception("Comm device already connected")
        
        self.connected = True
        
        self.connection_thread = Thread(self._connect)
        self.connection_thread.crashed.connect(self._crashed)
        self.connection_thread.start()
    
    def stop_connection(self):
        self.connected = False
    
    def _crashed(self, e: Exception):
        self.connection_thread.quit()
        self.error_func(e)
    
    def _data_process(self, msg_recv: str):
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
    
    def _connect(self):
        raise NotImplementedError()
    
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


class Bluetooth(BaseCommSystem):
    def __init__(self, device: CommDevice, error_func):
        super().__init__(device, error_func)
        
        assert self.device.addr is not None, "Invalid device"
    
    def _connect(self):
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as bt_comm:
            bt_comm.connect((self.device.addr, self.device.port))
            
            while self.connected:
                bt_comm.send(self.connection_message.encode())
                msg_recv = bt_comm.recv(1024).decode().strip()
                
                if msg_recv:
                    self._data_process(msg_recv)
                
                self.connection_message = ""

class DirectSerial(BaseCommSystem):
    def __init__(self, device: CommDevice, error_func):
        super().__init__(device, error_func)
        
        assert self.device.baud_rate is not None, "Invalid device"
    
    def _connect(self):
        serial_target = serial.Serial(self.device.port, self.device.baud_rate, timeout=1)
        
        time.sleep(2)  # Wait for Target to initialize
        
        while self.connected:
            if serial_target.in_waiting > 0:
                if self.connection_message:
                    serial_target.write(bytes(self.connection_message))
                
                msg_recv = serial_target.readline().decode().strip()
                if msg_recv:
                    self._data_process(msg_recv)
                
                self.connection_message = ""
        
        serial_target.close()

