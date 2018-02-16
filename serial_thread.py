import serial
import global_vars
import struct


def init(port):
	global ser
	ser = serial.Serial(port)


def record(prefix, timestamp, payload):
	with open(global_vars.filenames[prefix], 'a') as csvfile:
		csvfile.write(str(timestamp) + ',' + str(payload) + '\n')


def readData(lock, stop_event):
	global ser
	ser.flush()
	print("Start1")
	while not stop_event.is_set():
		# print("wait")
		# if ser.inWaiting() > 0:
		if True:
			print("read")
			data = ser.read()
			print(data)
			if data == b'\x93':
				data = ser.read()
				print(data)
				if data != b'\x01':
					print("badver")
					continue
				with lock:
					print("Got data")
					global_vars.data['Coolant'] = struct.unpack('>b', ser.read(1))[0]
					global_vars.data['O2'] = struct.unpack('>B', ser.read(1))[0]
					global_vars.data['Gear'] = struct.unpack('>H', ser.read(2))[0]
					global_vars.data['RPMs'] = struct.unpack('>H', ser.read(2))[0]
					global_vars.data['Load'] = struct.unpack('>H', ser.read(2))[0]
					global_vars.data['Throttle'] = struct.unpack('>H', ser.read(2))[0]
					global_vars.data['Speed'] = struct.unpack('>H', ser.read(2))[0]
					global_vars.data['Volts'] = struct.unpack('>H', ser.read(2))[0]
					lat = struct.unpack('>i', ser.read(4))[0]
					# TODO make it so we don't have to add the minus sign (fix big endian bug)
					lng = -struct.unpack('>i', ser.read(4))[0]
					global_vars.data['RLPot'] = struct.unpack('>H', ser.read(2))[0]
					global_vars.data['RRPot'] = struct.unpack('>H', ser.read(2))[0]
					global_vars.data['FBrake'] = struct.unpack('>H', ser.read(2))[0]
					global_vars.data['RBrake'] = struct.unpack('>H', ser.read(2))[0]
					timestamp = struct.unpack('>I', ser.read(4))[0]
					if not lat == 0 and not lng == 0:
						global_vars.data['coords'].append({'lat': lat / 10000000, 'lng': lng / 10000000})
					print("Finished reading")

def cleanup():
	global ser
	ser.close()
