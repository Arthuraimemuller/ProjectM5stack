from m5stack import *
from m5ui import *
from uiflow import *
import unit
import urequests
import time

# --- CONFIGURATION ---
OPENWEATHER_API_KEY = 'TA_CLE_API'  # ⇦ Remplace par ta clé OpenWeather
CITY = 'Geneva'
COUNTRY_CODE = 'CH'

# --- Initialisation capteur ENVIII ---
env3 = unit.get(unit.ENV3, unit.PORTA)

# --- Interface UI ---
setScreenColor(0xFFFFFF)

# Données simulées à remplir
data_values = [
    ['Temp Ext', '-- °C'],
    ['Temp Int', '-- °C'],
    ['Humidité', '-- %']
]
rotation_index = 0

# --- Création des boutons (zone tactile seulement) ---
button_top = M5Btn(text='', x=90, y=0, w=140, h=140, bg_c=0x87CEEB, text_c=0xFFFFFF, font=FONT_MONT_18)
button_left = M5Btn(text='', x=36, y=132, w=100, h=100, bg_c=0x90EE90, text_c=0xFFFFFF, font=FONT_MONT_18)
button_right = M5Btn(text='', x=187, y=132, w=100, h=100, bg_c=0xFFD700, text_c=0xFFFFFF, font=FONT_MONT_18)

# --- Labels centrés sur les boutons ---
label_top = M5Label('', x=100, y=40, color=0x000000, font=FONT_MONT_18)
label_left = M5Label('', x=50, y=160, color=0x000000, font=FONT_MONT_18)
label_right = M5Label('', x=200, y=160, color=0x000000, font=FONT_MONT_18)

# --- Fonctions ---

def update_labels():
    label_top.set_text("{}\n{}".format(*data_values[rotation_index % 3]))
    label_left.set_text("{}\n{}".format(*data_values[(rotation_index + 1) % 3]))
    label_right.set_text("{}\n{}".format(*data_values[(rotation_index + 2) % 3]))

def rotate_data(button=None):
    global rotation_index
    rotation_index = (rotation_index + 1) % 3
    update_labels()

def read_env_sensor():
    try:
        temp = round(env3.temperature, 1)
        humid = round(env3.humidity, 1)
        return temp, humid
    except:
        return None, None

def get_outdoor_temp():
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}&units=metric'.format(CITY, COUNTRY_CODE, OPENWEATHER_API_KEY)
        r = urequests.get(url)
        data = r.json()
        temp_ext = round(data['main']['temp'], 1)
        r.close()
        return temp_ext
    except:
        return None

# --- Clics pour rotation
button_top.pressed(rotate_data)
button_left.pressed(rotate_data)
button_right.pressed(rotate_data)

# --- Boucle principale ---
while True:
    temp_int, humid = read_env_sensor()
    if temp_int is not None:
        data_values[1][1] = "{} °C".format(temp_int)
        data_values[2][1] = "{} %".format(humid)

    temp_ext = get_outdoor_temp()
    if temp_ext is not None:
        data_values[0][1] = "{} °C".format(temp_ext)

    update_labels()
    wait(10)
