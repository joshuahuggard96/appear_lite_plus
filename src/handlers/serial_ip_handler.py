import socket
import threading
import logging
from src.database.db import Database

logger = logging.getLogger(__name__)

class SerialIPHandler:
    """Handler for Serial over IP (TCP serial server)"""

    def __init__(self, host, port, alarm_callback=None):
        self.host = host
        self.port = int(port)
        self.alarm_callback = alarm_callback
        self.server_socket = None
        self.running = False
        self.thread = None
        self.db = Database()
        self.client_threads = []

    def start(self):
        """Start Serial over IP server"""
        if self.running:
            logger.warning("Serial over IP handler already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        logger.info(f"Serial over IP handler started on {self.host}:{self.port}")

    def stop(self):
        """Stop Serial over IP server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Serial over IP handler stopped")

    def _run_server(self):
        """Run TCP server to accept serial connections"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1)

            logger.info(f"Serial over IP server listening on {self.host}:{self.port}")

            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    logger.info(f"Serial over IP client connected from {client_address}")

                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    self.client_threads.append(client_thread)

                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        logger.error(f"Error accepting connection: {e}")

        except Exception as e:
            logger.error(f"Error in Serial over IP server: {e}", exc_info=True)
        finally:
            if self.server_socket:
                self.server_socket.close()

    def _handle_client(self, client_socket, client_address):
        """Handle individual Serial over IP client connection"""
        try:
            buffer = ""

            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break

                # Decode and process line by line
                received = data.decode('utf-8', errors='ignore')
                buffer += received

                # Log received data for debugging
                logger.info(f"Received {len(data)} bytes from {client_address}: {repr(received[:100])}")

                # Process complete lines (newline-delimited)
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    if line:
                        self._process_serial_message(line, client_address)

            # Process any remaining data in buffer when connection closes
            if buffer.strip():
                logger.info(f"Processing remaining buffer from {client_address}: {repr(buffer[:100])}")
                self._process_serial_message(buffer.strip(), client_address)

        except Exception as e:
            logger.error(f"Error handling Serial over IP client {client_address}: {e}")
        finally:
            client_socket.close()
            logger.info(f"Serial over IP client {client_address} disconnected")

    def _process_serial_message(self, message, client_address):
        """Process serial message received over IP"""
        try:
            # Save to database
            alarm_id = self.db.save_alarm(
                source='serial_ip',
                message=message,
                raw_data=f"From {client_address}: {message}"
            )

            logger.info(f"Received alarm from Serial over IP ({client_address}): {message[:100]}")

            # Call callback if registered
            if self.alarm_callback:
                self.alarm_callback({
                    'id': alarm_id,
                    'source': 'serial_ip',
                    'message': message,
                    'raw_data': f"From {client_address}: {message}",
                    'client_address': str(client_address)
                })

        except Exception as e:
            logger.error(f"Error processing Serial over IP message: {e}", exc_info=True)

    def is_running(self):
        return self.running and self.thread and self.thread.is_alive()
