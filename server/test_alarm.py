#!/usr/bin/env python3
"""
Test script to send alarms to the Appear Lite Plus system
"""

import socket
import time
import sys

def send_serial_ip_alarm(host='localhost', port=5001, message=None):
    """Send an alarm via Serial over IP"""
    if not message:
        message = f"TEST ALARM: Fire detected in Building A at {time.strftime('%H:%M:%S')}"

    try:
        # Connect to Serial over IP server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        # Send message (newline-delimited)
        sock.send(f"{message}\n".encode('utf-8'))

        print(f"[OK] Sent alarm to Serial over IP ({host}:{port})")
        print(f"  Message: {message}")

        sock.close()
        return True
    except Exception as e:
        print(f"[ERROR] Error sending alarm: {e}")
        return False

def send_tap_alarm(host='localhost', port=18001, message=None):
    """Send an alarm via TAP over IP"""
    if not message:
        message = f"TEST ALARM: Security breach at Gate 2 at {time.strftime('%H:%M:%S')}"

    try:
        # Connect to TAP server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        # Send TAP-formatted message (ESC EOT delimiter)
        tap_message = f"{message}\x1b\x04"  # ESC EOT
        sock.send(tap_message.encode('utf-8'))

        # Wait for ACK
        response = sock.recv(1)
        if response == b'\x06':
            print(f"[OK] Sent alarm to TAP ({host}:{port}) - ACK received")
        else:
            print(f"[OK] Sent alarm to TAP ({host}:{port}) - No ACK")

        print(f"  Message: {message}")

        sock.close()
        return True
    except Exception as e:
        print(f"[ERROR] Error sending TAP alarm: {e}")
        return False

def main():
    print("=" * 60)
    print("Appear Lite Plus - Alarm Test Script")
    print("=" * 60)

    if len(sys.argv) > 1:
        custom_message = ' '.join(sys.argv[1:])
        print(f"\nUsing custom message: {custom_message}\n")
    else:
        custom_message = None
        print("\nSending test alarms...\n")

    # Send to Serial over IP
    print("1. Testing Serial over IP:")
    send_serial_ip_alarm(message=custom_message)

    print()

    # Send to TAP over IP
    print("2. Testing TAP over IP:")
    send_tap_alarm(message=custom_message)

    print("\n" + "=" * 60)
    print("Test complete! Check the web interface at http://localhost:5000")
    print("Login: admin/admin")
    print("=" * 60)

if __name__ == '__main__':
    main()
