from locust import task, run_single_user, FastHttpUser
from insert_product import login

class AddToCartUser(FastHttpUser):
    host = "http://localhost:5000"
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    def on_start(self):
        """Runs before any task starts"""
        self.username = "PES1UG22AM149"
        self.password = "Snrk@123"
        cookies = login(self.username, self.password)

        if cookies and "token" in cookies:
            self.token = cookies.get("token")
        else:
            self.token = None
            print("Failed to retrieve token during login")

    @task
    def access_cart(self):
        """Simulates accessing the cart page."""
        if not self.token:
            print("No token available. Skipping request.")
            return

        with self.client.get(
            "/cart",
            headers={
                **self.default_headers,
                "Cookie": f"token={self.token}",
                "Referer": "http://localhost:5000/product/1",
            },
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Request failed with status code {response.status_code}")


if __name__ == "__main__":
    run_single_user(AddToCartUser)