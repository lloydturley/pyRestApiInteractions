import datetime
import time
import os
import requests

NUTRITIONIXAPPID = os.environ['NUTRITIONIXAPP']
NUTRITIONIXAPIKEY = os.environ['NUTRITIONIXAPIKEY']
URLBASE = 'https://trackapi.nutritionix.com'
SHEETYURL = os.environ['SHEETYURL']
SHEETYAUTH = os.environ['SHEETYAUTH']


NATLANGEXERCISEENDPOINT = '/v2/natural/exercise'

AUTHHEADERS = {
    "x-app-id": f"{NUTRITIONIXAPPID}",
    "x-app-key": f"{NUTRITIONIXAPIKEY}"
}

exercise_answer = input("What exercise did you do?")

body = {
    "query": f"{exercise_answer}"
}

print(AUTHHEADERS)

response = requests.post(url=f"{URLBASE}{NATLANGEXERCISEENDPOINT}", json=body, headers=AUTHHEADERS)
response.raise_for_status()
print(response.text)

received_exercises = response.json()["exercises"]

print(received_exercises)

AUTHHEADERS2 = {
    "Authorization": f"{SHEETYAUTH}"
}

for exercise in received_exercises:
    record = {
        "workout": {
            "date": datetime.date.today().strftime('%d/%m/%Y'), # "date": "23/07/2024",
            "time": time.strftime("%H:%M:%S"),  # "time": "16:00:00",
            "exercise": exercise["name"],
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    print(AUTHHEADERS2)
    sheetyResponse = requests.post(url=f"{SHEETYURL}", json=record, headers=AUTHHEADERS2)
    sheetyResponse.raise_for_status()
    print(sheetyResponse.text)

