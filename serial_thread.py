import multiprocessing

import serial
import global_vars
import struct
import time
from flask_sse import sse


class SerialProcess(multiprocessing.Process):
	def __init__(self, port='/dev/master', baud=9600, app=None):
		multiprocessing.Process.__init__(self)
		self.ser = serial.Serial(port, baud, timeout=1)
		self.app = app

	def close(self):
		self.ser.close()

	def read_packet(self):
		if self.ser.read() != b'!':
			return

		key = struct.unpack('>B', self.ser.read())[0]
		timestamp = struct.unpack('>I', self.ser.read(4))[0]
		print("Read {key:x} at {timestamp}".format(key=key, timestamp=timestamp))
		if key == 0x30:
			self.push('dashboard', {'RPMs': struct.unpack('>f', self.ser.read(4))[0], 'Time': timestamp})
		if key == 0x31:
			self.push('dashboard', {'Load': struct.unpack('>f', self.ser.read(4))[0], 'Time': timestamp})
		if key == 0x32:
			self.push('dashboard', {'Throttle': struct.unpack('>f', self.ser.read(4))[0], 'Time': timestamp})
		if key == 0x33:
			self.push('dashboard', {'Coolant': struct.unpack('>f', self.ser.read(4))[0], 'Time': timestamp})
		if key == 0x34:
			self.push('dashboard', {'O2': struct.unpack('>f', self.ser.read(4))[0], 'Time': timestamp})
		if key == 0x35:
			self.push('dashboard', {'Speed': struct.unpack('>f', self.ser.read(4))[0], 'Time': timestamp})
		if key == 0x36:
			self.push('dashboard', {'Gear': struct.unpack('>B', self.ser.read())[0], 'Time': timestamp})
		if key == 0x37:
			self.push('dashboard', {'Volts': struct.unpack('>f', self.ser.read(4))[0], 'Time': timestamp})
		if key == 0x38:
			self.push('dashboard', {'RRPot': struct.unpack('>f', self.ser.read(4))[0], 'Time': timestamp})
		if key == 0x39:
			self.push('dashboard', {'RLPot': struct.unpack('>f', self.ser.read(4))[0], 'Time': timestamp})
		if key == 0x40:
			self.push('dashboard', {'FBrake': struct.unpack('>f', self.ser.read(4))[0], 'Time': timestamp})
		if key == 0x41:
			self.push('dashboard', {'RBrake': struct.unpack('>f', self.ser.read(4))[0], 'Time': timestamp})
		if key == 0x42:
			self.push('maps', {'lat': struct.unpack('>i', self.ser.read(4))[0] / 10000000, 'Time': timestamp})
		if key == 0x43:
			self.push('maps', {'lng': -struct.unpack('>i', self.ser.read(4))[0] / 10000000, 'Time': timestamp})

	def push(self, key: str, value: dict):
		with self.app.app_context():
			sse.publish(value, type=key)
		prefix = (set(value.keys()) - {'Time'}).pop()
		global_vars.record(prefix, value['Time'], value[prefix])

	def run(self):
		while True:
			if self.ser.in_waiting > 0:
				self.read_packet()
			time.sleep(0.00001)

	def stop(self):
		self.close()
		self.terminate()
		self.close()
