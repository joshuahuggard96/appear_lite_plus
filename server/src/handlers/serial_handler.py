import serial
import threading
import time
import logging
from src.database.db import Database

logger = logging.getLogger(__name__)

class SerialHandler:
    def __init__(self, port, baud_rate, alarm_callback=None):
        self.port = port
        self.baud_rate = int(baud_rate)
        self.alarm_callback = alarm_callback
        self.serial_conn = None
        self.running = False
        self.thread = None
        self.db = Database()

    def start(self):
        """Start serial port monitoring"""
        if self.running:
            logger.warning("Serial handler already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._monitor_serial, daemon=True)
        self.thread.start()
        logger.info(f"Serial handler started on {self.port} at {self.baud_rate} baud")

    def stop(self):
        """Stop serial port monitoring"""
        self.running = False
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Serial handler stopped")

    def _monitor_serial(self):
        """Monitor serial port for incoming data"""
        while self.running:
            try:
                if not self.serial_conn or not self.serial_conn.is_open:
                    self.serial_conn = serial.Serial(
                        port=self.port,
                        baudrate=self.baud_rate,
                        timeout=1
                    )
                    logger.info(f"Connected to serial port {self.port}")

                if self.serial_conn.in_waiting > 0:
                    raw_data = self.serial_conn.readline().decode('utf-8', errors='ignore').strip()
                    if raw_data:
                        self._process_alarm(raw_data)

            except serial.SerialException as e:
                logger.error(f"Serial port error: {e}")
                if self.serial_conn and self.serial_conn.is_open:
                    self.serial_conn.close()
                time.sleep(5)  # Wait before retry

            except Exception as e:
                logger.error(f"Error in serial handler: {e}", exc_info=True)
                time.sleep(1)

    def _process_alarm(self, raw_data):
        """Process received alarm data"""
        try:
            # Save to database
            alarm_id = self.db.save_alarm(
                source='serial',
                message=raw_data,
                raw_data=raw_data
            )

            logger.info(f"Received alarm from serial: {raw_data[:100]}")

            # Call callback if registered (for real-time notification)
            if self.alarm_callback:
                self.alarm_callback({
                    'id': alarm_id,
                    'source': 'serial',
                    'message': raw_data,
                    'raw_data': raw_data
                })

        except Exception as e:
            logger.error(f"Error processing alarm: {e}", exc_info=True)

    def is_running(self):
        return self.running and self.thread and self.thread.is_alive()
