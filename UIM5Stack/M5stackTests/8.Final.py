from m5stack import *
from m5ui import *
from uiflow import *
import unit
import urequests
import time

# Config backend & OpenWeather via backend
BIGQUERY_URL = "https://docker-flask-backend-project-688745668065.europe-west6.run.app/send-to-bigquery"
BACKEND_WEATHER_CURRENT = "https://docker-flask-backend-project-688745668065.europe-west6.run.app/weather/current"
BACKEND_WEATHER_FORECAST = "https://docker-flask-backend-project-688745668065.europe-west6.run.app/weather/forecast"

# UI Setup
setScreenColor(0xFFFFFF)

# Ligne 1 : date/heure
label_datetime = M5Label('', x=50, y=5, color=0x000000, font=FONT_MONT_14)

# Ligne 2 : boutons Indoor, Outdoor, CO2
btn_indoor = M5Btn('', x=10, y=40, w=100, h=100, bg_c=0x90EE90, text_c=0x000000)
btn_outdoor = M5Btn('', x=110, y=40, w=100, h=100, bg_c=0x87CEEB, text_c=0x000000)
btn_co2 = M5Btn('', x=210, y=40, w=100, h=100, bg_c=0xFFD700, text_c=0x000000)

icon_indoor = M5Label('🏠', x=15, y=45, color=0x000000, font=FONT_MONT_18)
icon_outdoor = M5Label('🌤', x=115, y=45, color=0x000000, font=FONT_MONT_18)
icon_co2 = M5Label('💨', x=215, y=45, color=0x000000, font=FONT_MONT_18)

label_indoor = M5Label('-- °C\n-- %', x=20, y=75, color=0x000000, font=FONT_MONT_14)
label_outdoor = M5Label('-- °C', x=125, y=90, color=0x000000, font=FONT_MONT_14)
label_co2 = M5Label('-- ppm', x=225, y=90, color=0x000000, font=FONT_MONT_14)

label_debug = M5Label('', x=5, y=200, color=0x000000, font=FONT_MONT_14)
label_hello = M5Label('', x=220, y=10, color=0xFF0000, font=FONT_MONT_18)


img1 = M5Img("res/home_imresizer.png", x=40, y=45)

img2 = M5Img("res/outdoor_imresizer.png", x=140, y=45)
img2 = M5Img("res/co2_imresizer.png", x=245, y=45)
img = M5Img("res/weatherIcon_imresizer.png", x=0, y=0)


# Ligne 3 à 9 : forecast météo sur 7 jours
days_labels = []
temps_labels = []
start_x = 10
gap_x = 40
for i in range(7):
    days_labels.append(M5Label('---', x=start_x + i * gap_x, y=140, color=0x000000, font=FONT_MONT_14))
    temps_labels.append(M5Label('-- °C', x=start_x + i * gap_x, y=160, color=0x000000, font=FONT_MONT_14))

# Capteurs
env_sensor = unit.get(unit.ENV3, unit.PORTA)
pir_sensor = unit.get(unit.PIR, unit.PORTB)
eco2_sensor = unit.get(unit.TVOC, unit.PORTC)

rtc.settime('ntp', host='pool.ntp.org', tzone=2)


def update_time():
    dt = rtc.datetime()
    label_datetime.set_text("{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(dt[0], dt[1], dt[2], dt[4], dt[5], dt[6]))


def read_env():
    try:
        return round(env_sensor.temperature, 1), round(env_sensor.humidity, 1)
    except Exception as e:
        label_debug.set_text("Env sensor error: " + str(e))
        return None, None


def read_co2():
    try:
        eco2_value = eco2_sensor.eCO2
        tvoc_value = eco2_sensor.TVOC
        return eco2_value, tvoc_value
    except Exception as e:
        label_debug.set_text("CO2 sensor error: " + str(e))
        return None, None


def get_outdoor_weather():
    """Récupère la météo extérieure depuis ton backend Flask."""
    try:
        res = urequests.get(BACKEND_WEATHER_CURRENT)
        data = res.json()
        res.close()
        temp = data.get("temperature")
        humidity = data.get("humidity")  # si tu veux afficher aussi
        return temp, humidity
    except Exception as e:
        label_debug.set_text("Outdoor weather error: " + str(e))
        return None, None


def get_forecast_week():
    """Récupère les prévisions météo 7 jours depuis ton backend Flask."""
    try:
        res = urequests.get(BACKEND_WEATHER_FORECAST)
        forecast = res.json()
        res.close()

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        forecast_list = []

        for i in range(7):
            if i >= len(forecast):
                forecast_list.append(('---', '--'))
                continue

            day_data = forecast[i]
            date_str = day_data.get("date", "1970-01-01")
            temp = day_data.get("temp", '--')

            try:
                y, m, d = map(int, date_str.split('-'))
                tm = time.localtime(time.mktime((y, m, d, 12, 0, 0, 0, 0)))
                weekday_num = tm[6]  # 0 = Monday
                day_label = days[weekday_num]
            except Exception:
                day_label = '---'

            forecast_list.append((day_label, temp))

        return forecast_list
    except Exception as e:
        label_debug.set_text("Forecast error: " + str(e))
        return [('--', '--')] * 7


def send_to_bigquery(temp, humidity):
    """Envoie les données vers BigQuery via backend."""
    passwd_hash = "943912667b08be19402bfc3a51a921cfc85f794938d4e23a1b7e37013c453f1e"
    dt = rtc.datetime()
    date_str = "{:04d}-{:02d}-{:02d}".format(dt[0], dt[1], dt[2])
    time_str = "{:02d}:{:02d}:{:02d}".format(dt[4], dt[5], dt[6])
    data = {
        "passwd": passwd_hash,
        "values": {
            "date": date_str,
            "time": time_str,
            "indoor_temp": round(temp, 1),
            "indoor_humidity": round(humidity, 1)
        }
    }
    try:
        res = urequests.post(BIGQUERY_URL, json=data)
        res.close()
        label_debug.set_text("Data sent ✔")
    except Exception as e:
        label_debug.set_text("Send Error: " + str(e))


last_forecast_time = 0
forecast_cache = [('--', '--')] * 7
last_send_time = 0


def update_display():
    global last_forecast_time, forecast_cache, last_send_time

    # Affiche Hello si détection mouvement
    if pir_sensor.state == 1:
        label_hello.set_text("Hello")
    else:
        label_hello.set_text("")

    temp_in, humidity = read_env()
    if temp_in is not None and humidity is not None:
        label_indoor.set_text("{:.1f}°C\n{:.0f}%".format(temp_in, humidity))
    else:
        label_indoor.set_text("-- °C\n-- %")

    temp_out, outdoor_humidity = get_outdoor_weather()
    if temp_out is not None:
        label_outdoor.set_text("{:.1f}°C".format(temp_out))
    else:
        label_outdoor.set_text("-- °C")

    eco2, tvoc = read_co2()
    if eco2 is not None:
        label_co2.set_text("{} ppm".format(eco2))
    else:
        label_co2.set_text("-- ppm")

    update_time()

    # Envoi BigQuery toutes les 60s si données valides
    if temp_in is not None and humidity is not None and (time.time() - last_send_time > 60):
        send_to_bigquery(temp_in, humidity)
        last_send_time = time.time()

    # Mise à jour prévisions toutes les 30min
    if time.time() - last_forecast_time > 3:  # 1800s = 30 minutes
        forecast_cache = get_forecast_week()
        last_forecast_time = time.time()

    # Affiche prévisions avec sécurité index
    for i in range(7):
        if i >= len(forecast_cache):
            continue
        day, temp = forecast_cache[i]
        days_labels[i].set_text(day)
        if isinstance(temp, (int, float)):
            temps_labels[i].set_text("{:.1f}°C".format(temp))
        else:
            temps_labels[i].set_text("-- °C")


while True:
    update_display()
    wait(1)
