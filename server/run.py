#!/usr/bin/env python3
"""
Appear Lite Plus - Raspberry Pi Alarm Messaging System
Main entry point for the application
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import app, socketio, logger, start_handlers

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("Starting Appear Lite Plus")
    logger.info("=" * 50)

    # Start alarm handlers
    start_handlers()

    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))

    logger.info(f"Web interface available at http://{host}:{port}")
    logger.info("Default login: admin/admin")
    logger.info("=" * 50)

    # Run the application
    socketio.run(app, host=host, port=port, debug=True, allow_unsafe_werkzeug=True)
