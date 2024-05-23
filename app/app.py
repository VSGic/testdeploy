from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import platform

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/state')

def server_state():
    uname = platform.uname()
    system_info = {
        "System": uname.system,
        "Node_name": uname.node,
        "Release": uname.release,
        "Version": uname.version,
        "Machine": uname.machine,
        "Processor": uname.processor
    }
    return jsonify(message=system_info)

@app.route('/metrics')

def custom_metrics():
    return metrics.export(), 200

@app.route('/health', methods=['GET'])

def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

