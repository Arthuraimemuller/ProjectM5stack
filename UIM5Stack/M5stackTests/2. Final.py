from m5stack import *
from m5ui import *
from uiflow import *
import unit
import urequests
import time

CITY = "Geneva"
COUNTRY = "CH"
API_KEY = "72dbcc9258a8493ae64994a80e22e830"
BIGQUERY_URL = "http://adresse-de-ton-endpoint/send-to-bigquery"

setScreenColor(0xFFFFFF)

# Ligne 1 : date/heure
label_datetime = M5Label('', x=10, y=5, color=0x000000, font=FONT_MONT_14)

# Ligne 2 : boutons Indoor, Outdoor, CO2 (inchangé)
btn_indoor = M5Btn('', x=10, y=40, w=100, h=100, bg_c=0x90EE90)
btn_outdoor = M5Btn('', x=110, y=40, w=100, h=100, bg_c=0x87CEEB)
btn_co2 = M5Btn('', x=210, y=40, w=100, h=100, bg_c=0xFFD700)

icon_indoor = M5Label('🏠', x=15, y=45, color=0x000000, font=FONT_MONT_18)
icon_outdoor = M5Label('🌤', x=115, y=45, color=0x000000, font=FONT_MONT_18)
icon_co2 = M5Label('💨', x=215, y=45, color=0x000000, font=FONT_MONT_18)

label_indoor = M5Label('-- °C\n-- %', x=20, y=75, color=0x000000, font=FONT_MONT_14)
label_outdoor = M5Label('-- °C', x=125, y=90, color=0x000000, font=FONT_MONT_14)
label_co2 = M5Label('-- ppm', x=225, y=90, color=0x000000, font=FONT_MONT_14)

label_debug = M5Label('', x=5, y=200, color=0xFF0000, font=FONT_MONT_14)  # label pour afficher erreurs

# Ligne 3 à 5 : forecast météo sur 7 colonnes
days_labels = []
temps_labels = []
icons_labels = []
start_x = 10
gap_x = 40

for i in range(7):
    days_labels.append(M5Label('---', x=start_x + i*gap_x, y=140, color=0x000000, font=FONT_MONT_14))
    temps_labels.append(M5Label('-- °C', x=start_x + i*gap_x, y=160, color=0x000000, font=FONT_MONT_14))
    icons_labels.append(M5Label('❓', x=start_x + i*gap_x, y=180, color=0x000000, font=FONT_MONT_18))

env_sensor = unit.get(unit.ENV3, unit.PORTA)
pir_sensor = unit.get(unit.PIR, unit.PORTB)
eco2_sensor = unit.get(unit.TVOC, unit.PORTC)

rtc.settime('ntp', host='pool.ntp.org', tzone=2)

def update_time():
    dt = rtc.datetime()
    label_datetime.set_text(
        "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(dt[0], dt[1], dt[2], dt[4], dt[5], dt[6])
    )

def read_env():
    try:
        return round(env_sensor.temperature, 1), round(env_sensor.humidity, 1)
    except:
        return None, None

def read_outdoor_temp():
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}&units=metric'.format(CITY, COUNTRY, API_KEY)
        res = urequests.get(url)
        temp = round(res.json()['main']['temp'], 1)
        res.close()
        return temp
    except:
        return None

def read_co2():
    try:
        eco2_value = eco2_sensor.eCO2
        tvoc_value = eco2_sensor.TVOC
        return eco2_value, tvoc_value
    except:
        return None, None

def icon_emoji(code):
    if code.startswith("01"): return "☀️"
    if code.startswith("02"): return "🌤️"
    if code.startswith("03"): return "☁️"
    if code.startswith("04"): return "☁️"
    if code.startswith("09"): return "🌧️"
    if code.startswith("10"): return "🌦️"
    if code.startswith("11"): return "⛈️"
    if code.startswith("13"): return "❄️"
    if code.startswith("50"): return "🌫️"
    return "❓"

def read_forecast_week():
    try:
        url = 'http://api.openweathermap.org/data/2.5/forecast?q={},{}&appid={}&units=metric'.format(CITY, COUNTRY, API_KEY)
        res = urequests.get(url)
        data = res.json()
        res.close()

        daily_forecast = {}

        # On cherche la prévision la plus proche de 12h00 pour chaque jour
        for item in data['list']:
            dt_txt = item['dt_txt']  # ex: "2025-05-21 21:00:00"
            date_str, time_str = dt_txt.split(' ')
            target_hour = 12
            hour = int(time_str.split(':')[0])
            diff = abs(hour - target_hour)

            if date_str not in daily_forecast or diff < daily_forecast[date_str]['diff']:
                daily_forecast[date_str] = {
                    'temp': round(item['main']['temp'], 1),
                    'icon': item['weather'][0]['icon'],
                    'diff': diff
                }

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        now_ts = time.time()
        forecast_list = []

        for i in range(7):
            future_ts = now_ts + i * 86400
            future_time = time.localtime(future_ts)
            date_str = "{:04d}-{:02d}-{:02d}".format(future_time[0], future_time[1], future_time[2])
            weekday_num = future_time[6]  # 0 = lundi

            day_label = days[weekday_num]

            if date_str in daily_forecast:
                temp = daily_forecast[date_str]['temp']
                icon = icon_emoji(daily_forecast[date_str]['icon'])
            else:
                temp = '--'
                icon = '❓'

            forecast_list.append((day_label, temp, icon))

        return forecast_list

    except Exception as e:
        print("Erreur forecast:", e)
        return [('--', '--', '❓')] * 7

last_forecast_time = 0
forecast_cache = [('--', '--', '❓')] * 7
last_send_time = 0

def send_to_bigquery(temp, humidity):
    """Send temperature and humidity data to BigQuery via Cloud Run."""
    passwd_hash = "943912667b08be19402bfc3a51a921cfc85f794938d4e23a1b7e37013c453f1e"
    data = {
        "passwd": passwd_hash,
        "values": {
            "indoor_temp": round(temp, 1),
            "indoor_humidity": round(humidity, 1)
        }
    }
    try:
        res = urequests.post(BIGQUERY_URL, json=data)
        res.close()
    except Exception as e:
        label_debug.set_text("Send Error: " + str(e))
        label_debug.set_pos(5, 200)
        label_debug.set_size(310, 30)
        label_debug.set_text_color(0xFF0000)
        label_debug.set_text_font(FONT_MONT_14)
        label_debug.set_long_mode(Label.LONG_WRAP)

def update_display():
    global last_forecast_time, forecast_cache, last_send_time

    temp_in, humidity = read_env()
    if temp_in is not None and humidity is not None:
        label_indoor.set_text("{:.1f}°C\n{:.0f}%".format(temp_in, humidity))
    else:
        label_indoor.set_text("-- °C\n-- %")

    temp_out = read_outdoor_temp()
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

    # Update forecast every 30 minutes
    if time.time() - last_forecast_time > 1800:
        forecast_cache = read_forecast_week()
        last_forecast_time = time.time()

    # Send data to BigQuery every 5 minutes (300 seconds)
    if temp_in is not None and humidity is not None and (time.time() - last_send_time > 300):
        send_to_bigquery(temp_in, humidity)
        last_send_time = time.time()

    for i in range(7):
        day, temp, icon = forecast_cache[i]
        days_labels[i].set_text(day)
        temps_labels[i].set_text(str(temp) + "°C" if temp != '--' else "-- °C")
        icons_labels[i].set_text(icon)

while True:
    update_display()
    wait(1)
