import paho.mqtt.client as mqtt
import time
import configparser
import sys

print("001")

config = configparser.RawConfigParser(allow_no_value=True)
config.read("watermeter_config.ini")

print("002")

log_path = config.get('Logging', 'log_path', fallback='/var/log/solar/')
do_raw_log = config.getboolean('Logging', 'do_raw_log')

mqttBroker = config.get('watermeter', 'mqttBroker')
mqttPort = int(config.get('watermeter', 'mqttPort'))
mqttKeepAlive = int(config.get('watermeter', 'mqttKeepAlive'))

print(mqttBroker)

def on_message(client, userdata, msg):
    print(str(msg.payload))
    print(msg.topic + " " + str(msg.payload) )

print("003")

client = mqtt.Client("reader")
client.connect(mqttBroker, mqttPort, mqttKeepAlive) 

print("004")

client.loop_start()

print("005")

client.subscribe("#")
client.on_message=on_message 

print("006")

# client.loop_forever()

print("007")

time.sleep(30)

print("008")

client.loop_stop()