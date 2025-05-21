from m5stack import *
from m5ui import *
from uiflow import *
import unit
import urequests
import time


# === CONFIG ===
OPENWEATHER_API_KEY = '72dbcc9258a8493ae64994a80e22e830'
CITY = 'Geneva'
COUNTRY_CODE = 'CH'

# === CAPTEUR ENVIII ===
env3 = unit.get(unit.ENV3, unit.PORTA)
pir = unit.get(unit.PIR, unit.PORTB)

# === ÉCRAN ===
setScreenColor(0xFFFFFF)

# === DONNÉES INITIALES ===
data_values = [
    ['Outdoor Temp.', '-- °C'],
    ['Indoor Temp.', '-- °C'],
    ['Humidity', '-- %']
]
rotation_index = 0

# === BOUTONS ===
button_top = M5Btn(text='', x=60, y=20, w=200, h=100, bg_c=0x87CEEB, text_c=0xFFFFFF, font=FONT_MONT_14)
button_left = M5Btn(text='', x=20, y=130, w=140, h=100, bg_c=0x90EE90, text_c=0xFFFFFF, font=FONT_MONT_14)
button_right = M5Btn(text='', x=170, y=130, w=140, h=100, bg_c=0xFFD700, text_c=0xFFFFFF, font=FONT_MONT_14)

button_colors = [0x87CEEB, 0x90EE90, 0xFFD700]

# === LABELS ===
# Ajout label date/heure en haut à droite
label_datetime = M5Label('', x=10, y=5, color=0x000000, font=FONT_MONT_14)

label_top_title = M5Label('', x=110, y=30, color=0x000000, font=FONT_MONT_14)
label_top_value = M5Label('', x=120, y=65, color=0x000000, font=FONT_MONT_18)
label_left_title = M5Label('', x=40, y=150, color=0x000000, font=FONT_MONT_14)
label_left_value = M5Label('', x=55, y=180, color=0x000000, font=FONT_MONT_18)
label_right_title = M5Label('', x=195, y=150, color=0x000000, font=FONT_MONT_14)
label_right_value = M5Label('', x=205, y=180, color=0x000000, font=FONT_MONT_18)

label_smiley = M5Label('', x=250, y=10, color=0x000000, font=FONT_MONT_18)




# === FONCTION DÉGRADÉ DE COULEURS ===
def interpolate_color(color1, color2, factor):
    r1, g1, b1 = (color1 >> 16) & 0xFF, (color1 >> 8) & 0xFF, color1 & 0xFF
    r2, g2, b2 = (color2 >> 16) & 0xFF, (color2 >> 8) & 0xFF, color2 & 0xFF
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return (r << 16) | (g << 8) | b


def get_temp_color(temp):
    if temp < 0:
        return 0x00008B  # Bleu foncé
    elif temp <= 30:
        factor = temp / 30.0
        return interpolate_color(0x00008B, 0x87CEFA, factor)
    elif temp <= 37:
        factor = (temp - 30) / 7.0
        return interpolate_color(0x87CEFA, 0xFFD700, factor)
    elif temp <= 45:
        factor = (temp - 37) / 8.0
        return interpolate_color(0xFFD700, 0xFF0000, factor)
    else:
        return 0xFF0000  # Rouge


# === AFFICHAGE SMILEY SI DÉTECTION MOUVEMENT ===
smiley_label = None


def show_smiley():
    #global label_smiley
    if label_smiley:
      label_smiley.set_text("Hey!")

def hide_smiley():
    if label_smiley:
        label_smiley.set_text("")


# === MISE À JOUR DE L'AFFICHAGE ===
def update_labels():
    global data_values, rotation_index

    current_label = data_values[rotation_index % 3][0]
    current_value = data_values[rotation_index % 3][1]

    label_top_title.set_text(current_label)
    label_top_value.set_text(current_value)

    try:
        if "Temp." in current_label:
            temp = float(current_value.replace("°C", "").strip())
            color = get_temp_color(temp)
        else:
            color = 0x000000
    except:
        color = 0x000000

    # Autres labels
    label_left_title.set_text(data_values[(rotation_index + 1) % 3][0])
    label_left_value.set_text(data_values[(rotation_index + 1) % 3][1])

    label_right_title.set_text(data_values[(rotation_index + 2) % 3][0])
    label_right_value.set_text(data_values[(rotation_index + 2) % 3][1])


# === CHANGEMENT DE VALEUR AFFICHÉE AU CLIC ===
def rotate_data(button=None):
    global rotation_index

    rotation_index = (rotation_index + 1) % 3
    update_labels()

    # Rotation des couleurs des boutons
    button_colors.append(button_colors.pop(0))
    button_top.set_bg_color(button_colors[0])
    button_left.set_bg_color(button_colors[1])
    button_right.set_bg_color(button_colors[2])


# === LECTURE DU CAPTEUR ENVIII ===
def read_env_sensor():
    try:
        temp = round(env3.temperature, 1)
        humid = round(env3.humidity, 1)
        return temp, humid
    except:
        return None, None


# === RÉCUPÉRATION TEMP EXTÉRIEURE ===
def get_outdoor_temp():
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}&units=metric'.format(CITY, COUNTRY_CODE,
                                                                                                    OPENWEATHER_API_KEY)
        r = urequests.get(url)
        data = r.json()
        temp_ext = round(data['main']['temp'], 1)
        r.close()
        return temp_ext
    except:
        return None


# === ACTION BOUTONS ===
button_top.pressed(rotate_data)
button_left.pressed(rotate_data)
button_right.pressed(rotate_data)



# Initialize RTC instance
#rtc_instance = rtc.RTC()
rtc.settime('ntp', host='de.pool.ntp.org', tzone=2)


def update_datetime():
    # rtc_instance.datetime returns tuple (year, month, day, weekday, hour, min, sec, subseconds)
    dt = rtc.datetime()
    date_str = "{:04d}-{:02d}-{:02d}".format(dt[0], dt[1], dt[2])
    time_str = "{:02d}:{:02d}:{:02d}".format(dt[4], dt[5], dt[6])
    label_datetime.set_text(date_str + ' ' + time_str)


# === SETUP POUR LE CHANGEMENT DE COULEUR TOUTES LES 10 SECONDES ===
last_color_change_time = time.time()
current_screen_color = None  # Mémoriser la dernière couleur appliquée

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

    # Mise à jour date/heure
    update_datetime()


    current_time = time.time()

    if pir.state == 1:
        show_smiley()
    else:
        hide_smiley()



    wait_ms(3)