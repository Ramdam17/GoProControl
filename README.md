# GoPro USB Control

Contrôle de caméras GoPro via USB en Python.

## Installation

```bash
# Avec Poetry
poetry install

# Ou avec pip
pip install -e .
```

## Utilisation

### Exemple rapide

```python
from gopro_usb import GoProUSB

# Initialisez avec le numéro de série de votre GoPro
gopro = GoProUSB("C1234567890")

# Allumez la caméra
gopro.power_on()

# Configurez les paramètres
gopro.mode_video()
gopro.set_resolution_5_3k()
gopro.set_fps_240()
gopro.set_lens_linear()

# Enregistrez
gopro.record_start()
time.sleep(10)  # Enregistrez pendant 10 secondes
gopro.record_stop()

# Éteignez
gopro.power_off()
```

### Exemple complet

Voir `example_usage.py` pour une démonstration complète incluant :
- Power on / Power off
- Configuration (résolution 5.3K, FPS 240, Lens Linear)
- Démarrage/arrêt d'enregistrement
- Monitoring du statut en temps réel

```bash
# Exécution de l'exemple
poetry run python example_usage.py

# Ou activez l'environnement virtuel
poetry shell
python example_usage.py
```

## Fonctionnalités principales

### Contrôle de base
- `power_on()` - Allumer la caméra
- `power_off()` - Éteindre la caméra
- `record_start()` - Démarrer l'enregistrement
- `record_stop()` - Arrêter l'enregistrement

### Configuration vidéo
- `set_resolution_5_3k()` - Résolution 5.3K
- `set_resolution_5k()` - Résolution 5K
- `set_resolution_4k()` - Résolution 4K
- `set_resolution_2_7k()` - Résolution 2.7K
- `set_resolution_1080()` - Résolution 1080p

### Configuration FPS
- `set_fps_240()` - 240 FPS
- `set_fps_200()` - 200 FPS
- `set_fps_120()` - 120 FPS
- `set_fps_60()` - 60 FPS
- `set_fps_30()` - 30 FPS
- `set_fps_24()` - 24 FPS

### Configuration objectif
- `set_lens_linear()` - Linear (recommandé pour moins de distorsion)
- `set_lens_wide()` - Wide
- `set_lens_narrow()` - Narrow
- `set_lens_superview()` - SuperView
- `set_lens_max_superview()` - Max SuperView
- `set_lens_linear_horizon()` - Linear + Horizon Lock

### Statut
- `get_state()` - Récupérer l'état complet
- `get_status_realtime(interval, duration)` - Monitoring en temps réel
- `is_busy()` - Vérifier si la caméra est occupée
- `is_encoding()` - Vérifier si un encodage est en cours

### Modes
- `mode_video()` - Mode vidéo
- `mode_photo()` - Mode photo
- `mode_timelapse()` - Mode timelapse

### Médias
- `get_media_list()` - Liste des fichiers sur la carte SD
- `download_last_media(filename)` - Télécharger le dernier fichier

## Configuration réseau

La classe utilise l'adresse IP de la GoPro basée sur son numéro de série :
- Format IP : `172.2{digit3}.1{digit2-3}.51`
- Exemple : SN "C1234567890" → IP `172.29.190.51`

Assurez-vous que :
1. La GoPro est connectée en USB
2. Le contrôle USB est activé sur la caméra
3. Votre ordinateur peut communiquer avec l'IP de la GoPro

## Crédits

Basé sur le projet [goproUSB](https://github.com/drukasz/goproUSB) par Lukasz J. Nowak.

Modifications et ajouts :
- Refactorisation complète en classe Python
- Support OpenCV pour preview local
- Configuration pour GoPro Hero 12 Black
- Ajout du monitoring en temps réel
- Support du téléchargement de médias

## License

Ce projet est sous licence **GNU General Public License v3.0** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

Comme dérivé de [goproUSB](https://github.com/drukasz/goproUSB), ce projet respecte les termes de la GPL v3.0 qui requiert que toute modification ou travail dérivé soit également distribué sous GPL v3.0.
