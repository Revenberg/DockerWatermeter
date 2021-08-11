import paho.mqtt.client as mqtt
import time
import configparser
import sys
import json
import datetime
import init_db
from influxdb import InfluxDBClient

print("watermeter 30-7-2021 22:37")

config = configparser.RawConfigParser(allow_no_value=True)
config.read("watermeter_config.ini")

log_path = config.get('Logging', 'log_path', fallback='/var/log/watermeter/')
do_raw_log = config.getboolean('Logging', 'do_raw_log')

mqttBroker = config.get('Watermeter', 'mqttBroker')
mqttPort = int(config.get('Watermeter', 'mqttPort'))
mqttKeepAlive = int(config.get('Watermeter', 'mqttKeepAlive'))

influx_server = config.get('InfluxDB', 'influx_server')
influx_port = int(config.get('InfluxDB', 'influx_port'))
influx_database = config.get('InfluxDB', 'database')
influx_measurement = config.get('InfluxDB', 'measurement')

values = dict()

previous_value = 0

def on_message(mqtt_client, userdata, msg):
    global values
    today = datetime.datetime.now()

    if msg.topic.lower() == "watermeter/reading/current_value" :        
        if previous_value > 0:
            values['current_value'] = int(str(msg.payload.decode("utf-8")))
            values['usages'] = int(str(msg.payload.decode("utf-8"))) - previous_value
        else:
            values['current_value'] = int(str(msg.payload.decode("utf-8")))
            values['usages'] = 0
        values['datetime'] = today.strftime("%d/%m/%Y %H:%M:%S")    

    if msg.topic.lower() == "watermeter/reading/pulse_count" :
        values['pulse_count'] = int(str(msg.payload.decode("utf-8")))
        values['datetime'] = today.strftime("%d/%m/%Y %H:%M:%S")
    
def getData(mqttBroker, mqttPort, mqttKeepAlive):
    global values
    
    mqtt_client = mqtt.Client("reader")

    mqtt_client.connect(mqttBroker, mqttPort, mqttKeepAlive)

    while True:
        mqtt_client.loop_start()

        mqtt_client.subscribe("#")
        mqtt_client.on_message=on_message

        time.sleep(60)

        if values['current_value'] > 0:
            json_body = {'points': [{
                            'fields': {k: v for k, v in values.items()}
                                    }],
                        'measurement': influx_measurement
                        }        
            
            print( json.dumps(json_body) )
            sys.stdout.flush()

            client = InfluxDBClient(host=influx_server,
                            port=influx_port)

            success = client.write(json_body,
                                # params isneeded, otherwise error 'database is required' happens
                                params={'db': influx_database})

            if not success:
                print('error writing to database')
        
        mqtt_client.loop_stop()

getData(mqttBroker, mqttPort, mqttKeepAlive)
