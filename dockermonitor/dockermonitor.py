import prometheus_api_client
import requests
import time

prometheus_url = "http://prometheus:9090"

service_name = "app"

cpu_load_threshold_up = 80
cpu_load_threshold_down = 20

prometheus_client = prometheus_api_client.prometheus_connect.PrometheusConnect(prometheus_url)
time.sleep(180)

def get_cpu_usage():
    query = 'rate(container_cpu_usage_seconds_total{container_label_com_docker_swarm_service_name="testdeploy_app"}[1m]) * 1000'
    result = prometheus_client.custom_query(query)
    print(result)
    cpu_usage_list = result[0]['value'][1]
    cpu_usage = float(cpu_usage_list)
    return cpu_usage

def send_post_request(url, data):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("POST request successful")
    else:
        print("POST request failed")

def main():
    while True:
        cpu_usage = get_cpu_usage()
        print(cpu_usage)
        if int(cpu_usage) > cpu_load_threshold_up:
            send_post_request("http://autoscaler:5000/scale/up", {"cpu_usage": cpu_usage})
        elif int(cpu_usage) < cpu_load_threshold_down:
            send_post_request("http://autoscaler:5000/scale/down", {"cpu_usage": cpu_usage})
        time.sleep(60)


if __name__ == "__main__":
    main()

