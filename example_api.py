from logging import exception
import requests
import json

if __name__ == "__main__":
    with open('instance.json', 'r') as f:
        instance = json.load(f)

    response = requests.post('http://localhost:5000/solve', json=instance)
    if response.status_code == 200:
        print(response.json())
    else:
        exception("An error has occured")
