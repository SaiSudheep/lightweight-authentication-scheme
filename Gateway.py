import random
import json
import calendar
import time
import paho.mqtt.client as mqtt

def hash(a, b):
    t = int(str(a)+str(b))
    t = t^10
    return t

MSID = None

#   --- Sensor Device Registration Phase ---

def sdgreg(data):
    T2 = str(calendar.timegm(time.gmtime()))
    T2 = int(T2[len(T2)-3:len(T2)])
    T1 = data["T1"]
    MSID = data["MSID"]
    if T2-T1 < 5:
        TI = hash(GID, T2)
        data["T2"] = T2
        data["TI"] = TI
        data = json.dumps(data)
        client.publish("GReg", data)

def sgreg(data):
    T4 = str(calendar.timegm(time.gmtime()))
    T4 = int(T4[len(T4)-3:len(T4)])
    T3 = data["T3"]
    if T4-T3 < 5:
        TISERcalc = hash(GID, T3)
        if not(TISERcalc == data["TISER"]):
            MSID = None
            print("MSID is not stored as there is value discrepancy")
        del data["TISER"]
        data["T4"] = T4
        data["MGID"] = MGID
        data = json.dumps(data)
        client.publish("GSDReg", data)

def on_message(client, userdata, message):
    data = json.loads(message.payload.decode("utf-8"))
    print(f"Data Received from {message.topic}: {data}")
    if message.topic == "SDReg":
        sdgreg(data)
    if message.topic == "SGReg":
        sgreg(data)

client = mqtt.Client("G")
client.username_pw_set("pxdyaqtz","FH4m_iiW5PRM")
client.on_message = on_message

ip = "m24.cloudmqtt.com"
port = 19903

#   --- Setup Phase ---

TI = None
GID = 834
XGD = 770
MGID = hash(GID, XGD)

#   ---

client.connect(ip, port)
print("Subscribing to SDReg, SGReg...")
client.subscribe("SDReg")
client.subscribe("SGReg")
client.loop_forever()