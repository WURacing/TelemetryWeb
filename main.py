import atexit

from flask import Flask, render_template
from flask_sse import sse

import debug_thread
import global_vars
import serial_thread
from serial_ports import get_port

debug = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

sp = None


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


def cleanup():
	sp.stop()


if __name__ == "__main__":

	global_vars.init()

	if not debug:
		port = get_port()
		sp = serial_thread.SerialProcess(port=port, app=app)
		sp.daemon = True
		sp.start()
	else:
		sp = debug_thread.DebugThread(app=app)
		sp.start()

	atexit.register(cleanup)

	app.run(debug=False)
	sp.stop()
