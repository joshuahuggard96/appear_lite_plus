import socket
import threading
import logging
from src.database.db import Database

logger = logging.getLogger(__name__)

class TAPHandler:
    """Handler for TAP (Telocator Alphanumeric Protocol) over IP"""

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
        """Start TAP server"""
        if self.running:
            logger.warning("TAP handler already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        logger.info(f"TAP handler started on {self.host}:{self.port}")

    def stop(self):
        """Stop TAP server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("TAP handler stopped")

    def _run_server(self):
        """Run TCP server to accept TAP connections"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1)

            logger.info(f"TAP server listening on {self.host}:{self.port}")

            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    logger.info(f"TAP client connected from {client_address}")

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
            logger.error(f"Error in TAP server: {e}", exc_info=True)
        finally:
            if self.server_socket:
                self.server_socket.close()

    def _handle_client(self, client_socket, client_address):
        """Handle individual TAP client connection"""
        try:
            buffer = ""

            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break

                buffer += data.decode('utf-8', errors='ignore')

                # Process complete messages (TAP uses ESC EOT as message delimiter)
                while '\x1b\x04' in buffer:  # ESC EOT
                    message, buffer = buffer.split('\x1b\x04', 1)
                    if message.strip():
                        self._process_tap_message(message.strip())
                        # Send ACK
                        client_socket.send(b'\x06')  # ACK

        except Exception as e:
            logger.error(f"Error handling TAP client {client_address}: {e}")
        finally:
            client_socket.close()
            logger.info(f"TAP client {client_address} disconnected")

    def _process_tap_message(self, message):
        """Process TAP protocol message"""
        try:
            # Parse TAP message (simplified - you may need more sophisticated parsing)
            # TAP format typically includes pager ID and message
            alarm_id = self.db.save_alarm(
                source='tap',
                message=message,
                raw_data=message
            )

            logger.info(f"Received alarm from TAP: {message[:100]}")

            # Call callback if registered
            if self.alarm_callback:
                self.alarm_callback({
                    'id': alarm_id,
                    'source': 'tap',
                    'message': message,
                    'raw_data': message
                })

        except Exception as e:
            logger.error(f"Error processing TAP message: {e}", exc_info=True)

    def is_running(self):
        return self.running and self.thread and self.thread.is_alive()
