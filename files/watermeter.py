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
    today = datetime.date.today()

    if msg.topic .lower() == "watermeter/reading/current_value" :
        values['current_value'] = int(str(msg.payload.decode("utf-8")))
        values['datetime'] = today.strftime("%d/%m/%Y %H:%M:%S")

    if msg.topic .lower() == "watermeter/reading/pulse_count" :
        values['pulse_count'] = int(str(msg.payload.decode("utf-8")))
        values['datetime'] = today.strftime("%d/%m/%Y %H:%M:%S")
    
def getData():
    global values

    client = mqtt.Client("reader")
    client.connect(mqttBroker, mqttPort, mqttKeepAlive) 

    client.loop_start()

    client.subscribe("#")
    client.on_message=on_message 

    time.sleep(10)
    print( json.dumps(values) )

    client.loop_stop()

#while True:
#    try: 
#        today = datetime.date.today()
#        print( today.strftime("%d/%m/%Y %H:%M:%S") )

#        getData()
#    except:
#        pass

getData()