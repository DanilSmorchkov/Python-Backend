from locust import HttpUser, TaskSet, task, User


class BehaviourUser(TaskSet):
    def __init__(self, parent: User):
        super().__init__(parent)
        self.item_id = None
        self.cart_id = None

    def on_start(self):
        response = self.client.post("/cart")
        self.cart_id = response.json()["id"]

    @task(2)
    def post_item(self):
        item = {
            'name': 'name',
            "price": 100
        }
        response = self.client.post("/item", json=item)
        self.item_id = response.json()["id"]

    @task(1)
    def get_item(self):
        self.client.get(f"/item/{self.item_id}")

    @task(1)
    def add_item_to_cart(self):
        self.client.post(f"/cart/{self.cart_id}/add/{self.item_id}")


class WebsiteUser(HttpUser):
    tasks = [BehaviourUser]
    min_wait = 2000
    max_wait = 8000
