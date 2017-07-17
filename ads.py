# reserved - 2 bytes - 0
# length - 4 bytes - od ams

# ams_target_adr - 6 bytes
# ams_target_port - 2 bytes
# ams_source_adr - 6 bytes
# ams_source_port - 2 bytes
# command - 2 bytes:
#     0 - invalid
#     1 - read device info
#     2 - read
#     3 - write
#     4 - read state
#     5 - write control
#     6 - add device notification
#     7 - delete device notification
#     8 - device notification
#     9 - read write
# state_flags - 2 bytes:
#     bit 0 - true request, false response
#     bit 2 - 1
#     bit 6 - true tcp, false udp
# data_length - 4 - bytes
# error_code - 4 bytes
#     0 - no error
#     ...
# invoke_id - 4 bytes - dowolne
# data - n bytes

# read:
# indexgroup - 4 bytes
# indexoffset - 4 bytes
# read_length - 4 bytes

import pyads
client = pyads.AdsClient()
client.connect('10.10.10.30')
# response = client.read_device_info("10.10.10.30.1.1", 801, "172.16.23.111.1.1", 32905)
# response = client.read("10.10.10.30.1.1", 801, "172.16.23.111.1.1", 32905, 16416, 0, 1)
# response = client.write("10.10.10.30.1.1", 801, "172.16.23.111.1.1", 32905, 16416, 0, b'a')
response = client.read_state("10.10.10.30.1.1", 801, "172.16.23.111.1.1", 32905)
client.close()
print(response)
