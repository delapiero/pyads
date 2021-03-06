import unittest
import pyads
from datetime import datetime

class PyAdsTests(unittest.TestCase):

    def setUp(self):
        self.req_to_resp = {
            #read device info
            b'\x00\x00 \x00\x00\x00\n\n\n\x1e\x01\x01!\x03\xac\x10\x17o\x01\x01\x89\x80\x01\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            b'\x00\x008\x00\x00\x00\xac\x10\x17o\x01\x01\x89\x80\n\n\n\x1e\x01\x01!\x03\x01\x00\x05\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x0b-\nTCatPlcCtrl\x00\x00\x00\x00\x00',
            # read
            b'\x00\x00,\x00\x00\x00\n\n\n\x1e\x01\x01!\x03\xac\x10\x17o\x01\x01\x89\x80\x02\x00\x04\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 @\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00':
            b'\x00\x00)\x00\x00\x00\xac\x10\x17o\x01\x01\x89\x80\n\n\n\x1e\x01\x01!\x03\x02\x00\x05\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01',
            # write
            b'\x00\x00-\x00\x00\x00\n\n\n\x1e\x01\x01!\x03\xac\x10\x17o\x01\x01\x89\x80\x03\x00\x04\x00\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 @\x00\x00\x00\x00\x00\x00\x01\x00\x00\x001':
            b'\x00\x00$\x00\x00\x00\xac\x10\x17o\x01\x01\x89\x80\n\n\n\x1e\x01\x01!\x03\x03\x00\x05\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            # read_state
            b'\x00\x00 \x00\x00\x00\n\n\n\x1e\x01\x01!\x03\xac\x10\x17o\x01\x01\x89\x80\x04\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            b'\x00\x00(\x00\x00\x00\xac\x10\x17o\x01\x01\x89\x80\n\n\n\x1e\x01\x01!\x03\x04\x00\x05\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00',
            # write control
            b"\x00\x00(\x00\x00\x00\n\n\n\x1e\x01\x01\x10'\xac\x10\x17o\x01\x01\x89\x80\x05\x00\x04\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00":
            b"\x00\x00\x8a\x03\x00\x00\xac\x10\x17o\x01\x019\x80\n\n\n\x1e\x01\x01d\x00\x08\x00\x04\x00j\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00f\x03\x00\x00\x01\x00\x00\x00\xe0S\xbf\x06+\x01\xd3\x01\x07\x00\x00\x00Y\x00\x00\x00r\x00\x00\x00\xe0S\xbf\x06+\x01\xd3\x01\x91\x00\x00\x00\x10'\x00\x00TcSysSrv\x00\x00\x00\x00\x00\x00\x00\x00M\x00\x00\x00TwinCAT System Restart initiated from AmsNetId: 172.16.23.111.1.1 port 32905.\x00[\x00\x00\x00r\x00\x00\x00\xe0S\xbf\x06+\x01\xd3\x01\x91\x00\x00\x00\x10'\x00\x00TcSysSrv\x00\x00\x00\x00\x00\x00\x00\x00M\x00\x00\x00TwinCAT System Restart initiated from AmsNetId: 172.16.23.111.1.1 port 32905.\x00\\\x00\x00\x00r\x00\x00\x00\xe0S\xbf\x06+\x01\xd3\x01\x91\x00\x00\x00\x10'\x00\x00TcSysSrv\x00\x00\x00\x00\x00\x00\x00\x00M\x00\x00\x00TwinCAT System Restart initiated from AmsNetId: 172.16.23.111.1.1 port 32905.\x00]\x00\x00\x00r\x00\x00\x00\xe0S\xbf\x06+\x01\xd3\x01\x91\x00\x00\x00\x10'\x00\x00TcSysSrv\x00\x00\x00\x00\x00\x00\x00\x00M\x00\x00\x00TwinCAT System Restart initiated from AmsNetId: 172.16.23.111.1.1 port 32905.\x00^\x00\x00\x00r\x00\x00\x00\xe0S\xbf\x06+\x01\xd3\x01\x91\x00\x00\x00\x10'\x00\x00TcSysSrv\x00\x00\x00\x00\x00\x00\x00\x00M\x00\x00\x00TwinCAT System Restart initiated from AmsNetId: 172.16.23.111.1.1 port 32905.\x00a\x00\x00\x00r\x00\x00\x00\xe0S\xbf\x06+\x01\xd3\x01\x91\x00\x00\x00\x10'\x00\x00TcSysSrv\x00\x00\x00\x00\x00\x00\x00\x00M\x00\x00\x00TwinCAT System Restart initiated from AmsNetId: 172.16.23.111.1.1 port 32905.\x00b\x00\x00\x00r\x00\x00\x00\xe0S\xbf\x06+\x01\xd3\x01\x91\x00\x00\x00\x10'\x00\x00TcSysSrv\x00\x00\x00\x00\x00\x00\x00\x00M\x00\x00\x00TwinCAT System Restart initiated from AmsNetId: 172.16.23.111.1.1 port 32905.\x00",
            # add notification
            b'\x00\x00H\x00\x00\x00\n\n\n\x1e\x01\x01!\x03\xac\x10\x17o\x01\x01\x89\x80\x06\x00\x04\x00(\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 @\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\xd0\x07\x00\x00\xe8\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            b'\x00\x00(\x00\x00\x00\xac\x10\x17o\x01\x01\x89\x80\n\n\n\x1e\x01\x01!\x03\x06\x00\x05\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00',
            # delete notification
            b'\x00\x00$\x00\x00\x00\n\n\n\x1e\x01\x01!\x03\xac\x10\x17o\x01\x01\x89\x80\x07\x00\x04\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00':
            b'\x00\x00(\x00\x00\x00\xac\x10\x17o\x01\x01\x89\x80\n\n\n\x1e\x01\x01!\x03\x06\x00\x05\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00'
        }
        self.pyadsclient = pyads.AdsClient()
        self.pyadsclient.send = self.mocky_send

    def mocky_send(self, request):
        if request in self.req_to_resp:
            return pyads.AdsClient().read_response(self.req_to_resp[request])
        else:
            return b''

    def test_read_device_info(self):
        response = self.pyadsclient.read_device_info("10.10.10.30.1.1", 801, "172.16.23.111.1.1", 32905)
        self.assertEqual(response['ams length'], 56)
        self.assertEqual(response['ams net id target'], (172, 16, 23, 111, 1, 1))
        self.assertEqual(response['ams port target'], 32905)
        self.assertEqual(response['ams net id source'], (10, 10, 10, 30, 1, 1))
        self.assertEqual(response['ams port source'], 801)
        self.assertEqual(response['command id'], pyads.AdsCommand.ADS_Read_Device_Info)
        self.assertTrue(response['state flags']["response"])
        self.assertTrue(response['state flags']["ads command"])
        self.assertTrue(response['state flags']["TCP"])
        self.assertEqual(response['data length'], 24)
        self.assertEqual(response['error code'], 0)
        self.assertEqual(response['invoke id'], 0)
        self.assertEqual(response['result'], 0)
        self.assertEqual(response['major version'], 2)
        self.assertEqual(response['minor version'], 11)
        self.assertEqual(response['version build'], 2605)
        self.assertEqual(response['device name'], 'TCatPlcCtrl\x00\x00\x00\x00\x00')

    def test_read(self):
        response = self.pyadsclient.read("10.10.10.30.1.1", 801, "172.16.23.111.1.1", 32905, 16416, 0, 1)
        self.assertEqual(response['ams length'], 41)
        self.assertEqual(response['ams net id target'], (172, 16, 23, 111, 1, 1))
        self.assertEqual(response['ams port target'], 32905)
        self.assertEqual(response['ams net id source'], (10, 10, 10, 30, 1, 1))
        self.assertEqual(response['ams port source'], 801)
        self.assertEqual(response['command id'], pyads.AdsCommand.ADS_Read)
        self.assertTrue(response['state flags']["response"])
        self.assertTrue(response['state flags']["ads command"])
        self.assertTrue(response['state flags']["TCP"])
        self.assertEqual(response['data length'], 9)
        self.assertEqual(response['error code'], 0)
        self.assertEqual(response['invoke id'], 0)
        self.assertEqual(response['result'], 0)
        self.assertEqual(response['data'], b'\x01')
        self.assertEqual(response['read length'], 1)

    def test_write(self):
        response = self.pyadsclient.write("10.10.10.30.1.1", 801, "172.16.23.111.1.1", 32905, 16416, 0, b'1')
        self.assertEqual(response['ams length'], 36)
        self.assertEqual(response['ams net id target'], (172, 16, 23, 111, 1, 1))
        self.assertEqual(response['ams port target'], 32905)
        self.assertEqual(response['ams net id source'], (10, 10, 10, 30, 1, 1))
        self.assertEqual(response['ams port source'], 801)
        self.assertEqual(response['command id'], pyads.AdsCommand.ADS_Write)
        self.assertTrue(response['state flags']["response"])
        self.assertTrue(response['state flags']["ads command"])
        self.assertTrue(response['state flags']["TCP"])
        self.assertEqual(response['data length'], 4)
        self.assertEqual(response['error code'], 0)
        self.assertEqual(response['invoke id'], 0)
        self.assertEqual(response['result'], 0)

    def test_read_state(self):
        response = self.pyadsclient.read_state("10.10.10.30.1.1", 801, "172.16.23.111.1.1", 32905)
        self.assertEqual(response['ams length'], 40)
        self.assertEqual(response['ams net id target'], (172, 16, 23, 111, 1, 1))
        self.assertEqual(response['ams port target'], 32905)
        self.assertEqual(response['ams net id source'], (10, 10, 10, 30, 1, 1))
        self.assertEqual(response['ams port source'], 801)
        self.assertEqual(response['command id'], pyads.AdsCommand.ADS_Read_State)
        self.assertTrue(response['state flags']["response"])
        self.assertTrue(response['state flags']["ads command"])
        self.assertTrue(response['state flags']["TCP"])
        self.assertEqual(response['data length'], 8)
        self.assertEqual(response['error code'], 0)
        self.assertEqual(response['invoke id'], 0)
        self.assertEqual(response['result'], 0)
        self.assertEqual(response['ads state'], pyads.AdsState.ADSSTATE_RUN)
        self.assertEqual(response['device state'], 0)

    def test_write_control(self):
        response = self.pyadsclient.write_control("10.10.10.30.1.1", 10000, "172.16.23.111.1.1", 32905, 2, 0)
        self.assertEqual(response['ams length'], 906)
        self.assertEqual(response['ams net id target'], (172, 16, 23, 111, 1, 1))
        self.assertEqual(response['ams port target'], 32825)
        self.assertEqual(response['ams net id source'], (10, 10, 10, 30, 1, 1))
        self.assertEqual(response['ams port source'], 100)
        self.assertEqual(response['command id'], pyads.AdsCommand.ADS_Device_Notification)
        self.assertTrue(response['state flags']["request"])
        self.assertTrue(response['state flags']["ads command"])
        self.assertTrue(response['state flags']["TCP"])
        self.assertEqual(response['data length'], 874)
        self.assertEqual(response['error code'], 0)
        self.assertEqual(response['invoke id'], 0)
        self.assertEqual(response['notification length'], 870)
        self.assertEqual(response['stamps'], 1)
        self.assertEqual(len(response['headers']), 1)
        self.assertEqual(response['headers'][0]['time stamp'], datetime(2017, 7, 20, 7, 37, 23, 230000))
        self.assertEqual(response['headers'][0]['samples count'], 7)
        self.assertEqual(len(response['headers'][0]['samples']), 7)
        self.assertEqual(response['headers'][0]['samples'][0]['notification handle'], 89)
        self.assertEqual(response['headers'][0]['samples'][0]['sample size'], 114)

    def test_add_device_notification(self):
        response = self.pyadsclient.add_device_notification("10.10.10.30.1.1", 801, "172.16.23.111.1.1", 32905, 16416, 0, 1, 4, 2000, 1000)
        self.assertEqual(response['ams length'], 40)
        self.assertEqual(response['ams net id target'], (172, 16, 23, 111, 1, 1))
        self.assertEqual(response['ams port target'], 32905)
        self.assertEqual(response['ams net id source'], (10, 10, 10, 30, 1, 1))
        self.assertEqual(response['ams port source'], 801)
        self.assertEqual(response['command id'], pyads.AdsCommand.ADS_Add_Device_Notification)
        self.assertTrue(response['state flags']["response"])
        self.assertTrue(response['state flags']["ads command"])
        self.assertTrue(response['state flags']["TCP"])
        self.assertEqual(response['data length'], 8)
        self.assertEqual(response['error code'], 0)
        self.assertEqual(response['invoke id'], 0)
        self.assertEqual(response['result'], 0)
        self.assertEqual(response['notification handle'], 2)

    def test_delete_device_notification(self):
        response = self.pyadsclient.delete_device_notification("10.10.10.30.1.1", 801, "172.16.23.111.1.1", 32905, 7)
        self.assertEqual(response['ams length'], 40)
        self.assertEqual(response['ams net id target'], (172, 16, 23, 111, 1, 1))
        self.assertEqual(response['ams port target'], 32905)
        self.assertEqual(response['ams net id source'], (10, 10, 10, 30, 1, 1))
        self.assertEqual(response['ams port source'], 801)
        self.assertEqual(response['command id'], pyads.AdsCommand.ADS_Add_Device_Notification)
        self.assertTrue(response['state flags']["response"])
        self.assertTrue(response['state flags']["ads command"])
        self.assertTrue(response['state flags']["TCP"])
        self.assertEqual(response['data length'], 8)
        self.assertEqual(response['error code'], 0)
        self.assertEqual(response['invoke id'], 0)
        self.assertEqual(response['result'], 0)

unittest.main()