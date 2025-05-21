from m5stack import *
from m5ui import *
from uiflow import *
import unit
import urequests
import time

# === CONFIG ===
OPENWEATHER_API_KEY = 'TA_CLE_API'
CITY = 'Geneva'
COUNTRY_CODE = 'CH'

# === CAPTEUR ENVIII ===
env3 = unit.get(unit.ENV3, unit.PORTA)

# === ÉCRAN ===
setScreenColor(0xFFFFFF)

# === DONNÉES INITIALES ===
data_values = [
    ['Temp Ext', '-- °C'],
    ['Temp Int', '-- °C'],
    ['Humidité', '-- %']
]
rotation_index = 0

# === BOUTONS ===
# Grand bouton (haut)
button_top = M5Btn(text='', x=60, y=10, w=200, h=100, bg_c=0x87CEEB, text_c=0xFFFFFF, font=FONT_MONT_18)
# Petits boutons (bas)
button_left = M5Btn(text='', x=20, y=130, w=130, h=100, bg_c=0x90EE90, text_c=0xFFFFFF, font=FONT_MONT_18)
button_right = M5Btn(text='', x=170, y=130, w=130, h=100, bg_c=0xFFD700, text_c=0xFFFFFF, font=FONT_MONT_18)

# === LABELS ===
# Haut
label_top_title = M5Label('', x=110, y=30, color=0x000000, font=FONT_MONT_20)
label_top_value = M5Label('', x=120, y=65, color=0x000000, font=FONT_MONT_26)
# Bas gauche
label_left_title = M5Label('', x=40, y=150, color=0x000000, font=FONT_MONT_18)
label_left_value = M5Label('', x=55, y=180, color=0x000000, font=FONT_MONT_22)
# Bas droit
label_right_title = M5Label('', x=195, y=150, color=0x000000, font=FONT_MONT_18)
label_right_value = M5Label('', x=205, y=180, color=0x000000, font=FONT_MONT_22)

# === FONCTIONS ===
def update_labels():
    label_top_title.set_text(data_values[rotation_index % 3][0])
    label_top_value.set_text(data_values[rotation_index % 3][1])

    label_left_title.set_text(data_values[(rotation_index + 1) % 3][0])
    label_left_value.set_text(data_values[(rotation_index + 1) % 3][1])

    label_right_title.set_text(data_values[(rotation_index + 2) % 3][0])
    label_right_value.set_text(data_values[(rotation_index + 2) % 3][1])

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

# === ACTIONS SUR CLIC ===
button_top.pressed(rotate_data)
button_left.pressed(rotate_data)
button_right.pressed(rotate_data)

# === LOOP PRINCIPALE ===
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
