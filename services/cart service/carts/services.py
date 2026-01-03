import requests


class ProductService:
    # Ensure there is NO slash at the end here to avoid double slashes later
    BASE_URL = "http://product-service:8000/api/products"

    @staticmethod
    def check_product_exists(product_id):
        try:
            url = f"{ProductService.BASE_URL}/{product_id}/"

            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                return response.json()

            print(f"Product Service Error: {response.status_code} - {response.text}")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Connection Failed: {e}")
            return None
