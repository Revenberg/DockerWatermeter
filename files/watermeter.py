import paho.mqtt.client as mqtt
import time
import configparser
import sys

config = configparser.RawConfigParser(allow_no_value=True)
config.read("watermeter_config.ini")

log_path = config.get('Logging', 'log_path', fallback='/var/log/solar/')
do_raw_log = config.getboolean('Logging', 'do_raw_log')

mqttBroker = config.get('watermeter', 'mqttBroker')
mqttPort = int(config.get('watermeter', 'mqttPort'))
mqttKeepAlive = int(config.get('watermeter', 'mqttKeepAlive'))

print(mqttBroker)

current_value = 0

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    if msg.topic.equals("watermeter/reading/current_value"):
        current_value = int(str(msg.payload.decode("utf-8")))
    print( current_value )

def getData():
    print("GetData")
    client = mqtt.Client("reader")
    client.connect(mqttBroker, mqttPort, mqttKeepAlive) 

    client.loop_start()

    client.subscribe("watermeter/#")
    client.on_message=on_message 

    # client.loop_forever()

    time.sleep(60)
    client.loop_stop()


#while True:
#    try: 
#        getData()
#    except:
#        pass

getData()
