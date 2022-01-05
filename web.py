import eel
import random
from datetime import datetime

eel.init('web')

@eel.expose
def get_random_name():
    eel.prompt_alerts('Random name')

@eel.expose
def get_random_number():
    eel.prompt_alerts(random.randint(1, 100))

@eel.expose
def get_date():
    eel.prompt_alerts(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

@eel.expose
def get_ip():
    eel.prompt_alerts('127.0.0.1')


#
# eel.start('index.html', mode='chrome-app',
#                         host='localhost',
#                         port=27000,
#                         block=True,
#                         size=(700, 480),
#                         position=(0,0),
#                         disable_cache=True,
#                         cmdline_args=['--browser-startup-dialog',
#                                 '--incognito', '--no-experiments'])
import os
import sys

def resource_path(rel_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

eel.browsers.set_path('electron', resource_path('node_modules/electron/dist/electron.exe'))

eel.start("index.html",mode='electron')