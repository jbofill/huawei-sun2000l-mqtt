# !/usr/bin/python3

try:
    from huawei_sun2000l_mqtt.configs import config
except ModuleNotFoundError:
    print('Run setup.py first')
    exit()
from huawei_sun2000l_mqtt.lib import Huawei
from huawei_sun2000l_mqtt.lib.modbustcp import connect_bus, read_registers, close_bus
import time
import asyncio
import json
import ssl
import pathlib

from paho.mqtt import client as mqtt_client
import random
from time import sleep

import logging


def to_str(s):
    str_return = ""
    for i in range(0, len(s)):
        high, low = divmod(s[i], 0x100)
        if high != 0:
            str_return = str_return + chr(high)
        if low != 0:
            str_return = str_return + chr(low)
    return str_return


def to_U16(i):
    return i[0] & 0xffff


def to_I16(i):
    i = i[0] & 0xffff
    return (i ^ 0x8000) - 0x8000


def to_U32(i):
    return (i[0] << 16) + i[1]


def to_I32(i):
    i = ((i[0] << 16) + i[1])
    i = i & 0xffffffff
    return (i ^ 0x80000000) - 0x80000000


def to_Bit16(i):
    return i[0]


def to_Bit32(i):
    return (i[0] << 16) + i[1]


def call_function(method_name, values):
    method_name = "to_" + method_name
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    if not method:
        return 'no_method_error', None
    try:
        return '', method(values)
    except:
        return "error in call_function".format(method_name, values), None


def read_inverter(options):
    def get_registers(interface_definitions, definition_group):

        get_error = False

        conn = connect_bus(ip=config.inverter_ip,
                           port=config.inverter_port,
                           timeout=config.timeout)
        out = ""
        values = []
        values_new = {}
        if conn:
            time.sleep(0.5)
            for register in definition_group:
                result = None
                k = 0
                while True:
                    try:
                        result = read_registers(conn, config.slave, interface_definitions.register_map[register])
                        break
                    except:
                        if result == -1:
                            time.sleep(0.3)
                            k += 1
                            if k > 3:
                                break
                        else:
                            raise

                if result == -1:
                    get_error = 'Read register error'
                    break
                if hasattr(result, 'registers'):
                    get_error, value = call_function(interface_definitions.register_map[register]['type'], result.registers)
                else:
                    get_error = "'ModbusIOException' object has no attribute 'registers'"
                    logging.info("'ModbusIOException' object has no attribute 'registers'")
                if get_error:
                    break
                if (interface_definitions.register_map[register]['type'] != 'str') and (
                        interface_definitions.register_map[register]['scale'] != 1):
                    value = value / interface_definitions.register_map[register]['scale']

                if interface_definitions.register_map[register]['units'] == 's':
                    if value > 2600000000:
                        continue
                    value = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(value))
                elif interface_definitions.register_map[register]['use'] == "stat":
                    value = interface_definitions.status(register, value)
                if register == 'Time':
                    value = value.split()[1]
                values.append('"{register}":"{val}"'.format(register=register, val=value))
                values_new[register] = {'value': value,
                                        'measurement': interface_definitions.register_map[register]['measurement'],
                                        'fieldname': interface_definitions.register_map[register]['fieldname']
                                        }
            close_bus(conn)
            if not get_error:
                out = '{' + ','.join(values) + '}'
                logging.debug(out)
        else:
            get_error = 'Connection error'

        return get_error, out, values_new

    logging.debug(f'reading... {options}')
    if options.find(':') >= 0:
        group_type, group_options = options.split(':')
        group_type = group_type.strip()
        group_options = group_options.strip()
        group_group = [register for register in reg_map if
                       reg_map[register][group_type] == group_options]
    else:
        group_group = options.split()
    retry = 3
    j = 0
    registers_mesure = {}
    while j < retry:
        error, registers, registers_mesure = get_registers(inverter_interface_definitions, group_group)
        if error:
            logging.error(error)
            time.sleep(2)
            j += 1
        else:
            break
    if j == retry:
        logging.info("Unable to get results")
    elif registers_mesure:
        return registers_mesure


####################################################################
# MSQTT Brocker
####################################################################

def connect_mqtt():
    def on_connect(client_m, userdata, flags, rc):
        global subscribe
        if rc == 0:
            logging.info("Connected to MQTT Broker!")
            logging.info(f'Subscribing {subscribe}')
            client_m.subscribe(subscribe)
        else:
            logging.warning(f"failed to connect, return code {rc}")

    def on_disconnect(client_m, userdata, rc):
        if rc != 0:
            logging.warning(f"Unexpected MQTT disconnection {rc}. Will auto-reconnect and subscribe")
            client_m.reconnect()

    client_mqtt_conn = mqtt_client.Client(client_id='{0}-{1}'.format(config.client_id, random.randint(1, 999)))
    client_mqtt_conn.username_pw_set(config.username, config.password)
    client_mqtt_conn.tls_set(config.ca_certs)
    client_mqtt_conn.tls_insecure_set(True)
    client_mqtt_conn.on_connect = on_connect
    client_mqtt_conn.connect(config.broker, config.port)
    client_mqtt_conn.on_disconnect = on_disconnect
    return client_mqtt_conn


def on_message(client_m, userdata, msg_in):
    global wakeup, query_input, group_query
    logging.info(f"Message received {msg_in.topic}: {msg_in.payload}")
    if msg_in.topic == 'sun2000l/query':
        query_input = msg_in.payload.decode('utf-8')
        if query_input.find(':') >= 0:
            group_type, group_options = query_input.split(':')
            group_type = group_type.strip()
            if group_type in reg_map['Model'].keys():
                group_options = group_options.strip()
                group_query = [register for register in reg_map if
                               reg_map[register][
                                   group_type] == group_options]
            else:
                logging.warning(f"group type not found {group_type}. Posible groups are: {reg_map['Model'].keys()}")
        else:
            query = ''
            for q in query_input.split():
                if q in reg_map:
                    query += ' ' + q
            group_query = query
        wakeup = True
    else:
        logging.warning(f'topic unkown {msg_in.topic}')


def publish_msg(pub_msg, topic=None):
    if not topic:
        topic = topic_mqtt
    response = client_mqtt.publish(topic, json.dumps(pub_msg, default=str))
    logging.info(f'publising {topic} {pub_msg}')
    if not response[0] == 0:
        logging.warning(f"MQTT: Failed to send {pub_msg} message")


def wait(time_wait, delta_time=5):
    global wakeup
    wakeup = False
    t = 0
    while t < time_wait and not wakeup:
        sleep(delta_time)
        t += delta_time
    if wakeup:
        logging.debug(f'sleeping for {time_wait}, but after {t} wakeup!')
        wakeup = False
    return t


ssl_context = None
if config.use_wss:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    localhost_pem = pathlib.Path(__file__).with_name("key_cert.pem")
    ssl_context.load_cert_chain(localhost_pem)


async def client(data_query, grp_query):
    response = read_inverter(data_query)
    logging.debug(f'data_query: {data_query} group_query: {grp_query} response: {response}')
    for x in response.keys():
        if x == 'P_active':
            response[x]['value'] = int(response[x]['value'] * 1000)  # change units to W
        topic_pub = '{}/{}'.format(response[x]['measurement'], response[x]['fieldname'])
        value_pub = response[x]['value']
        publish_msg(value_pub, topic_pub)
    if data_query == 'group:monitor':
        grid_consumption = 0
        grid_surplus = 0
        if response['M_P']['value'] < 0:
            grid_consumption = -response['M_P']['value']
        else:
            grid_surplus = response['M_P']['value']
        home_consumption = response['P_active']['value'] - response['M_P']['value']
        publish_msg(grid_consumption, 'grid/consumption')
        publish_msg(grid_surplus, 'grid/surplus')
        publish_msg(home_consumption, 'home/consumption')


if __name__ == '__main__':

    logformat = "%(asctime)s: %(message)s"
    logging.basicConfig(format=logformat, level=logging.INFO, datefmt="%H:%M:%S")

    inverter_interface_definitions = Huawei
    reg_map = Huawei.register_map

    topic_mqtt = 'sun2000l/results'
    client_mqtt = connect_mqtt()
    client_mqtt.on_message = on_message
    subscribe = [("sun2000l/query", 0)]
    client_mqtt.loop_start()
    wakeup = False
    query_input = ''
    group_query = ''
    sleep_time = 60
    while True:
        while query_input == '':
            time_elapsed = wait(sleep_time)
            if query_input != '':
                logging.debug(f'{query_input}')
                wakeup = False
            else:
                logging.info(f'No command, sleeping {sleep_time / 60} minuts')
        if query_input and group_query:
            logging.debug(f'{query_input} {group_query}')
            # asyncio.get_event_loop().run_until_complete(client(query_input))
            asyncio.run(client(query_input, group_query))
        else:
            logging.info('No query')
        query_input = ''
