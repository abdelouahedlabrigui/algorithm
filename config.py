import json 
from netmiko import Netmiko
from netmiko import ConnectHandler
import pandas as pd
from itertools import permutations

append = []
def enumerate_routers(fixName, number):
    for n in range(number):
        append.append({'names':str(fixName) + str(n), 'optional':str(n)})
    df = pd.DataFrame(append)
    # print(df.shape)
    return df
dfInc = pd.DataFrame(enumerate_routers('R',8))


def duplicate_dataframe(dfLocal):
    return dfLocal
# duplicate_dataframe(print(dfInc))


append_2 = []
def allocate_loopback_address():
    for router,number in zip(list(dfInc['names']), list(dfInc['optional'])):
        for loopback in range(4):
            if loopback != 0:
                commands = [
                    'configure terminal',
                    'interface loopback ' + str(loopback),
                    'ip address 192.168.' + str(number) + '.' + str(loopback) + ' 255.255.255.255',
                    'no shutdown',
                    'end'
                ]
                # print(commands)
                append_2.append({'routers':str(router),'interfaces': 'interface loopback ' + str(loopback),'loopbacks':'192.168.' + str(number) + '.' + str(loopback) + ' 255.255.255.255'})
    df = pd.DataFrame(append_2)
    # print(df)
    #   Please export this frame to use it
    # df.to_csv("allocate_loopback_address.csv")
# allocate_loopback_address()
append_3 = []
def allocate_ipv4_address():
    # frame_df = duplicate_dataframe(print(dfInc))
    # frameCol = list(dfInc['names'])
    df = pd.read_csv('info.csv', delimiter=',')
    for router, int1, ip in zip(list(df['routers']), list(df['int1']), list(df['ip'])):
        commands = [
            'configure terminal',
            'interface ' + str(int1),
            'ip address ' + str(ip) + ' 255.255.255.0',
            'no shutdown',
            'end'
        ]
        # print(commands)
        append_3.append({'routers':str(router),'interfaces': 'interface ' + str(int1),'ip_address': str(ip) + ' 255.255.255.0'})

    df = pd.DataFrame(append_3)
    # print(df)
    # print(df.shape)
    # print(df.head())
    # print(df.tail()) 
    #   Please export this frame to use it
    # df.to_csv("allocate_ipv4_address.csv")      
#         for cmd in list(commands):
#             with open('allocate_ipv4_address.txt', 'a') as f:
#                 f.write(cmd)
#                 f.close()
# allocate_ipv4_address()
append_4 = []
def configure_ip_route():    
    df_l = pd.read_csv('allocate_loopback_address.csv', delimiter=',')
    df_i = pd.read_csv('allocate_ipv4_address_v2.csv', delimiter=',')
    for r, i1, ip1 in zip(list(df_l['routers']), list(df_l['interfaces']), list(df_l['loopbacks'])):
        for ip2 in list(df_i['ip_address']): 
            if 'interface loopback 1' in i1:
                commands = [
                    'configure terminal',
                    'ip route ' + str(ip1) + ' ' + str(ip2),               
                    'end'
                ]  
                # print(commands)
                append_4.append({'routers':str(r), 'ip_route': 'ip route ' + str(ip1) + ' ' + str(ip2)})
    df = pd.DataFrame(append_4)
    print(df)
    # df.to_csv('configure_ip_route.csv')
# configure_ip_route()
# def confip(device,port):
#     cisco_device = {
#         'device_type':'cisco_ios_telnet',
#         'host':'127.0.0.1',
#         'username':str(device),
#         'password':'',
#         'port':str(port),
#         'secret':'',
#         'verbose':True
#     }
#     return cisco_device
append_5 = []
def configure_eigrp(asn):
    # to configure eigrp, i'm going to have all ip addresses corresponded to each network
    df = pd.read_csv('info.csv', delimiter=',')
    # cisco_device = confip(device,port)
    for i,r,p in zip(list(df['ip']),list(df['routers']),list(df['ports'])):
        # cisco_device = confip(r,p)
        # connection = ConnectHandler(**cisco_device)
        # connection.enable()
        command = [
            'configure terminal',
            'router eigrp ' + str(asn),
            'network ' + str(i),
            'end'
        ]
        append_5.append({'routers':str(r), 'ip':str(i), 'ports':str(p), 'ASN':str(asn), 'network':'network ' + str(i)})
    df_eigrp = pd.DataFrame(append_5)
    print(df_eigrp)
# configure_eigrp(123)

# def permute_devices():
#     df_info = pd.read_csv('info.csv', delimiter=',')
#     perm = permutations(list(df_info['routers']))
#     for i in list(perm):
#         print(i)
# permute_devices()
append_6 = []
def configure_ip_route_v2():
    df = pd.read_csv('info_v3.csv', delimiter=',')
    # print(df)
    for a,b,c in zip(list(df['routers']), list(df['networks']), list(df['ip_addresses'])):
        commands = [
            'configure terminal',
            f'ip route {str(b)} {str(c)}',
            'end'            
        ]
        append_6.append({'routers':str(a), 'ip_route': f'ip route {str(b)} 255.255.255.0 {str(c)}'})
    df_iproute = pd.DataFrame(append_6)
    print(df_iproute)
# configure_ip_route_v2()
append_7 = []
def configure_ip_route_v3():
    df = pd.read_csv('ip_route.csv', delimiter=',')
    for a,b,c in zip(list(df['routers']),list(df['loopback']),list(df['ip'])):
        append_7.append({'routers': f'{a}','ip_route': f'ip route {b} {c}'})
    df1 = pd.DataFrame(append_7)
    print(df1)
# configure_ip_route_v3()

def configure_access_list_icmp():
    