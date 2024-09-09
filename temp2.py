import paho.mqtt.client as mqtt
import time

def on_message(client,userdata,message):
    data = message.payload.decode("utf-8")
    print(data)

client = mqtt.Client("B")
client.username_pw_set("pxdyaqtz","FH4m_iiW5PRM")
client.on_message = on_message

ip = "m24.cloudmqtt.com"
port = 19903

client.connect(ip, port)


client.subscribe("satty")
client.loop_forever()