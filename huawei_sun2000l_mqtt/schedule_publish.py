#!/usr/bin/env python3
try:
    from configs import config
except ModuleNotFoundError:
    print('Run setup.py first')
    exit()
try:
    from configs import config_schedule
except ModuleNotFoundError:
    print('Create configs/config_schedule.py first')
    exit()
from paho.mqtt import client as mqtt_client
import random
from operator import itemgetter
from time import sleep
import time
import continuous_threading
import logging
import threading

####################################################################
# MSQTT Brocker
####################################################################


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        global mqtt_connected
        mqtt_connected = False
        if rc == 0:
            mqtt_connected = True
            logging.info("Connected to MQTT Broker!")
        else:
            logging.warning(f"failed to connect, return code {rc}")
    client_mqtt_conn = mqtt_client.Client(client_id='{0}-{1}'.format(config.client_id, random.randint(1, 999)))
    client_mqtt_conn.username_pw_set(config.username, config.password)
    client_mqtt_conn.tls_set(config.ca_certs)
    client_mqtt_conn.tls_insecure_set(True)
    client_mqtt_conn.on_connect = on_connect
    client_mqtt_conn.connect(config.broker, config.port)
    return client_mqtt_conn

def publish_msg(pub_msg, topic=None):
    if not topic:
        topic = topic_mqtt
    # give time so messages are not published at the same moment
    logging.debug(f'waiting lock')
    threadLock.acquire(blocking=True, timeout=-1)
    logging.debug(f'got lock')
    response = client_mqtt.publish(topic, pub_msg)
    threadLock.release()
    logging.debug(f'release lock')
    if not response[0] == 0:
        logging.info("MQTT: Failed to send pub_msg message")
    else:
        logging.info(pub_msg)


if __name__ == "__main__":
    logformat = "%(asctime)s %(threadName)s: %(message)s"
    logging.basicConfig(format=logformat, level=logging.INFO, datefmt="%H:%M:%S")
    topic_mqtt = 'sun2000l/query'
    mqtt_connected = False
    client_mqtt = connect_mqtt()
    client_mqtt.subscribe([("sun2000l/query", 0)])
    client_mqtt.loop_start()
    while not mqtt_connected:
        sleep(1)
    threadLock = threading.Lock()
    logging.info(f'{config_schedule.schedule}')
    threads = []
    threads_tnum = []
    threads_delay = []
    for k in config_schedule.schedule:
        s = config_schedule.schedule[k]
        logging.info(f"Scheduling {k}: {s}")
        tnum = 0.
        if s == 'once_at_start':
            publish_msg(k)
            sleep(2)
        elif s.endswith('m'):
            tnum = float(s.split('m')[0].strip())*60
        elif s.endswith('h'):
            tnum = float(s.split('h')[0].strip())*60*60
        else:
            logging.warning(f'Unknown time value {s}')
        if tnum > 0.:
            if tnum < 60.:
                tnum = 60.
            th = continuous_threading.PeriodicThread(tnum, publish_msg, args=[k])
            th.name = f'thread {k}: {s}'
            threads.append(th)
            threads_tnum.append(tnum)

    logging.info(f'{len(threads)} threads')
    threads_time_sorted = [list(x) for x in zip(*sorted(zip(threads_tnum, threads), key=itemgetter(0), reverse=False))]
    inicial_wait = 60./len(threads)
    for x in threads:
        x.start()
        sleep(inicial_wait)

    sleeping = 600
    while True:
        time.sleep(sleeping)
