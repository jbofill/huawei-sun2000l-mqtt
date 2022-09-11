from pymodbus.client.sync import ModbusTcpClient as ModbusClient

import time
import sys
import logging


def connect_bus(ip, port=502, timeout=3):
	client = ModbusClient(host=ip, port=port, timeout=timeout, RetryOnEmpty=True, retries=3)
	time.sleep(1)
	client.connect()
	time.sleep(1)
	return client


def close_bus(client):
	client.close()
	time.sleep(1)
	del client


def read_registers(client, unit_id, data):
	try:
		result = None
		nb = int(data['registers'])
		if data['method'] == "hold":
			try:
				result = client.read_holding_registers(int(data['addr']), nb, unit=unit_id)
			except:
				e = sys.exc_info()[0]
				logging.error(e)
		elif data['method'] == "input":
			result = client.read_input_registers(int(data['addr']), nb, unit=unit_id)
		# result.registers[nb - 1]
		if not result:
			result = -1
		time.sleep(0.025)
		return result
	except Exception as e:
		logging.error(f'Exception occurred while code execution: {repr(e)}')
		return -1

