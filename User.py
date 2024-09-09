import random
import json
import time
import calendar
import paho.mqtt.client as mqtt

x = None
f = None
e = None
MGID = None

def hash(a, b):
    t = int(str(a)+str(b))
    t = t^10
    return t

def on_message(client, userdata, message):
    data = json.loads(message.payload.decode("utf-8"))
    print(f"Data Received from {message.topic}: {data}")
    if message.topic == "SReg":
        e = data["e"]
        x = hash(MP, XGD)
        f = e^x
        print("User Registration Phase Completed")
    if message.topic == "GSDReg":
        T5 = str(calendar.timegm(time.gmtime()))
        T5 = int(T5[len(T5)-3:len(T5)])
        T4 = data["T4"]
        if T5-T4 < 5:
            TIcalc = hash(SID, data["T3"])
            if not(TIcalc == data["TI"]):
                print("Message is not coming from cloud server")
                return
            x = hash(MP, XSD)
            f = data["e"]^x
            MGID = data["MGID"]
            print("Sensing Device Registration Completed")

client = mqtt.Client("U")
client.username_pw_set("pxdyaqtz","FH4m_iiW5PRM")
client.on_message = on_message

ip = "m24.cloudmqtt.com"
port = 19903

#   --- Setup Phase ---
ID = 123
PW = 678
SID = 123
XSD = 984
XGD = 770
MSID = hash(SID, XSD)
MGID = 834776

r = random.randint(100, 999)

print("Starting User Registration Phase...")
#   --- User Registration Phase ---

#   Let the User have a default username and password initially (Assume length = 5)

MI = hash(ID, r)
MP = hash(PW, r)
print("MI :"+str(MI))
print("MP :"+str(MP))

data = { "MI" : MI, "MP" : MP, "MGID" : MGID }
data = json.dumps(data)

client.connect(ip, port)
client.publish("UReg", data)
client.loop_start()
print("Waiting for the server's response...")
client.subscribe("SReg")
time.sleep(5)
client.loop_stop()

#   --- Sensing Device Registration Phase ---

print("Starting Device Registration Phase...")
rm = random.randint(100, 999)
T1 = str(calendar.timegm(time.gmtime()))
T1 = int(T1[len(T1)-3:len(T1)])

MPS = hash(str(SID)+str(XSD), str(rm)+str(T1))
MNS = XSD^rm

data = { "MSID" : MSID, "MNS" : MNS, "MPS" : MPS, "T1" : T1 }
data = json.dumps(data)
client.publish("SDReg", data)
client.loop_start()
print("Waiting for the server's response...")
client.subscribe("GSDReg")
time.sleep(5)
client.loop_stop()

