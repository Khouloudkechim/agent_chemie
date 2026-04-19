import json
import requests

API_URL = "http://localhost:8000/api"

scenarios = [
    "phosphate_plant",
    "cement_kiln",
    "chemical_complex"
]

def seed_and_test():
    for scenario in scenarios:
        print(f"\n--- Testing Scenario: {scenario} ---")
        try:
            response = requests.post(f"{API_URL}/simulate", json={"scenario_id": scenario})
            if response.status_code == 200:
                data = response.json()
                print(f"Decision: {data.get('decision')}")
                print(f"Confidence: {data.get('confidence')}")
                print(f"Safety: {data.get('safety_status')}")
                print("Reasoning:")
                print(data.get('reasoning'))
            else:
                print(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Failed to connect to backend: {e}")

if __name__ == "__main__":
    seed_and_test()
