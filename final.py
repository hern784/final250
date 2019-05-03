import sys
import time
sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')
import grovepi
import grove_rgb_lcd as lcd
import math
import requests
import json
import paho.mqtt.client as mqtt
import threading
from flask import Flask
from flask import jsonify
from flask import request
import argparse

#variables
desired_temp_min = 60
desired_temp_max = 100
indoor_temp = 0
outdoor_temp = 0
temp = 0
desired_temp = 70
mode = 1
hvac = 0
i = 0
flag = 0
wind_on = "rpi-jaeishin/HVAC", "Entering wind mode: rpi-jaeishin"
wind_off = "rpi-jaeishin/HVAC", "Exiting wind mode: rpi-jaeishin"

#i/o being used

sensor = 7
buzzer_pin = 2
button = 4
potentiometer = 0    #
grovepi.pinMode(buzzer_pin, "OUTPUT")
grovepi.pinMode(button, "INPUT")
grovepi.pinMode(potentiometer,"INPUT")
lcd.setRGB(0,122,0)

# Used for threading

def startup():
    thread = threading.Thread(target=main)
    thread.daemon = True
    thread.start()

# Used For HTTP requests

app = Flask('RaspberryPi Mailbox Server')
@app.route('/send-mail', methods=['POST'])
def post_mail_callback():

    global desired_temp

    payload = request.get_json()
    in_temp = int(payload["temp"])

    # Print incomming temp
    print("Incomming encrypted temp = " + str(in_temp))
    desired_temp = int(math.sqrt(in_temp))
    print("Incomming decrypted temp = " + str(desired_temp))
    print(payload)

    if (desired_temp>60) and (desired_temp <100):
        response = {'Response': 'Mail sent'}
    else:
        response = {'Response': 'Invalid temp sent'}

    return json.dumps(response)

# Used for MQTT to send ack when entering or exiting wind mode

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("rpi-jaeishin/HVAC")
    client.message_callback_add("rpi-jaeishin/HVAC", ledcustom)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    print("on_message: msg.payload is of type " + str(type(msg.payload)))

# changing temp with rotary encoder

def get_rotary_angle():

    adc_ref = 5
    grove_vcc = 5
    full_angle = 300
    sensor_value = grovepi.analogRead(potentiometer)
    voltage = round((float)(sensor_value) * adc_ref / 1023, 2)
    degrees = round((voltage * full_angle) / grove_vcc, 2)

    d_temp = 60 + degrees/5
    if d_temp > 100:
        d_temp = 100
    if d_temp < 60:
        d_temp = 60

    return d_temp

# Get indoor temp from grovepi sensor

def get_indoor_temp():
    sensor = 7
    while True:
        try:
            [temp, humid] = grovepi.dht(sensor, 0)
            if math.isnan(temp) == False and math.isnan(humid) == False:
                #print("temp =", temp)
                temp_f = (1.8 * temp) + 32
                time.sleep(.5)
                return temp_f

        except KeyboardInterrupt:
            break
        except IOError:
            print ("Error")

# API for getting outdoor temp

OWM_API_KEY = '5fa72aaa861d38b37e5ebd93634a1f88'  # OpenWeatherMap API Key
DEFAULT_ZIP = 90089
def get_weather(zip_code):
    params = {
        'appid': OWM_API_KEY,
    }
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+ str(zip_code) + '&appid=' + str(OWM_API_KEY))
    if response.status_code == 200: # Status: OK
        data = response.json()
        temp_k = data["main"]["temp"]
        outdoor_temp = ((temp_k-273)*1.8+32)
        return outdoor_temp
    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return 0.0, 0.0

# main function with the logic for the thermostat

def main():
    global desired_temp_min 
    global desired_temp_max    
    global indoor_temp 
    global outdoor_temp 
    global temp 
    global desired_temp 
    global mode 
    global hvac 
    global wind_on
    global wind_off
    global i
    global flag

    while True:
        try:
            # Get indoor temp
            indoor_temp = int(get_indoor_temp())
            
            # lcd sleep after 5 seonds
            time.sleep(.2)
            button_status = grovepi.digitalRead(button)
            i = i + 1
            if button_status:
                i = 0
                lcd.setRGB(0,122,0)
                print("awake")
                flag = 0
            elif i == 5:
                lcd.setRGB(0,0,0)
                print("asleep")
                flag = 1

            # if lcd is off turn on, if lcd is on change mode and sound buzzer
            if button_status:
                grovepi.digitalWrite(buzzer_pin, 1)
                time.sleep(.1)
                grovepi.digitalWrite(buzzer_pin, 0)  
                if flag == 0:     
                                      
                    if (mode < 3):
                        mode = mode + 1
                    else:
                        mode = 0
                else:
                    lcd.setRGB(0,122,0)
     
            # state machine for window
            if (indoor_temp > desired_temp):
                if (outdoor_temp < desired_temp):
                    if hvac != "wind":
                        # send open window
                        client.publish("rpi-jaeishin/HVAC", str(wind_on))
                        print(wind_on)
                    hvac = "wind"
                else:
                    if hvac == "wind":
                        # send close window
                        client.publish("rpi-jaeishin/HVAC", str(wind_off))
                        print(wind_off)
                    hvac = "AC"

            if (indoor_temp < desired_temp):
                if (outdoor_temp < desired_temp):
                    if hvac == "wind":
                        # send close window
                        client.publish("rpi-jaeishin/HVAC", str(wind_off))
                        print(wind_off)
                    hvac = "heat"
                else:
                    if hvac != "wind":
                        # send open window
                        client.publish("rpi-jaeishin/HVAC", str(wind_on))
                        print(wind_on)
                    hvac = "wind"

            if (indoor_temp == desired_temp):
                # send message close window
                if hvac == "wind":
                    client.publish("rpi-jaeishin/HVAC", str(wind_off))
                    print(wind_off)
                hvac = "fan"

            # measure outdoor temp from API
            outdoor_temp = int(get_weather(DEFAULT_ZIP))


            # Set LED to print in correct format

            #default
            if (mode == 1):
                print ("\nmode = 1 - Default")
                print("Temp: {:>3}F  {:>4}".format(indoor_temp, hvac))
                print("Desired: {:>3}F".format(desired_temp))
                lcd.setText_norefresh("Temp: {:>3}F {:>4}\nDesired: {:>3}F".format(indoor_temp, hvac, desired_temp))
            
            #outdoor
            if (mode == 2):
                print("\nmode = 2 - Outdoor")
                print("Temp: {:>3}F {:>4}".format(indoor_temp, hvac))
                print("Outdoor: {:>3}F".format(outdoor_temp))
                lcd.setText_norefresh("Temp: {:>3}F {:>4}\nOutdoor: {:>3.2f}F".format(indoor_temp, hvac, outdoor_temp))
            
            #edit
            if (mode == 0):
                print("\nmode = 0 - Edit")
                # get rotary angle set desired temp
                desired_temp = get_rotary_angle()
                print("Set Temp: {:>3}F".format(desired_temp)) 
                lcd.setText_norefresh("Set Temp:{:>3}F".format(desired_temp))

        except KeyboardInterrupt:
            lcd.setRGB(0,0,0)
            setText_norefresh("")
            break

##########################  begin  #######################################

if __name__ == '__main__':
   
    # MQTT to publish HVAC
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    i = 0

    # Set up argparse, a Python module for handling command-line arguments
    parser = argparse.ArgumentParser(prog='mailServer',
            description='Script to start up mail server')

    parser.add_argument('-p', metavar='password', required=True,
            help='Required password to access server')

    args = parser.parse_args()

    mailbox_password = args.p   # password
    startup()
    app.run(debug=False, host='0.0.0.0', port=4250)






