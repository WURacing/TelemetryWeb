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
	while not stop_event.is_set():
		if ser.inWaiting() > 0:
			data = ser.read()
			if data == bytes(b'!'):
				data = ser.read()

				# Packet Headers:
				# 0x30 : RPMs
				# 0x31 : Engine Load
				# 0x32 : throttle
				# 0x33 : Coolant Temp (F)
				# 0x34 : O2 level
				# 0x35 : Vehicle Speed (The shitty one from the ECU anyway)
				# 0x36 : Gear (Again, shitty ECU version)
				# 0x37 : Battery Voltage
				# 0x38 : Shock pot sensor on right rear wheel
				# 0x39 : Shock pot sensor on left rear wheel

				if data == bytes(b'0'):
					timestamp = struct.unpack('>I', ser.read(4))[0]
					payload = struct.unpack('>f', ser.read(4))[0]
					# print(payload)
					with lock:
						global_vars.data["RPMs"] = payload
					record(prefix="RPMs", timestamp=timestamp, payload=payload)

				elif data == bytes(b'1'):
					timestamp = struct.unpack('>I', ser.read(4))[0]
					payload = struct.unpack('>f', ser.read(4))[0]
					with lock:
						global_vars.data["Load"] = payload
					record(prefix="Load", timestamp=timestamp, payload=payload)

				elif data == bytes(b'2'):
					timestamp = struct.unpack('>I', ser.read(4))[0]
					payload = struct.unpack('>f', ser.read(4))[0]
					with lock:
						global_vars.data["Throttle"] = payload
					record(prefix="Throttle", timestamp=timestamp, payload=payload)

				elif data == bytes(b'3'):
					timestamp = struct.unpack('>I', ser.read(4))[0]
					payload = struct.unpack('>f', ser.read(4))[0]
					with lock:
						global_vars.data["Coolant"] = payload
					record(prefix="Coolant", timestamp=timestamp, payload=payload)

				elif data == bytes(b'4'):
					timestamp = struct.unpack('>I', ser.read(4))[0]
					payload = struct.unpack('>f', ser.read(4))[0]
					with lock:
						global_vars.data["O2"] = payload
					record(prefix="O2", timestamp=timestamp, payload=payload)

				elif data == bytes(b'5'):
					timestamp = struct.unpack('>I', ser.read(4))[0]
					payload = struct.unpack('>f', ser.read(4))[0]
					with lock:
						global_vars.data["Speed"] = payload
					record(prefix="Speed", timestamp=timestamp, payload=payload)

				elif data == bytes(b'6'):
					timestamp = struct.unpack('>I', ser.read(4))[0]
					payload = int(list(ser.read())[0])
					# print(payload)
					with lock:
						global_vars.data["Gear"] = payload
					record(prefix="Gear", timestamp=timestamp, payload=payload)

				elif data == bytes(b'7'):
					timestamp = struct.unpack('>I', ser.read(4))[0]
					payload = struct.unpack('>f', ser.read(4))[0]
					with lock:
						global_vars.data["Volts"] = payload
					record(prefix="Volts", timestamp=timestamp, payload=payload)

				elif data == bytes(b'8'):
					timestamp = struct.unpack('>I', ser.read(4))[0]
					payload = struct.unpack('>f', ser.read(4))[0]
					with lock:
						global_vars.data["RRPot"] = payload
					record(prefix="RRPot", timestamp=timestamp, payload=payload)

				elif data == bytes(b'9'):
					timestamp = struct.unpack('>I', ser.read(4))[0]
					payload = struct.unpack('>f', ser.read(4))[0]
					with lock:
						global_vars.data["RLPot"] = payload
					record(prefix="RLPot", timestamp=timestamp, payload=payload)

				elif data == bytes(b'@'):
					timestamp = struct.unpack('>I', ser.read(4))[0]
					payload = struct.unpack('>f', ser.read(4))[0]
					with lock:
						global_vars.data["FBrake"] = payload
					record(prefix="FBrake", timestamp=timestamp, payload=payload)

				elif data == bytes(b'A'):
					timestamp = struct.unpack('>I', ser.read(4))[0]
					payload = struct.unpack('>f', ser.read(4))[0]
					with lock:
						global_vars.data["RBrake"] = payload
					record(prefix="RBrake", timestamp=timestamp, payload=payload)

				else:
					print("ERROR: Corrupted Data")
			else:
				pass
		else:
			pass


def cleanup():
	global ser
	ser.close()
