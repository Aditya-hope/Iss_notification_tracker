
import requests
from datetime import datetime
import smtplib
import time
my_email="aditya1441behera@gmail.com"
app_password="xtludskksznexluq"
My_lat=20.951666
My_long=-85.098526
def is_iss_overhead():

    response=requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data=response.json()
    iss_longitude=float(data["iss_position"]["longitude"])
    iss_latitude=float(data["iss_position"]["latitude"])
    # your positon is within +5 or -5 degrees of the iss position
    if My_lat-5<=iss_latitude<=My_lat+5 and My_long-5<= iss_longitude <=My_long+5:
            return True
    else:
        return False
def is_night():
    parameters={
        "lat":My_lat,
        "lng":My_long,
        "formatted":0
    }

    response=requests.get(url="https://api.sunrise-sunset.org/json",params=parameters)
    response.raise_for_status()
    data=response.json()
    sunrise=int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset=int(data["results"]["sunset"].split("T")[1].split(":")[0])


    time_now=datetime.now().hour
    if time_now>= sunset and time_now<= sunrise:
        return True
    else:
        return False
while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection=smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(my_email,app_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject:Look up \n\n the iss is overhead in the sky ."
        )


