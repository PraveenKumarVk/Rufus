import requests

class RufusClient:
    def __init__(self, api_key: str, base_url: str = "http://localhost:8080"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"{self.api_key}"
        }

    def scrape(self, prompt: str):
        """
        Call this method to scrape based on the prompt.
        """
        endpoint = f"{self.base_url}/scrape/"
        data = {"prompt": prompt}

        response = requests.post(endpoint, json=data, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()["content"]
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")
