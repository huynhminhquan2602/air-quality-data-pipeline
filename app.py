# import requests #Thư viện gửi HTTP request.
# import psycopg2 #Driver để Python kết nối PostgreSQL.
# from datetime import datetime

# #test
# print("fine")

# API_KEY = "58f629ed-93f1-4fae-845c-45cdf5aa68c4"
# BASE_URL = "http://api.airvisual.com/v2/city" #endpoint

# cities = [
#     {"city": "Hanoi", "state": "Ha Noi", "country": "Vietnam"},
#     {"city": "Hue", "state": "Tinh Thua Thien-Hue", "country": "Vietnam"}
# ]

# # Kết nối database
# conn = psycopg2.connect(
#     host="localhost",
#     database="airquality", #DB đc tạo từ docker compose
#     user="admin",
#     password="admin123"
# )

# cur = conn.cursor() #Tạo Cursor = đối tượng để thực thi SQL.

# for c in cities: #lặp qua từng thành phố
#     params = {
#         "city": c["city"],
#         "state": c["state"],
#         "country": c["country"],
#         "key": API_KEY
#     } #Đây là query string gửi lên server. Theo kiểu HTTP: http://api.airvisual.com/v2/city?city=Hanoi&state=Ha+Noi&country=Vietnam&key=...

#     response = requests.get(BASE_URL, params=params)  #Đây là HTTP GET request.

#     print("Status:", response.status_code)
#     print("Response:", response.text)
#     #In ra (200 = OK, 400 = Bad request, 401 = Invalid API key)

#     data = response.json() #Server trả JSON → chuyển thành dict Python.

#     if response.status_code == 200:
#         city_info = data["data"]["city"]
#         state = data["data"]["state"]
#         country = data["data"]["country"]
#         lat = data["data"]["location"]["coordinates"][1]
#         lon = data["data"]["location"]["coordinates"][0]

#         pollution = data["data"]["current"]["pollution"]

#         ts = pollution["ts"]
#         dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
#         aqius = pollution["aqius"]
#         mainus = pollution["mainus"]
#         aqicn = pollution["aqicn"]
#         maincn = pollution["maincn"]

#         # Insert city (tránh duplicate)
#         cur.execute("""
#             INSERT INTO city (cityName, stateName, countryName, latitude, longitude)
#             VALUES (%s, %s, %s, %s, %s)
#             ON CONFLICT DO NOTHING
#             RETURNING cityId
#         """, (city_info, state, country, lat, lon))

#         result = cur.fetchone()

#         if result:
#             city_id = result[0]
#         else:
#             cur.execute("SELECT cityId FROM city WHERE cityName=%s", (city_info,))
#             city_id = cur.fetchone()[0]

#         # Insert pollution
#         cur.execute("""
#             INSERT INTO pollution (cityId, datetime, ts, aqius, mainus, aqicn, maincn)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#             ON CONFLICT DO NOTHING
#         """, (city_id, dt, int(dt.timestamp()), aqius, mainus, aqicn, maincn))

#         conn.commit()
#         print(f"Inserted data for {city_info}")

# cur.close()
# conn.close()


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