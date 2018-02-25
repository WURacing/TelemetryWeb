import atexit
import math
import multiprocessing
import time
from threading import Thread

from flask import Flask, render_template
from flask_sse import sse

import global_vars
import serial_thread
from serial_ports import get_port

debug = True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

output_queue = multiprocessing.Queue()
read_thread = None


@app.route('/')
def dash():
	statics = [('js', 'dash-client.js'), ('css', 'dash-style.css')]
	return render_template('dash.html', statics=statics)


@app.route('/plots')
def plots():
	statics = [('js', 'jquery.flot.min.js'), ('js', 'plots-client.js'), ('css', 'base.css'),
		('css', 'chart-modules.css'), ('css', 'pure-min.css')]
	return render_template('plots.html', statics=statics)


@app.route('/maps')
def maps():
	statics = [('css', 'base.css'), ('css', 'pure-min.css')]
	mdata = {'center': {'lat': 38.64831890000001, 'lng': -90.3075894}, 'zoom': 16,
		'coords': []}
	return render_template('maps.html', statics=statics, map=mdata)


dashboard_k = ["RPMs", "Load", "Throttle", "Coolant", "O2", "Speed", "Gear", "Volts", "RRPot", "RLPot", "FBrake",
	"RBrake"]
maps_k = ["lat", "lng"]
if debug:
	debug_data = {prefix: 0 for prefix in dashboard_k + maps_k}


def checkQueue():
	with app.app_context():
		if debug:
			debug_data["RPMs"] += 100
			debug_data["Coolant"] += 15.5
			debug_data["Throttle"] += 10.2
			debug_data["Load"] = 10.5
			debug_data["Volts"] = 12.0
			debug_data["O2"] = 1.2
			if debug_data["RPMs"] > 12000:
				debug_data["RPMs"] = 0
			if debug_data["Coolant"] > 200:
				debug_data["Coolant"] = 140
			if debug_data["Throttle"] > 80:
				debug_data["Throttle"] = 0
			debug_data["lat"] = 38.6483189 + 0.001 * math.sin(debug_data["RPMs"] / 12000 * 2 * math.pi)
			debug_data["lng"] = -90.3075894 + 0.001 * math.cos(debug_data["RPMs"] / 12000 * 2 * math.pi)
			message = debug_data
			dashboard = {key: value for key, value in message.items() if key in dashboard_k}
			sse.publish(dashboard, type='dashboard')
			maps = {key: value for key, value in message.items() if key in maps_k}
			sse.publish(maps, type='maps')
		elif not output_queue.empty():
			message = output_queue.get()
			dashboard = {key: value for key, value in message.items() if key in dashboard_k}
			sse.publish(dashboard, type='dashboard')
			maps = {key: value for key, value in message.items() if key in maps_k}
			sse.publish(maps, type='maps')


class QueueThread(Thread):
	def __init__(self):
		super(QueueThread, self).__init__()

	def run(self):
		while True:
			time.sleep(0.1)
			checkQueue()


def cleanup():
	pass


if __name__ == "__main__":

	global_vars.init()

	if not debug:
		port = get_port()
		sp = serial_thread.SerialProcess(output_queue, port=port)
		sp.daemon = True
		sp.start()
	read_thread = QueueThread()
	read_thread.start()

	atexit.register(cleanup)

	app.run(debug=False)
