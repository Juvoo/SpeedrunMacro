import time, pynput.mouse, subprocess, psutil, logging

from pynput import keyboard
from pynput.keyboard import Key


keyboardController = pynput.keyboard.Controller()
mouseController = pynput.mouse.Controller()

taigaSeed = "2483313382402348964"
dolphinSeed = "-4530634556500121041"
gravelSeed = "-3294725893620991126"
vineSeed = "8398967436125155523"

seed = taigaSeed

multi_instance_enabled = True
speak_info = False
freeze_instances = False

instances = []


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
    try:
        focused_window_pid = subprocess.check_output(['osascript', '-e', 'tell application "System Events"', '-e', 'set pid to unix id of first application process whose frontmost is true', '-e', 'return pid', '-e', 'end tell'])
        process = psutil.Process(int(focused_window_pid))
        return process.pid.__str__() in instances
    except subprocess.CalledProcessError:
        return False


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
        switch_to_next_instance()


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
            switch_to_next_instance()


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
            switch_to_next_instance()


def execute_publish():
    if minecraft_window_focused():
        press_key('t')
        time.sleep(0.1)
        type_string('/publish 25565')
        press_key(Key.enter)


def switch_to_next_instance():
    if instances.__len__() > 1:
        next_instance = instances.__getitem__(0)
        subprocess.run(['osascript', '-e', 'tell application "System Events" to set frontmost of first process whose unix id is ' + next_instance + ' to true'])
        instances.remove(next_instance)
        instances.append(next_instance)


def auto_detect_instances():
    if multi_instance_enabled:
        instances.clear()
        print("Detecting Minecraft instances...")
        if speak_info:
            subprocess.run(['say', 'Detecting Minecraft instances'])
        for process in psutil.process_iter():
            try:
                if "minecraft" in process.open_files().__str__():
                    try:
                        window_name = subprocess.check_output(['osascript', '-e', 'tell application "System Events"', '-e', 'set windowTitle to name of (front window of (first application process whose unix id is ' + process.pid.__str__() + '))', '-e', 'return windowTitle', '-e', 'end tell']).__str__()
                        if "minecraft" or "Minecraft" in window_name:
                            instances.append(process.pid.__str__())
                    except subprocess.CalledProcessError:
                        logging.exception('\033[1;31m' + 'Encountered a problem while detecting instances. Make sure all Minecraft instances are not in fullscreen mode and are unfrozen.' + '\x1b[0m')
                        pass
            except (subprocess.CalledProcessError, psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        num_instances = instances.__len__().__str__()
        print("Found " + num_instances + " instance(s)")
        for instance in instances:
            print(instance)

        if speak_info:
            subprocess.run(['say', 'Found ' + num_instances + ' instances'])


def get_focused_instance_pid():
    if minecraft_window_focused():
        try:
            pid = subprocess.check_output(['osascript', '-e', 'tell application "System Events"', '-e', 'set pid to unix id of first application process whose frontmost is true', '-e', 'return pid', '-e', 'end tell'])
            process = psutil.Process(int(pid))
            return process.pid
        except subprocess.CalledProcessError:
            return None
    else:
        return None


def freeze_inactive_instances():
    if multi_instance_enabled and freeze_instances:
        current_instance_pid = get_focused_instance_pid()
        for pid in instances:
            current_instance_pid = ''.join(filter(str.isdigit, current_instance_pid.__str__()))
            print(current_instance_pid)
            if pid != current_instance_pid:
                process = psutil.Process(int(pid))
                process.suspend()


def unfreeze_inactive_instances():
    if multi_instance_enabled and freeze_instances:
        current_instance_pid = get_focused_instance_pid()
        for pid in instances:
            current_instance_pid = ''.join(filter(str.isdigit, current_instance_pid.__str__()))
            print(current_instance_pid)
            if pid != current_instance_pid:
                process = psutil.Process(int(pid))
                process.resume()


if __name__ == '__main__':
    if multi_instance_enabled:
        auto_detect_instances()


with keyboard.GlobalHotKeys({'[': execute_rsg, ']': execute_publish, '.': auto_detect_instances, '-': freeze_inactive_instances, '=': unfreeze_inactive_instances}) as listener:
    listener.join()
