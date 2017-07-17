AMS_TCP_HEADER_FORMAT = 'HI'
AMS_HEADER_FORMAT = 'BBBBBBHBBBBBBHHHIII'

import struct
from socket import *


class AdsClient():

    def __init__(self):
        self.ads_socket = socket(AF_INET, SOCK_STREAM)

    def connect(self, ip, port=None):
        self.ads_socket.connect((ip, port if port is not None else 48898))

    def send(self, request):
        bytes_send = self.ads_socket.send(request)
        response = self.ads_socket.recv(65535)
        result = {'result' : response[38:42]}
        if len(response) > 42:
            result['data'] = response[42:]
        return result

    def get_ams_tcp_header(self, length):
        values = (0, length)
        header = struct.Struct('<' + AMS_TCP_HEADER_FORMAT)
        return header.pack(*values)

    def get_ams_header(self, net_id_target, port_target, net_id_source, port_source, command_id, state_flags, data_length, error_code, invoke_id):
        target_arr = net_id_target.split(".")
        source_arr = net_id_source.split(".")
        target_arr_int = list(map(int, target_arr)) + [port_target]
        source_arr_int = list(map(int, source_arr)) + [port_source]
        other = [command_id, state_flags, data_length, error_code, invoke_id]
        values = target_arr_int + source_arr_int + other
        header = struct.Struct('<' + AMS_HEADER_FORMAT)
        return header.pack(*values)

    def get_header(self, values, fmt, data=None):
        data = data if data is not None else bytes([])
        data_struct = struct.Struct('<' + fmt)
        return data_struct.pack(*values) + data

    def get_data(self, net_id_target, port_target, net_id_source, port_source, function, data=None):
        data = data if data is not None else bytes([])
        ams_header = self.get_ams_header(
            net_id_target, port_target, net_id_source, port_source, function, 4, len(data), 0, 0)
        ams_tcp_header = self.get_ams_tcp_header(len(ams_header) + len(data))
        return ams_tcp_header + ams_header + data

    def read_device_info(self, net_id_target, port_target, net_id_source, port_source):
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, 1)
        response = self.send(request)
        response['major version'] = response['data'][0:1]
        response['minor version'] = response['data'][1:2]
        response['version build'] = response['data'][2:4]
        response['device name'] = response['data'][4:]
        del response['data']
        return response

    def read(self, net_id_target, port_target, net_id_source, port_source, index_group, index_offset, length):
        values = (index_group, index_offset, length)
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, 2, self.get_header(values, 'III'))
        response = self.send(request)
        response['length'] = response['data'][0:4]
        response['data'] = response['data'][4:]
        return response

    def write(self, net_id_target, port_target, net_id_source, port_source, index_group, index_offset, data):
        values = (index_group, index_offset, len(data))
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, 3, self.get_header(values, 'III', data))
        return self.send(request)

    def read_state(self, net_id_target, port_target, net_id_source, port_source):
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, 4)
        response = self.send(request)
        response['ads state'] = response['data'][0:2]
        response['device state'] = response['data'][2:4]
        del response['data']
        return response

    def write_control(self, net_id_target, port_target, net_id_source, port_source, ads_state, device_state, data=None):
        data = data if data is not None else bytes([])
        values = (ads_state, device_state, len(data))
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, 5, self.get_header(values, 'HHI', data))
        return self.send(request)

    def add_device_notification(self, net_id_target, port_target, net_id_source, port_source, index_group, index_offset, length, transmission_mode, max_delay, cycle_time):
        values = (index_group, index_offset, length, transmission_mode, max_delay, cycle_time, 0, 0, 0, 0)
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, 6, self.get_header(values, 'IIIIIIIIII'))
        response = self.send(request)
        response['notification handle'] = response['data'][0:4]
        del response['data']
        return response

    def delete_device_notification(self, net_id_target, port_target, net_id_source, port_source, notification_handle):
        values = (notification_handle)
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, 7, self.get_header(values, 'I'))
        return self.send(request)

    def device_notification(self, net_id_target, port_target, net_id_source, port_source, length, stamps, headers):
        values = (length, stamps)
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, 8, self.get_header(values, 'II', headers))
        return self.send(request)

    def read_write(self, net_id_target, port_target, net_id_source, port_source, index_group, index_offset, length, data):
        values = (index_group, index_offset, length, len(data))
        request = self.get_data(net_id_target, port_target, net_id_source, port_source, 9, self.get_header(values, 'IIII', data))
        response = self.send(request)
        response['length'] = response['data'][0:4]
        response['data'] = response['data'][4:]
        return response

    def close(self):
        self.ads_socket.close()
