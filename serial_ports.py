import sys
import glob
import serial


def serial_ports():
	if sys.platform.startswith('win'):
		ports = ['COM%s' % (i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this excludes your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')

	result = []
	for port in ports:
		try:
			# s = serial.Serial(port)
			# s.close()
			result.append(port)
		except (OSError, serial.SerialException):
			pass
	return result


def get_port():
	ports = serial_ports()
	if ports != []:
		if len(ports) == 1:
			print("Using port {}".format(ports[0]))
			return ports[0]
		print("The following serial ports are available:")
		print(ports)
		port = input("Please enter the XBee radio port:")
		if port in ports:
			return port
		else:
			print("-- Port not recognized, please try again --")
			return get_port()
	else:
		print("No serial ports found")
		sys.exit()


if __name__ == '__main__':
	print(get_port())
