import paho.mqtt.client as mqtt
import time
import configparser
import sys
import json

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
    print( "002")
    if msg.topic .lower() == "watermeter/reading/current_value" :
        values['current_value'] = int(str(msg.payload.decode("utf-8")))
    if msg.topic .lower() == "watermeter/reading/pulse_count" :
        values['pulse_count'] = int(str(msg.payload.decode("utf-8")))
    print( "003")

def getData():
    print( "001")
    global values

    client = mqtt.Client("reader")
    client.connect(mqttBroker, mqttPort, mqttKeepAlive) 

    client.loop_start()

    client.subscribe("#")
    client.on_message=on_message 

    time.sleep(30)
    print( "004")
    print( json.dumps(values) )
    client.loop_stop()

print( "000")
while True:
    try: 
        getData()
    except:
        pass
