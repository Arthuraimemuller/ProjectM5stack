from m5stack import *
from m5ui import *
from uiflow import *
import unit
import urequests
import time

CITY = "Geneva"
COUNTRY = "CH"
API_KEY = "72dbcc9258a8493ae64994a80e22e830"
BIGQUERY_URL = "https://docker-flask-backend-project-688745668065.europe-west6.run.app/send-to-bigquery"

setScreenColor(0xFFFFFF)

# Ligne 1 : date/heure
label_datetime = M5Label('', x=50, y=5, color=0x000000, font=FONT_MONT_14, parent=None)

btn_width = 100
btn_height = 140
btn_y = 60
btn_spacing = 5
icon_y = btn_y - 35

# Boutons Indoor, Outdoor, CO2 (avec M5Btn)
btn_indoor = M5Btn("", x=5, y=btn_y, w=btn_width, h=btn_height, bg_c=0x90EE90)
btn_indoor.set_btn_text_color(0xFFFFFF)
btn_indoor.set_btn_text_font(FONT_MONT_18)
img_indoor = M5Img("res/home.png", x=55, y=icon_y)

btn_outdoor = M5Btn("", x=5 + btn_width + btn_spacing, y=btn_y, w=btn_width, h=btn_height, bg_c=0x87CEEB)
btn_outdoor.set_btn_text_color(0xFFFFFF)
btn_outdoor.set_btn_text_font(FONT_MONT_18)
img_outdoor = M5Img("res/outdoor.png", x=5 + btn_width + btn_spacing + 55, y=icon_y)

btn_co2 = M5Btn("", x=220, y=btn_y, w=btn_width, h=btn_height, bg_c=0xFFD700)
btn_co2.set_btn_text_color(0x000000)
btn_co2.set_btn_text_font(FONT_MONT_18)
img_co2 = M5Img("res/co2.png", x=220 + 55, y=icon_y)

label_debug = M5Label('', x=5, y=200, color=0x000000, font=FONT_MONT_14, parent=None)  # label pour afficher erreurs
label_hello = M5Label('', x=220, y=10, color=0xFF0000, font=FONT_MONT_18, parent=None)

# Ligne 3 à 5 : forecast météo sur 7 colonnes (avec images au lieu d'icônes textes)
days_labels = []
temps_labels = []
icons_imgs = []  # liste d'images

start_x = 10
gap_x = 40
icon_y_forecast = 180

for i in range(7):
    days_labels.append(M5Label('---', x=start_x + i * gap_x, y=140, color=0x000000, font=FONT_MONT_14))
    temps_labels.append(M5Label('-- °C', x=start_x + i * gap_x, y=160, color=0x000000, font=FONT_MONT_14))
    icons_imgs.append(M5Img("res/unknown.png", x=start_x + i * gap_x - 10, y=icon_y_forecast, parent=None))  # placeholder image

# Fonction pour mapper icône météo openweathermap en nom fichier image
def icon_to_img_file(icon_code):
    if icon_code.startswith("01"): return "res/sunny.png"
    if icon_code.startswith("02"): return "res/partly_cloudy.png"
    if icon_code.startswith("03"): return "res/cloudy.png"
    if icon_code.startswith("04"): return "res/cloudy.png"
    if icon_code.startswith("09"): return "res/shower_rain.png"
    if icon_code.startswith("10"): return "res/rain.png"
    if icon_code.startswith("11"): return "res/thunderstorm.png"
    if icon_code.startswith("13"): return "res/snow.png"
    if icon_code.startswith("50"): return "res/mist.png"
    return "res/unknown.png"


# ... Toutes tes fonctions read_env, read_outdoor_temp, read_co2, etc. restent inchangées ...


def update_display():
    if pir_sensor.state == 1:
        label_hello.set_text("Hello")
    else:
        label_hello.set_text("")

    global last_forecast_time, forecast_cache, last_send_time

    temp_in, humidity = read_env()
    if temp_in is not None and humidity is not None:
        btn_indoor.set_btn_text("{:.1f}°C\n{:.0f}%".format(temp_in, humidity))
    else:
        btn_indoor.set_btn_text("-- °C\n-- %")

    temp_out = read_outdoor_temp()
    if temp_out is not None:
        btn_outdoor.set_btn_text("{:.1f}°C".format(temp_out))
    else:
        btn_outdoor.set_btn_text("-- °C")

    eco2, tvoc = read_co2()
    if eco2 is not None:
        btn_co2.set_btn_text("{} ppm".format(eco2))
    else:
        btn_co2.set_btn_text("-- ppm")

    update_time()

    # Update forecast every 30 minutes
    if time.time() - last_forecast_time > 1800:
        forecast_cache = read_forecast_week()
        last_forecast_time = time.time()

    # Send data to BigQuery every 5 minutes (300 seconds)
    if temp_in is not None and humidity is not None and (time.time() - last_send_time > 300):
        send_to_bigquery(label_debug, temp_in, humidity)
        last_send_time = time.time()

    for i in range(7):
        day, temp, icon_code = forecast_cache[i]
        days_labels[i].set_text(day)
        temps_labels[i].set_text(str(temp) + "°C" if temp != '--' else "-- °C")
        # Change image for icon météo
        icons_imgs[i].set_src(icon_to_img_file(icon_code))


while True:
    update_display()
    wait(1)
    label_debug.set_text("")
