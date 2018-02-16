import os
from datetime import datetime

prefixes = []
primaries = []
secondaries = []
data = {}
filenames = {}


def init():
	global prefixes
	prefixes = ["RPMs", "Load", "Throttle", "Coolant", "O2", "Speed", "Gear", "Volts", "RRPot", "RLPot", "FBrake",
		"RBrake"]

	global primaries
	primaries = ["RPMs", "Load", "Throttle", "RRPot", "RLPot", "FBrake", "RBrake"]

	global secondaries
	secondaries = ["Coolant", "O2", "Speed", "Gear", "Volts"]

	global data
	data = {prefix: 0 for prefix in prefixes}
	data['coords'] = []

	# mac gets sad when you use : in file names
	directory = os.path.join(os.getcwd(), "logs", "Engine Data {} {}".format(
		datetime.today().strftime("%m-%d-%Y"), datetime.today().strftime("%H-%M-%S")))
	if not os.path.exists(directory):
		os.makedirs(directory)

	global filenames
	filenames = {prefix: os.path.join(directory, "{}.csv".format(prefix)) for prefix in prefixes}
