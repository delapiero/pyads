import struct
import threading
import select
from datetime import datetime, timedelta
from socket import socket, AF_INET, SOCK_STREAM
from enum import Enum


class AdsState(Enum):
    ADSSTATE_INVALID = 0
    ADSSTATE_IDLE = 1
    ADSSTATE_RESET = 2
    ADSSTATE_INIT = 3
    ADSSTATE_START = 4
    ADSSTATE_RUN = 5
    ADSSTATE_STOP = 6
    ADSSTATE_SAVECFG = 7
    ADSSTATE_LOADCFG = 8
    ADSSTATE_POWERFAILURE = 9
    ADSSTATE_POWERGOOD = 10
    ADSSTATE_ERROR = 11
    ADSSTATE_SHUTDOWN = 12
    ADSSTATE_SUSPEND = 13
    ADSSTATE_RESUME = 14
    ADSSTATE_CONFIG = 15 # system is in config mode
    ADSSTATE_RECONFIG = 16 # system should restart in config mode


class AdsCommand(Enum):
    Invalid = 0
    ADS_Read_Device_Info = 1
    ADS_Read = 2
    ADS_Write = 3
    ADS_Read_State = 4
    ADS_Write_Control = 5
    ADS_Add_Device_Notification = 6
    ADS_Delete_Device_Notification = 7
    ADS_Device_Notification = 8
    ADS_Read_Write = 9


class AdsClient():

    def __init__(self):
        self.ip = ""
        self.port = 48898
        self.dev_thread = threading.Thread(target=self.listen_task)
        self.dev_thread.daemon = True
        self.dev_thread_running = False

    def connect(self, ip, port=None):
        self.ip = ip
        self.port = port if port is not None else 48898

    def send(self, request):
        ads_socket = socket(AF_INET, SOCK_STREAM)
        ads_socket.connect((self.ip, self.port))
        ads_socket.send(request)
        response = ads_socket.recv(65535)
        ads_socket.close()
        return self.read_response(response)

    def listen(self):
        self.dev_thread_running = True
        self.dev_thread.start()

    def listen_task(self):
        notification_socket = socket(AF_INET, SOCK_STREAM)
        notification_socket.connect((self.ip, self.port))
        notification_socket.settimeout(None)
        while self.dev_thread_running:
            ready = select.select([notification_socket], [], [], 5)
            if ready[0]:
                try:
                    response = notification_socket.recv(65535)
                    if response:
                        self.listen_handler(self.device_notification(self.read_response(response)))
                except ConnectionResetError:
                    pass
                finally:
                    notification_socket.close()
                    notification_socket = socket(AF_INET, SOCK_STREAM)
                    notification_socket.connect((self.ip, self.port))
                    notification_socket.settimeout(None)

    def listen_handler(self, response):
        print(response)

    def listen_stop(self):
        self.dev_thread_running = False
        self.dev_thread.join()

    def read_response(self, response):
        response_format = self.get_align() + self.get_ams_tcp_header_format() + self.get_ams_header_format() + "I"
        header = struct.unpack(response_format, response[0:42])
        result = {
            'ams length' : header[1],
            'ams net id target' : header[2:8],
            'ams port target' : header[8],
            'ams net id source' : header[9:15],
            'ams port source' : header[15],
            'command id' : AdsCommand(header[16]),
            'state flags' : {
                'request' : (header[17] & 0x0001) == 0,
                'response' : (header[17] & 0x0001) > 0,
                'ads command' : (header[17] & 0x0004) > 0,
                'TCP' : (header[17] & 0x0040) == 0,
                'UDP' : (header[17] & 0x0040) > 0
            },
            'data length' : header[18],
            'error code' : header[19],
            'invoke id' : header[20],
            'result' : header[21]
            }
        if len(response) > 42:
            result['data'] = response[42:]
        return result

    def get_align(self):
        return "<" # https://docs.python.org/3/library/struct.html#byte-order-size-and-alignment

    def get_ams_tcp_header_format(self):
        return 'HI'

    def get_ams_header_format(self):
        return 'BBBBBBHBBBBBBHHHIII'

    def get_ams_tcp_header(self, length):
        values = (0, length)
        header = struct.Struct(self.get_align() + self.get_ams_tcp_header_format())
        return header.pack(*values)

    def get_ams_header(self, net_id_target, port_target, net_id_source, port_source, command_id, state_flags, data_length, error_code, invoke_id):
        target_arr = net_id_target.split(".")
        source_arr = net_id_source.split(".")
        target_arr_int = list(map(int, target_arr)) + [port_target]
        source_arr_int = list(map(int, source_arr)) + [port_source]
        other = [command_id, state_flags, data_length, error_code, invoke_id]
        values = target_arr_int + source_arr_int + other
        header = struct.Struct(self.get_align() + self.get_ams_header_format())
        return header.pack(*values)

    def get_header(self, values, fmt, data=None):
        data = data if data is not None else bytes([])
        data_struct = struct.Struct(self.get_align() + fmt)
        return data_struct.pack(*values) + data

    def get_data(self, net_id_target, port_target, net_id_source, port_source, function, data=None):
        data = data if data is not None else bytes([])
        ams_header = self.get_ams_header(
            net_id_target, port_target, net_id_source, port_source, function, 4, len(data), 0, 0)
        ams_tcp_header = self.get_ams_tcp_header(len(ams_header) + len(data))
        return ams_tcp_header + ams_header + data

    def read_device_info(self, net_id_target, port_target, net_id_source, port_source):
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, AdsCommand.ADS_Read_Device_Info.value)
        response = self.send(request)
        device_info_format = self.get_align() + "BBH"
        device_info = struct.unpack(device_info_format, response['data'][0:4])
        response['major version'] = device_info[0]
        response['minor version'] = device_info[1]
        response['version build'] = device_info[2]
        response['device name'] = "".join(map(chr, response['data'][4:]))
        del response['data']
        return response

    def read(self, net_id_target, port_target, net_id_source, port_source, index_group, index_offset, length):
        values = (index_group, index_offset, length)
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, AdsCommand.ADS_Read.value, self.get_header(values, 'III'))
        response = self.send(request)
        read_format = self.get_align() + "I"
        read = struct.unpack(read_format, response['data'][0:4])
        response['read length'] = read[0]
        response['data'] = response['data'][4:]
        return response

    def write(self, net_id_target, port_target, net_id_source, port_source, index_group, index_offset, data):
        values = (index_group, index_offset, len(data))
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, AdsCommand.ADS_Write.value, self.get_header(values, 'III', data))
        return self.send(request)

    def read_state(self, net_id_target, port_target, net_id_source, port_source):
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, AdsCommand.ADS_Read_State.value)
        response = self.send(request)
        read_state_format = self.get_align() + "HH"
        read_state = struct.unpack(read_state_format, response['data'][0:4])
        response['ads state'] = AdsState(read_state[0])
        response['device state'] = read_state[1]
        del response['data']
        return response

    def write_control(self, net_id_target, port_target, net_id_source, port_source, ads_state, device_state, data=None):
        data = data if data is not None else bytes([])
        values = (ads_state, device_state, len(data))
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, AdsCommand.ADS_Write_Control.value, self.get_header(values, 'HHI', data))
        return self.device_notification(self.send(request))

    def add_device_notification(self, net_id_target, port_target, net_id_source, port_source, index_group, index_offset, length, transmission_mode, max_delay, cycle_time):
        values = (index_group, index_offset, length, transmission_mode, max_delay, cycle_time, 0, 0, 0, 0)
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, AdsCommand.ADS_Add_Device_Notification.value, self.get_header(values, 'IIIIIIIIII'))
        response = self.send(request)
        add_device_notification_format = self.get_align() + "I"
        add_device_notification = struct.unpack(add_device_notification_format, response['data'][0:4])
        response['notification handle'] = add_device_notification[0]
        del response['data']
        return response

    def delete_device_notification(self, net_id_target, port_target, net_id_source, port_source, notification_handle):
        values = [notification_handle]
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, AdsCommand.ADS_Delete_Device_Notification.value, self.get_header(values, 'I'))
        return self.send(request)

    def device_notification(self, response):
        response['notification length'] = response['result']
        del response['result']
        device_notification_format = self.get_align() + "I"
        stamp_header_format = self.get_align() + "QI"
        notification_sample_format = self.get_align() + "II"
        device_notification = struct.unpack(device_notification_format, response['data'][0:4]) 
        response['stamps'] = device_notification[0]
        response['headers'] = []
        response['data'] = response['data'][4:]
        for _ in range(response['stamps']):
            stamp_header = struct.unpack(stamp_header_format, response['data'][0:12])
            new_header = {
                'time stamp' : datetime(1601,1,1) + timedelta(microseconds=(stamp_header[0]/10)),
                'samples count' : stamp_header[1],
                'samples' : []
            }
            response['data'] = response['data'][12:]
            for _ in range(new_header['samples count']):
                notification_sample = struct.unpack(notification_sample_format, response['data'][0:8])
                new_notification_sample = {
                    'notification handle' : notification_sample[0],
                    'sample size' : notification_sample[1]
                }
                new_notification_sample['sample data'] = response['data'][8:8 + new_notification_sample['sample size']]
                new_header['samples'].append(new_notification_sample)
                response['data'] = response['data'][8 + new_notification_sample['sample size']:]
            response['headers'].append(new_header)
        del response['data']
        return response

    def read_write(self, net_id_target, port_target, net_id_source, port_source, index_group, index_offset, length, data):
        values = (index_group, index_offset, length, len(data))
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, AdsCommand.ADS_Read_Write.value, self.get_header(values, 'IIII', data))
        response = self.send(request)
        read_write_format = self.get_align() + "I"
        read_write = struct.unpack(read_write_format, response['data'][0:4])
        response['read length'] = read_write[0]
        response['data'] = response['data'][4:]
        return response
