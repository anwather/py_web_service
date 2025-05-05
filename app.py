#!/usr/bin/env python3
"""
Test Web Connectivity Service - A basic connectivity testing web service

This service provides a simple web interface to test connectivity
and display the hostname of the machine it's running on.
"""

import os
import socket
import yaml
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Load configuration
def load_config():
    """Load server configuration from config.yaml file"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')
    try:
        with open(config_path, 'r') as config_file:
            return yaml.safe_load(config_file)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        # Return default configuration
        return {'server': {'port': 5000, 'host': '0.0.0.0'}}

# Define HTML template for the homepage
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Web Connectivity Service</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }
        code {
            background-color: #f0f0f0;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: monospace;
        }
        .endpoint {
            background-color: #e9ecef;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #007bff;
            border-radius: 3px;
        }
        .status {
            color: #28a745;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Test Web Connectivity Service</h1>
        <p class="status">Status: Running</p>
        
        <h2>Description</h2>
        <p>This is a simple web service designed to test connectivity. It provides basic endpoints to verify the service is operational and return information about the host machine.</p>
        
        <h2>Available Endpoints</h2>
        
        <div class="endpoint">
            <h3>Homepage (You are here)</h3>
            <p><code>GET /</code></p>
            <p>Returns this documentation page.</p>
        </div>
        
        <div class="endpoint">
            <h3>Hostname</h3>
            <p><code>GET /hostname</code></p>
            <p>Returns the hostname of the machine this service is running on.</p>
            <p>Example response: <code>{{ '{"hostname": "server-name"}' }}</code></p>
        </div>
        
        <div class="endpoint">
            <h3>Health Check</h3>
            <p><code>GET /health</code></p>
            <p>Returns the health status of the service.</p>
            <p>Example response: <code>{{ '{"status": "healthy"}' }}</code></p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Render the homepage with documentation"""
    return render_template_string(HOME_TEMPLATE)

@app.route('/hostname')
def get_hostname():
    """Return the hostname of the current machine"""
    hostname = socket.gethostname()
    return jsonify({'hostname': hostname})

@app.route('/health')
def health_check():
    """Return the health status of the service"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    config = load_config()
    port = config['server']['port']
    host = config['server']['host']
    
    print(f"Starting web service on {host}:{port}")
    app.run(host=host, port=port)