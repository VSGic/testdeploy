from locust import HttpUser, TaskSet, task, between
from locust.stats import stats_printer, stats_history

class UserBehavior(TaskSet):
    @task(1)
    def info(self):
        self.client.get("/state")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
