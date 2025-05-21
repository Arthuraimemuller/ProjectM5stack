
Voici la liste des méthodes et attributs accessibles sur un objet `M5Btn` ou `M5Label`, tel qu'obtenu manuellement via `print(dir(button))` ou `print(dir(label))` et en utilisant un label_debug pour afficher sur l'écran du m5stack. Je n'ai pas trouvé les informations sur internet:


## Références — M5Btn (M5Stack UIFlow)

### Méthodes et attributs accessibles via `dir(M5Btn)`

- `__class__`  
- `__init__`  
- `__module__`  
- `__qualname__`  
- `__dict__`  

### Méthodes fonctionnelles :
- `cb` — Callback associé (lecture seule ou interne selon firmware).  
- `delete()` — Supprime le bouton de l'écran.  
- `get-state()` — Renvoie l'état du bouton (ex: pressé ou non).  
- `set_align(align)` — Définit l’alignement du bouton (gauche, centre, droite).  
- `set_bg_color(color)` — Définit la couleur de fond du bouton (`0xRRGGBB`).  
- `set_cb(callback_function)` — Associe une fonction callback lors du clic.  
- `set_hidden(bool)` — Affiche ou masque le bouton.  
- `set_pos(x, y)` — Positionne le bouton à l'écran.  
- `set_size(width, height)` — Définit les dimensions du bouton.  
- `set_btn_text(text)` — Définit le texte affiché dans le bouton.  
- `set_btn_text_color(color)` — Définit la couleur du texte du bouton.  
- `set_btn_text_font(font)` — Définit la police du texte (ex: `FONT_MONT_14`).  

### Événements :
- `pressed(callback)` — Déclenche la fonction `callback` lors d’un appui.  
- `released(callback)` — Déclenche la fonction `callback` lors du relâchement.  
- `__callback__` — Callback interne lié à l'objet (rarement utilisé directement).

### Attributs :
- `btn_text` — Texte actuel du bouton (lecture/écriture selon firmware).  
- `btn_label_obj` — Objet interne du label dans le bouton.  
- `obj` — Objet graphique interne LVGL.

### Notes :
- Les boutons sont **arrondis avec un cadre gris par défaut**.
- Il **n'existe pas de méthode** pour changer la forme ou supprimer la bordure.
- Pour un style sans cadre, utiliser `M5Canvas` comme alternative plus personnalisable.


## Références — M5Label (M5Stack UIFlow)

### Méthodes et attributs accessibles via `dir(M5Label)`

- `__class__`  
- `__init__`  
- `__module__`  
- `__qualname__`  
- `__dict__`  

### Méthodes fonctionnelles :
- `delete()` — Supprime le label de l'écran.  
- `get_state()` — Renvoie l'état du label (visible, etc.).  
- `get_width()` — Renvoie la largeur du texte du label.  
- `set_align(align)` — Définit l'alignement (ex. `0`, `1`, `2` pour gauche, centre, droite).  
- `set_cb(callback_function)` — Associe une fonction callback au label (si cliquable).  
- `set_hidden(bool)` — Masque ou affiche le label.  
- `set_long_mode(mode)` — Définit le comportement si le texte est long (ex: couper, faire défiler, etc.).  
- `set_pos(x, y)` — Définit la position du label.  
- `set_size(width, height)` — Définit la taille de la zone du label.  
- `set_text(string)` — Modifie le texte affiché.  
- `set_text_color(color)` — Change la couleur du texte (`0x000000` pour noir, par exemple).  
- `set_text_font(font)` — Définit la police (ex: `FONT_MONT_14`).  

### Attributs :
- `text` — Accès direct au contenu textuel (lecture/écriture possible selon firmware).  
- `style` — Objet contenant les styles du label (non modifiable directement dans certains firmwares).  
- `obj` — Référence interne à l’objet LVGL utilisé.

### Notes :
- Le label peut afficher plusieurs lignes avec `\n` dans le texte.
- `set_long_mode(0)` permet de couper le texte s’il dépasse, `set_long_mode(1)` de le faire défiler, etc.
