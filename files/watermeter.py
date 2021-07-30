import paho.mqtt.client as mqtt
import time
import configparser
import sys
import json
import datetime

config = configparser.RawConfigParser(allow_no_value=True)
config.read("watermeter_config.ini")

log_path = config.get('Logging', 'log_path', fallback='/var/log/solar/')
do_raw_log = config.getboolean('Logging', 'do_raw_log')

mqttBroker = config.get('watermeter', 'mqttBroker')
mqttPort = int(config.get('watermeter', 'mqttPort'))
mqttKeepAlive = int(config.get('watermeter', 'mqttKeepAlive'))

print(mqttBroker)

values = dict()

def on_message(client, userdata, msg):
    global values
    today = datetime.today()

    if msg.topic .lower() == "watermeter/reading/current_value" :
        values['current_value'] = int(str(msg.payload.decode("utf-8")))
        values['datetime'] = today.strftime("%d/%m/%Y %H:%M:%S")

    if msg.topic .lower() == "watermeter/reading/pulse_count" :
        values['pulse_count'] = int(str(msg.payload.decode("utf-8")))
        values['datetime'] = today.strftime("%d/%m/%Y %H:%M:%S")
    
    print( json.dumps(values) )

def getData():
    global values
    
    client = mqtt.Client("reader")

    client.connect(mqttBroker, mqttPort, mqttKeepAlive)

    while True:
        client.loop_start()

        client.subscribe("#")
        client.on_message=on_message

        time.sleep(10)
        
        client.loop_stop()

today = datetime.today()
print(today.strftime("%d/%m/%Y %H:%M:%S") )

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)

#while True:
#    try:
#        today = datetime.date.today()
#        print( today.strftime("%d/%m/%Y %H:%M:%S") )

#        getData()
#    except:
#        pass

getData()