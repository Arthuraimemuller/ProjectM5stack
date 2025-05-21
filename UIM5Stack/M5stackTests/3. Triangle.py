from m5stack import *
from m5ui import *
from uiflow import *
import unit
import urequests
import time

# === CONFIGURATION ===
API_KEY = '72dbcc9258a8493ae64994a80e22e830'
CITY = 'Geneva'
COUNTRY = 'CH'

# === SENSORS ===
env_sensor = unit.get(unit.ENV3, unit.PORTA)
pir_sensor = unit.get(unit.PIR, unit.PORTB)

# === UI SETUP ===
setScreenColor(0xFFFFFF)

# === DATA ===
data = [
    ['Outdoor Temp.', '-- °C'],
    ['Indoor Temp.', '-- °C'],
    ['Humidity', '-- %']
]
index = 0

# === BUTTONS ===
btn_colors = [0x87CEEB, 0x90EE90, 0xFFD700]  # Sky blue, light green, gold

button_top = M5Btn('', 60, 20, 200, 100, bg_c=btn_colors[0])
button_left = M5Btn('', 20, 130, 140, 100, bg_c=btn_colors[1])
button_right = M5Btn('', 170, 130, 140, 100, bg_c=btn_colors[2])

# === LABELS ===
label_datetime = M5Label('', 10, 5, 0x000000, FONT_MONT_14)
label_top_title = M5Label('', 110, 30, 0x000000, FONT_MONT_14)
label_top_value = M5Label('', 120, 65, 0x000000, FONT_MONT_18)
label_left_title = M5Label('', 40, 150, 0x000000, FONT_MONT_14)
label_left_value = M5Label('', 55, 180, 0x000000, FONT_MONT_18)
label_right_title = M5Label('', 195, 150, 0x000000, FONT_MONT_14)
label_right_value = M5Label('', 205, 180, 0x000000, FONT_MONT_18)
label_smiley = M5Label('', 250, 10, 0x000000, FONT_MONT_18)

# === COLOR UTILS ===
def interpolate(color1, color2, ratio):
    """Linearly interpolate between two RGB colors."""
    def channel(c1, c2): return int((1 - ratio) * c1 + ratio * c2)
    r = channel((color1 >> 16) & 0xFF, (color2 >> 16) & 0xFF)
    g = channel((color1 >> 8) & 0xFF, (color2 >> 8) & 0xFF)
    b = channel(color1 & 0xFF, color2 & 0xFF)
    return (r << 16) | (g << 8) | b

def temp_to_color(temp):
    """Return a color based on temperature value."""
    if temp < 0:
        return 0x00008B  # Dark blue
    elif temp <= 30:
        return interpolate(0x00008B, 0x87CEFA, temp / 30)  # Dark blue → Light blue
    elif temp <= 37:
        return interpolate(0x87CEFA, 0xFFD700, (temp - 30) / 7)  # Light blue → Yellow
    elif temp <= 45:
        return interpolate(0xFFD700, 0xFF0000, (temp - 37) / 8)  # Yellow → Red
    else:
        return 0xFF0000  # Red

# === DISPLAY HELPERS ===
def update_display():
    """Update label texts and apply color based on selected data."""
    title, value = data[index]
    label_top_title.set_text(title)
    label_top_value.set_text(value)

    try:
        temp = float(value.replace("°C", "").strip()) if "Temp" in title else None
        color = temp_to_color(temp) if temp is not None else 0x000000
    except:
        color = 0x000000

    # Other labels
    left = (index + 1) % 3
    right = (index + 2) % 3
    label_left_title.set_text(data[left][0])
    label_left_value.set_text(data[left][1])
    label_right_title.set_text(data[right][0])
    label_right_value.set_text(data[right][1])

def rotate_data(_=None):
    """Cycle through data items and rotate button colors."""
    global index
    index = (index + 1) % 3
    update_display()

    btn_colors.append(btn_colors.pop(0))
    button_top.set_bg_color(btn_colors[0])
    button_left.set_bg_color(btn_colors[1])
    button_right.set_bg_color(btn_colors[2])

# === SENSOR READERS ===
def read_env():
    """Read internal temperature and humidity."""
    try:
        return round(env_sensor.temperature, 1), round(env_sensor.humidity, 1)
    except:
        return None, None

# === SENSOR READERS ===
def read_outdoor_temp():
    """Fetch outdoor temperature from OpenWeather."""
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}&units=metric'.format(CITY, COUNTRY, API_KEY)
        res = urequests.get(url)
        temp = round(res.json()['main']['temp'], 1)
        res.close()
        return temp
    except:
        return None

# === TIME ===
rtc.settime('ntp', host='de.pool.ntp.org', tzone=2)

def update_time():
    """Update displayed time."""
    dt = rtc.datetime()
    label_datetime.set_text("{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(dt[0], dt[1], dt[2], dt[4], dt[5], dt[6]))

# === MOTION FEEDBACK ===
def show_smiley(): label_smiley.set_text("Hey!") if label_smiley else None
def hide_smiley(): label_smiley.set_text("") if label_smiley else None

# === BIND BUTTONS ===
button_top.pressed(rotate_data)
button_left.pressed(rotate_data)
button_right.pressed(rotate_data)

# === MAIN LOOP ===
while True:
    # Read indoor values
    temp_in, humidity = read_env()
    if temp_in is not None:
        data[1][1] = "{:.1f} °C".format(temp_in)
        data[2][1] = "{:.1f} %".format(humidity)

    # Read outdoor temperature
    temp_out = read_outdoor_temp()
    if temp_out is not None:
        data[0][1] = "{:.1f} °C".format(temp_out)

    # Update UI
    update_display()
    update_time()
    show_smiley() if pir_sensor.state else hide_smiley()

    wait_ms(3000)  # Read data every 3 seconds
