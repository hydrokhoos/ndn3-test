# To provide provider record, send Interest packet: /1/provide/<CID>/<PID>
# To get provider record, send Interest packet: /1/get/<CID>

from ndn.app import NDNApp
from ndn.encoding import Name, Component
from ndn.types import InterestNack, InterestTimeout

import os
import socket

data = {}
app = NDNApp()

router_group_num = os.environ['ROUTER_GROUP_NUM']
peerid = os.environ['PEERID']

@app.route(f'/{router_group_num}/provide')
def on_interest_provide(name, interest_param, application_param):
    # Store some information about the received packet
    print(f"Received Interest for: {Name.to_str(name)}")
    name_list = Name.to_str(name).split("/")
    if len(name_list) <= 4:
        app.put_data(name, content=b'-1', freshness_period=10000)
    cid = name_list[3]
    peerID = ''
    for l in name_list[4:]:
        peerID += '/' + str(l)

    if cid not in data.keys():
      data[cid] = [peerID]
    elif peerID not in data[cid]:
      data[cid].append(peerID)
    app.put_data(name, content=b'SUCCESS', freshness_period=10000)

@app.route(f'/{router_group_num}/get')
def on_interest_get(name, interest_param, application_param):
    # Store some information about the received packet
    print(f"Received Interest for: {Name.to_str(name)}")
    name_list = Name.to_str(name).split("/")
    if len(name_list) > 2 and name_list[3] in data.keys():
        app.put_data(name, content=bytes(str(data[name_list[3]]), 'utf-8'), freshness_period=10000)
    else:
        app.put_data(name, content=b'-1', freshness_period=10000)

@app.route(f'/{peerid}/info')
def on_interest_get(name, interest_param, application_param):
    # Store some information about the received packet
    print(f"Received Interest for: {Name.to_str(name)}")
    ip = str(socket.gethostbyname(socket.gethostname()))
    app.put_data(name, content=f'/ip4/{ip}/tcp/4001/dummy'.encode(), freshness_period=10000)

# Start the app
try:
    print("start running app")
    app.run_forever()
except FileNotFoundError as e:
    print("Error: could not connect to NFD.")
except KeyboardInterrupt:
    print("Closing...")
finally:
    app.shutdown()
