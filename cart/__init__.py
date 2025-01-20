import json
from cart import dao
from products import Product, get_product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @classmethod
    def load(cls, data):
        contents = json.loads(data['contents'])  # Safely parse the contents
        return cls(data['id'], data['username'], contents, data['cost'])


def get_cart(username: str) -> list[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []
    
    items = json.loads(cart_details['contents'])  # Safely load contents as list
    products_in_cart = [get_product(product_id) for product_id in items]
    return products_in_cart


def add_to_cart(username: str, product_id: int):
    # Fetch the cart details
    cart_details = dao.get_cart(username)
    if cart_details:
        contents = json.loads(cart_details['contents'])
        contents.append(product_id)
        dao.update_cart(username, contents)
    else:
        # Create a new cart for the user
        dao.create_cart(username, [product_id])


def remove_from_cart(username: str, product_id: int):
    cart_details = dao.get_cart(username)
    if cart_details:
        contents = json.loads(cart_details['contents'])
        if product_id in contents:
            contents.remove(product_id)
            dao.update_cart(username, contents)


def delete_cart(username: str):
    dao.delete_cart(username)

