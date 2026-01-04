import requests


class CartService:
    BASE_URL = "http://cart-service:8000/api/cart"

    @staticmethod
    def get_cart(user_id):
        try:
            response = requests.get(
                f"{CartService.BASE_URL}/?user_id={user_id}", timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            return None

    @staticmethod
    def clear_cart(user_id):
        try:
            requests.post(
                f"{CartService.BASE_URL}/clear/", json={"user_id": user_id}, timeout=5
            )
        except requests.exceptions.RequestException:
            pass


class ProductService:
    BASE_URL = "http://product-service:8000/api/products"

    @staticmethod
    def get_product(product_id):
        try:
            response = requests.get(
                f"{ProductService.BASE_URL}/{product_id}", timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
