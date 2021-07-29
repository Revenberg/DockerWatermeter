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

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))

print("001")

client = mqtt.Client("reader")
client.connect(mqttBroker, mqttPort, mqttKeepAlive) 

print("002")

client.loop_start()

print("003")

client.subscribe("#")
client.on_message=on_message 

print("004")

# client.loop_forever()

time.sleep(30)
client.loop_stop()