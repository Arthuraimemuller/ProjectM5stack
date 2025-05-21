from m5stack import *
from m5ui import *
from uiflow import *

setScreenColor(0x111111)

# Crée une interface stylisée
label = M5TextBox(20, 0, "Choisir une pièce", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)

# Boutons pour chaque pièce
btn_salon = M5Btn(text="Salon", x=30, y=40, w=100, h=50, bg_c=0x222222, text_c=0xffffff, font=FONT_MONT_14)
btn_cuisine = M5Btn(text="Cuisine", x=160, y=40, w=100, h=50, bg_c=0x222222, text_c=0xffffff, font=FONT_MONT_14)
btn_chambre = M5Btn(text="Chambre", x=30, y=110, w=100, h=50, bg_c=0x222222, text_c=0xffffff, font=FONT_MONT_14)
btn_sdb = M5Btn(text="Salle de bain", x=160, y=110, w=100, h=50, bg_c=0x222222, text_c=0xffffff, font=FONT_MONT_14)
btn_bureau = M5Btn(text="Bureau", x=30, y=180, w=100, h=50, bg_c=0x222222, text_c=0xffffff, font=FONT_MONT_14)
btn_balcon = M5Btn(text="Balcon", x=160, y=180, w=100, h=50, bg_c=0x222222, text_c=0xffffff, font=FONT_MONT_14)

# Exemple de callback
def show_room_data(room_name):
    # Ici tu appelles BigQuery/local data pour afficher les mesures de la pièce
    label.setText("Température: 22°C\nHumidité: 43%\nAir: OK")

btn_salon.pressed(lambda: show_room_data("salon"))
btn_cuisine.pressed(lambda: show_room_data("cuisine"))
btn_chambre.pressed(lambda: show_room_data("chambre"))
btn_sdb.pressed(lambda: show_room_data("sdb"))
btn_bureau.pressed(lambda: show_room_data("bureau"))
btn_balcon.pressed(lambda: show_room_data("balcon"))
