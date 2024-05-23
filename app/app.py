from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

cpu_load_metric = metrics.info('cpu_load', 'CPU load over time')
cpu_quota_metric = metrics.info('cpu_quota', 'CPU quota used percentage')

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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

