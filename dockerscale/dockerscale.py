from flask import Flask, request, jsonify
import docker

app = Flask(__name__)
client = docker.from_env()

# Configuration
SERVICE_NAME = 'testdeploy_app'

@app.route('/scale/up', methods=['POST'])
def scale_up():
    try:
        service = client.services.get(SERVICE_NAME)
        current_replicas = service.attrs['Spec']['Mode']['Replicated']['Replicas']
        if current_replicas < 5:
            new_replicas = current_replicas + 1
            service.scale(new_replicas)
        return jsonify({'status': 'success', 'replicas': new_replicas}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/scale/down', methods=['POST'])
def scale_down():
    try:
        service = client.services.get(SERVICE_NAME)
        current_replicas = service.attrs['Spec']['Mode']['Replicated']['Replicas']
        new_replicas = max(current_replicas - 1, 1)
        service.scale(new_replicas)
        return jsonify({'status': 'success', 'replicas': new_replicas}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/scale/set', methods=['POST'])
def scale_set():
    try:
        data = request.get_json()
        replicas = data.get('replicas')
        if replicas is None or not isinstance(replicas, int) or replicas < 1:
            return jsonify({'status': 'error', 'message': 'Invalid number of replicas'}), 400
        service = client.services.get(SERVICE_NAME)
        service.scale(replicas)
        return jsonify({'status': 'success', 'replicas': replicas}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/scale/get', methods=['GET'])
def scale_get():
    try:
        service = client.services.get(SERVICE_NAME)
        current_replicas = service.attrs['Spec']['Mode']['Replicated']['Replicas']
        return jsonify({'status': 'success', 'replicas': current_replicas}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

