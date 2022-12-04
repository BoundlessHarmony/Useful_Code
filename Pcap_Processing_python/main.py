# import pcap
# extract sort by http.response 200 ok
# encode data base64
# decode XOR rotation with key 0x7A
# Find *.exe
# print formatted ficker detection or not

import pyshark
# import pcap

import pandas as pd
import pyshark

wd = 'C:\\Users\\Boundless\\PycharmProjects\\pyshark_data_Extraction\\data\\'
pcap_d = wd + 'ex3.pcap'
cap = pyshark.FileCapture(pcap_d)
# filtered_cap = pyshark.FileCapture(cap, display_filter='http')
fn = input("Name your file")

if type(fn) == str:
    filename = fn + ".csv"
    csv_file = wd + filename
    f = open(csv_file, 'w')
pID = 1

for p in cap:
    if hasattr(p, 'http'):
        field_names = p.http._all_fields
        field_values = p.http._all_fields.values()
        df = pd.DataFrame(field_names, field_values)
        df.to_csv(csv_file, mode='a', index=False)
        pID += 1

#         for field_name in field_names:
#             for field_value in field_values:
#                 # if field_name == 'http.request.full_uri' and field_value.startswith('http'):
#                 #     print(f'{field_value}')
#
#
#
# # print(cap[9405])
print("done")