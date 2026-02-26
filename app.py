import os
import requests
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables từ file .env
load_dotenv()

API_KEY = os.getenv("IQAIR_API_KEY")
BASE_URL = "http://api.airvisual.com/v2/city"

cities = [
    {"city": "Hanoi", "state": "Ha Noi", "country": "Vietnam"},
    {"city": "Hue", "state": "Tinh Thua Thien-Hue", "country": "Vietnam"}
]

# Kết nối database bằng biến môi trường
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

for c in cities:
    params = {
        "city": c["city"],
        "state": c["state"],
        "country": c["country"],
        "key": API_KEY
    }

    response = requests.get(BASE_URL, params=params, timeout=10)

    print("Status:", response.status_code)

    if response.status_code != 200:
        print("Error:", response.text)
        continue

    data = response.json()

    city_info = data["data"]["city"]
    state = data["data"]["state"]
    country = data["data"]["country"]
    lat = data["data"]["location"]["coordinates"][1]
    lon = data["data"]["location"]["coordinates"][0]

    pollution = data["data"]["current"]["pollution"]

    ts = pollution["ts"]
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    aqius = pollution["aqius"]
    mainus = pollution["mainus"]
    aqicn = pollution["aqicn"]
    maincn = pollution["maincn"]

    # Insert city
    cur.execute("""
        INSERT INTO city (cityName, stateName, countryName, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        RETURNING cityId
    """, (city_info, state, country, lat, lon))

    result = cur.fetchone()

    if result:
        city_id = result[0]
    else:
        cur.execute("SELECT cityId FROM city WHERE cityName=%s", (city_info,))
        city_id = cur.fetchone()[0]

    # Insert pollution
    cur.execute("""
        INSERT INTO pollution (cityId, datetime, ts, aqius, mainus, aqicn, maincn)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (city_id, dt, int(dt.timestamp()), aqius, mainus, aqicn, maincn))

    conn.commit()
    print(f"Inserted data for {city_info}")

cur.close()
conn.close()