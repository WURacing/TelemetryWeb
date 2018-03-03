import threading

import time

import math
from flask_sse import sse

dashboard_k = ["RPMs", "Load", "Throttle", "Coolant", "O2", "Speed", "Gear", "Volts", "RRPot", "RLPot", "FBrake",
	"RBrake"]
maps_k = ["lat", "lng"]


class DebugThread(threading.Thread):
	def __init__(self, app):
		super(DebugThread, self).__init__()
		self.debug_data = {prefix: 0 for prefix in dashboard_k + maps_k}
		self.app = app
		self._stop_event = threading.Event()

	def run(self):
		while not self.stopped():
			time.sleep(0.1)
			self.generate_debug_data()

	def generate_debug_data(self):
		with self.app.app_context():
			self.debug_data["RPMs"] += 100
			self.debug_data["Coolant"] += 15.5
			self.debug_data["Throttle"] += 10.2
			self.debug_data["Load"] = 10.5
			self.debug_data["Volts"] = 12.0
			self.debug_data["O2"] = 1.2
			if self.debug_data["RPMs"] > 12000:
				self.debug_data["RPMs"] = 0
			if self.debug_data["Coolant"] > 200:
				self.debug_data["Coolant"] = 140
			if self.debug_data["Throttle"] > 80:
				self.debug_data["Throttle"] = 0
			self.debug_data["lat"] = 38.6483189 + 0.001 * math.sin(self.debug_data["RPMs"] / 12000 * 2 * math.pi)
			self.debug_data["lng"] = -90.3075894 + 0.001 * math.cos(self.debug_data["RPMs"] / 12000 * 2 * math.pi)
			message = self.debug_data
			dashboard = {key: value for key, value in message.items() if key in dashboard_k}
			sse.publish(dashboard, type='dashboard')
			maps = {key: value for key, value in message.items() if key in maps_k}
			sse.publish(maps, type='maps')

	def stop(self):
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()
