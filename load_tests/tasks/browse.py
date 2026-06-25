import random
from locust import task
from base import BaseUser

class ShopUser(BaseUser):

    @task(10)
    def browse_shop(self):
        with self.client.get("/products", name="GET",catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error: {response.status_code}")
    @task(6)
    def veiw_product(self):
        random_id =random.randint(1,100)
        with self.client.get(f"/products/{random_id}", name="GET/products/{id}",catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error: {response.status_code}")

    @task(1)
    def create_order(self):
        order = {
            "user_id": random.randint(1, 20),
            "product_id": random.randint(1, 100),
            "quantity": random.randint(1, 3),
        }

        with self.client.post("/orders",json=order, name="POST",catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Error: {response.status_code}")