import pandas as pd
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
duplicate_dataframe(print(dfInc))


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
    print(df)

allocate_loopback_address()
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
    print(df)
    # print(df.shape)
    # print(df.head())
    # print(df.tail())            
#         for cmd in list(commands):
#             with open('allocate_ipv4_address.txt', 'a') as f:
#                 f.write(cmd)
#                 f.close()
allocate_ipv4_address()

