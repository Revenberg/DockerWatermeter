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

def on_message(mqtt_client, userdata, msg):
    global values
    today = datetime.datetime.now()

    if msg.topic .lower() == "watermeter/reading/current_value" :
        values['current_value'] = int(str(msg.payload.decode("utf-8")))
        values['datetime'] = today.strftime("%d/%m/%Y %H:%M:%S")

    if msg.topic .lower() == "watermeter/reading/pulse_count" :
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

def openDatabase():
    # if the db is not found, then try to create it
    try:
        dbclient = InfluxDBClient(host=influx_server, port=influx_port )
        dblist = dbclient.get_list_database()
        db_found = False
        for db in dblist:
            if db['name'] == influx_database:
                db_found = True
        if not(db_found):
            print( dbclient.get_list_continuous_queries())
            sys.exit('Database ' + influx_database + ' not found, create it')

    except Exception as e:
        print(e)
        sys.exit('Error querying open influx_server: ' + influx_server)

openDatabase()

getData(mqttBroker, mqttPort, mqttKeepAlive)