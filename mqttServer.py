import paho.mqtt.client as mqtt
import time

# for mqtt for window mode
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #led, ultrasonic, button subscribing
    client.subscribe("rpi-jaeishin/HVAC")
    client.message_callback_add("rpi-jaeishin/HVAC",ultrasonicranges)

    #subscribe to the ultrasonic ranger topic here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8")) 


if __name__ == '__main__':

    # used for mqtt for window mode
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    
    while True:
        time.sleep(1)

