import paho.mqtt.client as mqtt
import time
import calendar

def on_message(client,userdata,message):
    data = message.payload.decode("utf-8")
    print(data)

client = mqtt.Client("G")
client.username_pw_set("pxdyaqtz","FH4m_iiW5PRM")
client.on_message = on_message

ip = "m24.cloudmqtt.com"
port = 19903

client.connect(ip, port)
client.publish("satty","moinasa")

T5 = str(calendar.timegm(time.gmtime()))
print(T5)
T5 = int(T5[len(T5)-3:len(T5)])
print(T5)