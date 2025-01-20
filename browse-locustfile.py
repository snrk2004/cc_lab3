from locust import task, run_single_user, FastHttpUser


class BrowseUser(FastHttpUser):
    # Base host for all requests
    host = "http://localhost:5000"

    # Default headers for requests
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    }

    @task
    def browse(self):
        """
        Simulates browsing the '/browse' page.
        Optimizations:
        - Reused session for efficiency.
        - Streamlined headers.
        - Reduced response logging overhead.
        """
        with self.client.get(
            "/browse",
            headers={
                **self.default_headers,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Upgrade-Insecure-Requests": "1",
            },
            name="Browse Page",
            stream=False,  # Prevents streaming to save resources unless explicitly needed
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code {response.status_code}")

    def on_start(self):
        """
        Runs before tasks start.
        Useful for initializing any necessary session setup or state.
        """
        print("Starting user session for browsing tasks...")


if __name__ == "__main__":
    run_single_user(BrowseUser)