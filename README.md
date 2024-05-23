# testdeploy

Intro
Simple python application with Flask framework managed with docker compose, docker swarm, and CI/CD Github actions(tested with act tool on ARM MacOS)

### Requirements ###
  docker
  docker-compose
  docker swarm (initiated - $ docker swarm init)
  act (Github actions tool) 

### How-to install ###
$ act -W .github/workflows/workflows.yml
/// Starts pipeline with docker images building, testing job and services deployments in Docker Swarm environment

$ act -W .github/workflows/locust_start.yml
/// Starts additional containers with locust for load and scaling tests after install

$ act -W .github/workflows/stop.yml
/// Deletes all containers

1. App (Name: testdeploy_app)
Simple Flask app starts with 3 endpoints at address: http://localhost:5000
- http://localhost:5000/state
- http://localhost:5000/metrics
- http://localhost:5000/health

2. Monitoring environment(Names: testdeploy_prometheus, testdeploy_alertmanager, testdeploy_cadvisor)
Prometheus interface is accessible:
- http://localhost:9090/

Metrics taken in consideration:
rate(container_cpu_usage_seconds_total{container_label_com_docker_swarm_service_name="testdeploy_app"}[1m]) * 1000 - 0.1 Limited cpu quota for testdeploy_app usage statistics inside 1m(for scaling purposes)  

increase(flask_http_request_duration_seconds_sum[1m]) / increase(flask_http_request_duration_seconds_count[1m]) - requests medium time duration(for alerting purposes)

sum(flask_http_request_total{status!="200"}) - no 200 requests returned by app 

Alerts:
increase(flask_http_request_duration_seconds_sum[1m]) / increase(flask_http_request_duration_seconds_count[1m]) > 0.00015 - If medium request duration grows more that 0.00015s within 1m

3. Scaling app(Names: testdeploy_autoscaler, testdeploy_app_monitor)
///testdeploy_autoscaler
- http://localhost:5033/scale/up - scale up to the 5 replicas
- http://localhost:5033/scale/down - scale down to at least 1 replics
///testdeploy_app_monitor - requests from prometheus stats about medium cpu usage from the app container quote
- if app container uses agregated cpu quota more that 80% within 1 minute, monitor send callback to scale up app replicas
- if app container uses agregated cpu quota less that 50% within 1 minute, monitor send callback to scale down app replicas

4. Load testing(Name: testdeploy_tester)
In CI/CD added job with load testing, locust library is used
Test case simulates 500 users uses service within 3 minutes

In case of successful execution you will get report in Github pipeline with requests statistics, while testing app should be scaled.

5. Locust setup(Name: testdeploy_master, testdeploy_worker)
- http://localhost:8089/
Allows additional test scenarios for autoscaling testing.

Additional test scenarios:
5.1. Set 1000 users for 5 minutes on address: http://app:5000, check load with command: "docker stats" and replication with "docker service ls"  - at the end of test there should be 5 replicas
5.2. Set 200 users for 5 minutes on address: http://app:5000, check load with command: "docker stats" and replication with "docker service ls"  - at the end of test there should be 2 replicas
5.3 Turn off load from app, check load with command: "docker stats" and replication with "docker service ls"  - at the end of test there should be 1 replicas

Step for iteration is about 1 minute

6. Containerization:
./docker-compose.yml - app, prometheus, cadvisor, alermanager, autoscaler, app_monitor(main services)
./test/docker-compose.yml - tester(testing scenario)
./locust/docker-compose.yml - locust with UI(testing final deployment) 
