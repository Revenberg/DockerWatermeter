import paho.mqtt.client as mqtt
import time
import configparser
import sys

config = configparser.RawConfigParser(allow_no_value=True)
config.read("watermeter_config.ini")

log_path = config.get('Logging', 'log_path', fallback='/var/log/solar/')
do_raw_log = config.getboolean('Logging', 'do_raw_log')

mqttBroker = config.get('watermeter', 'mqttBroker')
mqttPort = config.get('watermeter', 'mqttPort')
mqttKeepAlive = config.get('watermeter', 'mqttKeepAlive')

print(mqttBroker)

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

client = mqtt.Client("reader")
client.connect(mqttBroker, mqttPort, mqttKeepAlive) 

client.loop_start()

client.subscribe("+/watermeter/#")
client.on_connect = on_connect
client.on_message=on_message 

# client.loop_forever()

time.sleep(900)
client.loop_stop()