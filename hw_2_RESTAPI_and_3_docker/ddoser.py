from concurrent.futures import ThreadPoolExecutor, as_completed

from faker import Faker
import requests

faker = Faker()


def create_items():
    for _ in range(500):
        item = faker.word()
        price = faker.pyfloat(min_value=-5., max_value=50.0)
        response = requests.post(url="http://localhost:8000/item/", json={"name": item, "price": price})
        print(response.status_code)


def get_item():
    for _ in range(500):
        id = faker.pyint(min_value=-10, max_value=499)
        response = requests.get(url="http://localhost:8000/item/" + str(id))
        print(response.status_code)


with ThreadPoolExecutor() as executor:
    futures = {}

    for i in range(2000):
        futures[executor.submit(create_items)] = f"create_items_{i}"

    for i in range(2000):
        futures[executor.submit(get_item)] = f"get_items_{i}"

    for future in as_completed(futures):
        print(f"completed {futures[future]}")
