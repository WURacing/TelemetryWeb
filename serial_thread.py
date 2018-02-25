import multiprocessing

import serial
import global_vars
import struct
import time


def record(prefix, timestamp, payload):
	with open(global_vars.filenames[prefix], 'a') as csvfile:
		csvfile.write(str(timestamp) + ',' + str(payload) + '\n')


class SerialProcess(multiprocessing.Process):
	def __init__(self, output_queue: multiprocessing.Queue, port='/dev/master', baud=9600):
		multiprocessing.Process.__init__(self)
		self.output_queue = output_queue
		self.ser = serial.Serial(port, baud, timeout=1)

	def close(self):
		self.ser.close()

	def read_packet(self):
		if self.ser.read() != b'\x93':
			return
		if self.ser.read() != b'\x01':
			print("Bad serial packet version")
			return

		coolant = struct.unpack('>b', self.ser.read(1))[0]
		o2 = struct.unpack('>B', self.ser.read(1))[0]
		gear = struct.unpack('>H', self.ser.read(2))[0]
		rpm = struct.unpack('>H', self.ser.read(2))[0]
		load = struct.unpack('>H', self.ser.read(2))[0]
		throttle = struct.unpack('>H', self.ser.read(2))[0]
		speed = struct.unpack('>H', self.ser.read(2))[0]
		volts = struct.unpack('>H', self.ser.read(2))[0]
		lat = struct.unpack('>i', self.ser.read(4))[0] / 10000000
		# TODO make it so we don't have to add the minus sign (fix big endian bug)
		lng = -struct.unpack('>i', self.ser.read(4))[0] / 10000000
		rlpot = struct.unpack('>H', self.ser.read(2))[0]
		rrpot = struct.unpack('>H', self.ser.read(2))[0]
		fbrake = struct.unpack('>H', self.ser.read(2))[0]
		rbrake = struct.unpack('>H', self.ser.read(2))[0]
		timestamp = struct.unpack('>I', self.ser.read(4))[0]
		pack = {'RPMs': rpm, 'Load': load, 'Throttle': throttle, 'Coolant': coolant, 'O2': o2, 'Speed': speed,
			'Gear': gear, 'Volts': volts, 'RRPot': rrpot, 'RLPot': rlpot, 'FBrake': fbrake, 'RBrake': rbrake,
			'lat': lat, 'lng': lng, 'Time': timestamp}
		self.output_queue.put(pack)
		print(f"Read packet sent at {timestamp}")

	def run(self):
		while True:
			if self.ser.in_waiting > 0:
				self.read_packet()
			time.sleep(0.1)
