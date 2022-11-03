from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task
    def summary(self):
        self.client.post("/showSummary", {'email': 'john@simplylift.co'})

    @task
    def purchase(self):
        with self.client.post('/purchasePlaces', {
            "places": 5,
            "club": "Simply Lift",
            "competition": "Spring Festival"
        }, catch_response=True) as response:
            if response.status_code == 403:
                response.success()
