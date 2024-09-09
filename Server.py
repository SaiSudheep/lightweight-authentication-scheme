import random
import json
import paho.mqtt.client as mqtt
import time
import calendar

#   Prioritising the need to show the implementation of the algorithm, let us assume that there is only one user and one gateway for simplicity

f = None
x = None
e = None

#   --- Setup Phase ---

XSER = 330
XGD = 770
XSD = 984
GID = 834
SID = 123 

def hash(a, b):
    t = int(str(a)+str(b))
    t = t^10
    return t

#   --- Registration Phase ---

def userreg(data):
    MI = data["MI"]
    MP = data["MP"]
    f = hash(MI, XSER)
    x = hash(MP, XGD)
    e = f^x
    data = { "e" : e }
    data = json.dumps(data)
    client.publish("SReg", data)

def sdreg(data):
    T3 = str(calendar.timegm(time.gmtime()))
    T3 = int(T3[len(T3)-3:len(T3)])
    T2 = data["T2"]
    if T3-T2 < 5:
        TIcalc = hash(GID, T2)
        if not(TIcalc == data["TI"]):
            print("Invalid Gateway ID")
            return
        rmcalc = data["MNS"]^XSD
        MPcalc = hash(str(SID)+str(XSD),str(rmcalc)+str(data["T1"]))
        if not(MPcalc == data["MPS"]):
            print("Invalid Sensing Device ID")
            return
        f = hash(SID, XSER)
        x = hash(MPcalc, XSD)
        e = f^x
        TI = hash(SID, T3)
        TISER = hash(GID, T3)
        data = { "e" : e, "TISER" : TISER, "TI" : TI, "T3" : T3 }
        data = json.dumps(data)
        client.publish("SGReg",data)

def on_message(client, userdata, message):
    data = json.loads(message.payload.decode("utf-8"))
    print(f"Data Received from {message.topic}: {data}")
    if message.topic == "UReg":
        print("Starting User Registration...")
        userreg(data)
        print("User Registration Completed")
    if message.topic == "GReg":
        print("Starting Sensing Device Registration...")
        sdreg(data)
        print("Sensing Device Registration Completed(SERVER side)")

client = mqtt.Client("S")
client.username_pw_set("pxdyaqtz","FH4m_iiW5PRM")
client.on_message = on_message

ip = "m24.cloudmqtt.com"
port = 19903

client.connect(ip,port)
print("Subscribing to UReg, GReg...")
client.subscribe("UReg")
client.subscribe("GReg")
client.loop_forever()