import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
print(f"Testing key: {api_key[:10]}...")

url = "https://api.tavily.com/search"
payload = {
    "api_key": api_key,
    "query": "test",
    "max_results": 1
}

response = requests.post(url, json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
