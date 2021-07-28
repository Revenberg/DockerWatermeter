import paho.mqtt.client as mqtt
import time
import configparser
import sys

config = configparser.RawConfigParser(allow_no_value=True)
config.read("watermeter_config.ini")

log_path = config.get('Logging', 'log_path', fallback='/var/log/solar/')
do_raw_log = config.getboolean('Logging', 'do_raw_log')

print("test")
mqttBroker = config.get('watermeter', 'mqttBroker')

print(mqttBroker)

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

client = mqtt.Client("reader")
client.connect(mqttBroker) 

client.loop_start()

client.subscribe("#")
client.on_message=on_message 

time.sleep(30)
client.loop_stop()