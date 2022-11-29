import time

from pynput import keyboard
from pynput.keyboard import Key, Controller

import subprocess


controller = Controller()

taigaSeed = "2483313382402348964"
dolphinSeed = "-4530634556500121041"
gravelSeed = "-3294725893620991126"
vineSeed = "8398967436125155523"

seed = taigaSeed


def press_key(key):
    controller.press(key)
    controller.release(key)
    time.sleep(0.01)


def type_seed():
    controller.type(seed)
    time.sleep(0.01)


def get_focused_application_name():
    cmd = """
    tell application "System Events"
      set windowTitle to ""
      set frontApp to first application process whose frontmost is true
      set frontAppName to name of frontApp
      tell process frontAppName
        tell (1st window whose value of attribute "AXMain" is true)
          set windowTitle to value of attribute "AXTitle"
        end tell
      end tell
    log frontAppName
    end tell
    """

    result = subprocess.run(['osascript', '-e', cmd])
    return result.stdout


print(get_focused_application_name())


def execute():
    press_key(Key.tab)
    press_key(Key.enter)
    for i in range(3):
        press_key(Key.tab)
    press_key(Key.enter)
    for i in range(2):
        press_key(Key.tab)
    for i in range(3):
        press_key(Key.enter)
    for i in range(4):
        press_key(Key.tab)
    press_key(Key.enter)
    for i in range(3):
        press_key(Key.tab)

    type_seed()

    for i in range(6):
        press_key(Key.tab)
    press_key(Key.enter)


#with keyboard.GlobalHotKeys({'m': execute}) as h:
    #h.join()
