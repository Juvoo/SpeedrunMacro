import time

import pynput.mouse

from pynput import keyboard
from pynput.keyboard import Key

import subprocess

import multi_instance


keyboardController = pynput.keyboard.Controller()
mouseController = pynput.mouse.Controller()

taigaSeed = "2483313382402348964"
dolphinSeed = "-4530634556500121041"
gravelSeed = "-3294725893620991126"
vineSeed = "8398967436125155523"

seed = taigaSeed

multi_instance_enabled = True

def press_key(key):
    keyboardController.press(key)
    keyboardController.release(key)
    time.sleep(0.01)


def press_button(button):
    mouseController.press(button)
    mouseController.release(button)
    time.sleep(0.01)


def move_to_point(x, y):
    mouseController.move(x, y)
    time.sleep(0.01)


def type_seed():
    type_string(seed)


def type_string(string):
    keyboardController.type(string)
    time.sleep(0.01)


def minecraft_window_focused():
    p = subprocess.run(['osascript', '-e', 'tell application "System Events"', '-e', 'set windowTitle to name of (front window of (first application process whose frontmost is true))', '-e', 'copy windowTitle to stdout', '-e', 'end tell'], capture_output=True)
    return "Minecraft" in p.stdout.__str__()


def execute_ssg():
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

    if multi_instance_enabled:
        multi_instance.switch_to_next_instance()



def execute_rsg():
    if minecraft_window_focused():
        press_key(Key.tab)
        press_key(Key.enter)
        for i in range(3):
            press_key(Key.tab)
        press_key(Key.enter)
        for i in range(2):
            press_key(Key.tab)
        for i in range(3):
            press_key(Key.enter)
        for i in range(5):
            press_key(Key.tab)
        press_key(Key.enter)

        if multi_instance_enabled:
            multi_instance.switch_to_next_instance()


def execute_duo_rsg():
    if minecraft_window_focused():
        press_key(Key.tab)

        press_key(Key.enter)
        for i in range(3):
            press_key(Key.tab)
        press_key(Key.enter)
        for i in range(2):
            press_key(Key.tab)
        for i in range(3):
            press_key(Key.enter)
        press_key(Key.tab)
        press_key(Key.enter)
        for i in range(4):
            press_key(Key.tab)
        press_key(Key.enter)

        if multi_instance_enabled:
            multi_instance.switch_to_next_instance()

def execute_publish():
    press_key('t')
    time.sleep(0.1)
    type_string('/publish 25565')
    press_key(Key.enter)


if multi_instance_enabled:
    multi_instance.auto_detect_instances()

with keyboard.GlobalHotKeys({'t': execute_rsg
                             ,
                            ']': execute_publish}) as h:
    h.join()
