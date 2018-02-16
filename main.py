import random

from flask import Flask, render_template, url_for
from flask_socketio import SocketIO
from threading import Thread, Lock, Event
from serial_ports import get_port

import time
import eventlet
import atexit
import global_vars
import serial_thread

debug = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# eventlet.monkey_patch()

ser_thread = None
emit_thread1 = None
emit_thread2 = None
lock = Lock()
stop_event = Event()


def respawn_threads_if_needed():
	global emit_thread1
	global emit_thread2

	if emit_thread1 is None:
		emit_thread1 = Thread(target=emitData, args=(global_vars.primaries, 0.2))
		emit_thread1.start()

	if emit_thread2 is None:
		emit_thread2 = Thread(target=emitData, args=(global_vars.secondaries, 1))
		emit_thread2.start()


@app.route('/')
def dash():
	respawn_threads_if_needed()
	statics = [('js', 'dash-client.js'), ('css', 'dash-style.css')]
	return render_template('dash.html', statics=statics)


@app.route('/plots')
def plots():
	respawn_threads_if_needed()
	statics = [('js', 'jquery.flot.min.js'), ('js', 'plots-client.js'), ('css', 'base.css'),
		('css', 'chart-modules.css'), ('css', 'pure-min.css')]
	return render_template('plots.html', statics=statics)


@app.route('/maps')
def maps():
	respawn_threads_if_needed()
	statics = [('css', 'base.css'), ('css', 'pure-min.css')]
	mdata = {'center': {'lat': 38.64831890000001, 'lng': -90.3075894}, 'zoom': 16,
		'coords': global_vars.data['coords']}
	return render_template('maps.html', statics=statics, map=mdata)


def emitData(keys, delay):
	global lock
	global stop_event
	while not stop_event.is_set():
		with lock:
			if debug:
				global_vars.data["RPMs"] += 100
				global_vars.data["Coolant"] += 15.5
				global_vars.data["Throttle"] += 10.2
				global_vars.data["Load"] = 10.5
				global_vars.data["Volts"] = 12.0
				global_vars.data["O2"] = 1.2
				if global_vars.data["RPMs"] > 12000:
					global_vars.data["RPMs"] = 0
				if global_vars.data["Coolant"] > 200:
					global_vars.data["Coolant"] = 140
				if global_vars.data["Throttle"] > 80:
					global_vars.data["Throttle"] = 0
			message = {key: global_vars.data[key] for key in keys}
		# print(message)
		socketio.emit('message', message)
		time.sleep(delay)


def cleanup():
	global stop_event
	stop_event.set()
	if emit_thread1 is not None:
		emit_thread1.join()
	if emit_thread2 is not None:
		emit_thread2.join()
	if ser_thread is not None:
		ser_thread.join()
	if not debug:
		serial_thread.cleanup()


if __name__ == "__main__":

	global_vars.init()

	if not debug:
		serial_thread.init(get_port())
		ser_thread = Thread(target=serial_thread.readData, args=(lock, stop_event))
		ser_thread.start()

	atexit.register(cleanup)

	socketio.run(app)
