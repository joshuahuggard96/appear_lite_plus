from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_socketio import SocketIO, emit
from functools import wraps
import os
import logging
from dotenv import load_dotenv

from src.database.db import Database
from src.handlers.serial_handler import SerialHandler
from src.handlers.tap_handler import TAPHandler
from src.handlers.serial_ip_handler import SerialIPHandler

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize SocketIO with threading mode (compatible with Python 3.13)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Setup logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize database
db = Database(os.getenv('DB_PATH', 'data/appear.db'))

# Initialize handlers
serial_handler = None
tap_handler = None
serial_ip_handler = None

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def alarm_callback(alarm_data):
    """Callback when new alarm received - send to connected apps"""
    socketio.emit('new_alarm', alarm_data, namespace='/app')
    logger.info(f"Alarm broadcasted to connected apps: {alarm_data['id']}")

# Routes
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if db.verify_user(username, password):
            session['user'] = username
            logger.info(f"User {username} logged in")
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/logout')
def logout():
    user = session.pop('user', None)
    if user:
        logger.info(f"User {user} logged out")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    stats = db.get_alarm_stats()
    return render_template('dashboard.html', stats=stats, user=session['user'])

@app.route('/alarms')
@login_required
def alarms():
    recent_alarms = db.get_recent_alarms(limit=100)
    return render_template('alarms.html', alarms=recent_alarms, user=session['user'])

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Update settings
        for key in request.form:
            if key.startswith('setting_'):
                setting_key = key.replace('setting_', '')
                db.update_setting(setting_key, request.form[key])

        # Restart handlers if needed
        restart_handlers()

        return redirect(url_for('settings'))

    all_settings = db.get_all_settings()
    handler_status = {
        'serial': serial_handler.is_running() if serial_handler else False,
        'tap': tap_handler.is_running() if tap_handler else False,
        'serial_ip': serial_ip_handler.is_running() if serial_ip_handler else False
    }
    return render_template('settings.html', settings=all_settings, status=handler_status, user=session['user'])

@app.route('/debug')
@login_required
def debug():
    recent_alarms = db.get_recent_alarms(limit=50)
    all_settings = db.get_all_settings()
    handler_status = {
        'serial': serial_handler.is_running() if serial_handler else False,
        'tap': tap_handler.is_running() if tap_handler else False,
        'serial_ip': serial_ip_handler.is_running() if serial_ip_handler else False
    }
    return render_template('debug.html', alarms=recent_alarms, settings=all_settings, status=handler_status, user=session['user'])

# API Routes for phone app
@app.route('/api/alarms/latest', methods=['GET'])
def api_latest_alarms():
    """Get latest alarms for phone app"""
    limit = request.args.get('limit', 50, type=int)
    alarms = db.get_recent_alarms(limit=limit)
    return jsonify([dict(alarm) for alarm in alarms])

@app.route('/api/alarms/<int:alarm_id>/mark_sent', methods=['POST'])
def api_mark_alarm_sent(alarm_id):
    """Mark alarm as sent to app"""
    db.mark_alarm_sent(alarm_id)
    return jsonify({'status': 'success'})

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get alarm statistics"""
    stats = db.get_alarm_stats()
    return jsonify(stats)

# SocketIO events for phone app
@socketio.on('connect', namespace='/app')
def handle_app_connect():
    logger.info("Phone app connected")
    emit('connected', {'status': 'connected'})

@socketio.on('disconnect', namespace='/app')
def handle_app_disconnect():
    logger.info("Phone app disconnected")

@socketio.on('subscribe', namespace='/app')
def handle_subscribe(data):
    logger.info(f"Phone app subscribed: {data}")
    emit('subscribed', {'status': 'subscribed'})

def start_handlers():
    """Start serial, TAP, and Serial over IP handlers based on settings"""
    global serial_handler, tap_handler, serial_ip_handler

    # Start serial handler if enabled
    if db.get_setting('serial_enabled', 'false').lower() == 'true':
        try:
            serial_port = db.get_setting('serial_port', '/dev/ttyUSB0')
            serial_baud = db.get_setting('serial_baud_rate', '9600')
            serial_handler = SerialHandler(serial_port, serial_baud, alarm_callback)
            serial_handler.start()
        except Exception as e:
            logger.error(f"Failed to start serial handler: {e}")

    # Start TAP handler if enabled
    if db.get_setting('tap_enabled', 'false').lower() == 'true':
        try:
            tap_host = db.get_setting('tap_host', '0.0.0.0')
            tap_port = db.get_setting('tap_port', '18001')
            tap_handler = TAPHandler(tap_host, tap_port, alarm_callback)
            tap_handler.start()
        except Exception as e:
            logger.error(f"Failed to start TAP handler: {e}")

    # Start Serial over IP handler if enabled
    if db.get_setting('serial_ip_enabled', 'false').lower() == 'true':
        try:
            serial_ip_host = db.get_setting('serial_ip_host', 'localhost')
            serial_ip_port = db.get_setting('serial_ip_port', '5001')
            serial_ip_handler = SerialIPHandler(serial_ip_host, serial_ip_port, alarm_callback)
            serial_ip_handler.start()
        except Exception as e:
            logger.error(f"Failed to start Serial over IP handler: {e}")

def restart_handlers():
    """Restart handlers with new settings"""
    global serial_handler, tap_handler, serial_ip_handler

    # Stop existing handlers
    if serial_handler:
        serial_handler.stop()
    if tap_handler:
        tap_handler.stop()
    if serial_ip_handler:
        serial_ip_handler.stop()

    # Start with new settings
    start_handlers()

if __name__ == '__main__':
    logger.info("Starting Appear Lite Plus server...")
    start_handlers()

    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))

    socketio.run(app, host=host, port=port, debug=True, allow_unsafe_werkzeug=True)
