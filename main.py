import requests
from datetime import datetime
import os

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]

GENDER = "nah you aint gettin my gender"
WEIGHT_KG = "nah you aint gettin my weight"
HEIGHT_CM = "nah you aint gettin my height"
AGE = "nah you aint gettin my age"


endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["SHEET_ENDPOINT"]

exercise_text = input("Tell me, what exercises you did: ")

header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

nutrix_parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(headers=header, url=endpoint, json=nutrix_parameters)
data = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")


for exercise in data["exercises"]:
    sheet_input = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # without auth
    # sheet_response = requests.post(sheet_endpoint, json=sheet_input)
    # print(sheet_response.text)

    bearer_headers = {
        "Authorization": f"Bearer {os.environ["TOKEN"]}"
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_input, headers=bearer_headers)
