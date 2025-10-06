import sqlite3
import os
import bcrypt
from datetime import datetime

class Database:
    def __init__(self, db_path='data/appear.db'):
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Alarms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alarms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                message TEXT NOT NULL,
                raw_data TEXT,
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed BOOLEAN DEFAULT 0,
                sent_to_app BOOLEAN DEFAULT 0
            )
        ''')

        # Alarm rules table for future expansion
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alarm_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                enabled BOOLEAN DEFAULT 1,
                conditions TEXT,
                actions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Insert default admin user if not exists
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            hashed_password = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         ('admin', hashed_password.decode('utf-8')))
            print("Created default admin user (admin/admin)")

        # Insert default settings if not exists
        default_settings = [
            ('serial_enabled', 'false', 'Enable serial port monitoring'),
            ('serial_port', '/dev/ttyUSB0', 'Serial port device path'),
            ('serial_baud_rate', '9600', 'Serial port baud rate'),
            ('tap_enabled', 'true', 'Enable TAP over IP'),
            ('tap_port', '18001', 'TAP over IP port'),
            ('tap_host', 'localhost', 'TAP over IP bind address'),
            ('serial_ip_enabled', 'true', 'Enable Serial over IP'),
            ('serial_ip_port', '5001', 'Serial over IP port'),
            ('serial_ip_host', 'localhost', 'Serial over IP bind address'),
        ]

        for key, value, description in default_settings:
            cursor.execute('INSERT OR IGNORE INTO settings (key, value, description) VALUES (?, ?, ?)',
                         (key, value, description))

        conn.commit()
        conn.close()
        print(f"Database initialized at {self.db_path}")

    # User methods
    def get_user(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user

    def verify_user(self, username, password):
        user = self.get_user(username)
        if user:
            return bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))
        return False

    # Settings methods
    def get_setting(self, key, default=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        return result['value'] if result else default

    def get_all_settings(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM settings ORDER BY key')
        settings = cursor.fetchall()
        conn.close()
        return settings

    def update_setting(self, key, value):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO settings (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET value=?, updated_at=CURRENT_TIMESTAMP
        ''', (key, value, value))
        conn.commit()
        conn.close()

    # Alarm methods
    def save_alarm(self, source, message, raw_data=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alarms (source, message, raw_data, received_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (source, message, raw_data))
        alarm_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return alarm_id

    def mark_alarm_sent(self, alarm_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE alarms SET sent_to_app = 1 WHERE id = ?', (alarm_id,))
        conn.commit()
        conn.close()

    def get_recent_alarms(self, limit=100):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM alarms
            ORDER BY received_at DESC
            LIMIT ?
        ''', (limit,))
        alarms = cursor.fetchall()
        conn.close()
        return alarms

    def get_alarm_stats(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN sent_to_app = 1 THEN 1 ELSE 0 END) as sent,
                COUNT(DISTINCT source) as sources
            FROM alarms
        ''')
        stats = cursor.fetchone()
        conn.close()
        return dict(stats) if stats else {'total': 0, 'sent': 0, 'sources': 0}
