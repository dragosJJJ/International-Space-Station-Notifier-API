import requests, smtplib, time
from datetime import datetime

MY_EMAIL = "draxgamer12@gmail.com"
MY_PASSWORD = "yfpp phio gfgf hmfv"
MY_LAT = 44.318378
MY_LONG = 23.796400

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    if MY_LONG - 5 <= iss_longitude <= MY_LONG + 5 and MY_LAT - 5 <= iss_latitude <= MY_LAT + 5:
        return True
def is_night_time():
    parameters = {
        #latitude and longitude for Craiova, Romania
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted":0
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()

    #In order for you to see the ISS it has to be night-time
    if time_now.hour >= sunset and time_now.hour <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_night_time() and is_iss_overhead():
        connection = smtplib.SMTP("smt.gmail.com")
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs= MY_EMAIL,
            msg="Subject:ISS Notification\n\nThe ISS is above your head! Look up! "
        )
