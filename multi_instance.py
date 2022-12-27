import subprocess

import psutil
from subprocess import Popen


instances = []

def switch_to_next_instance():
    if instances.__len__() > 1:
        next_instance = instances.__getitem__(0)
        subprocess.run(['osascript', '-e', 'tell application "System Events" to set frontmost of first process whose unix id is ' + next_instance + ' to true'])
        #Popen(['osascript', '-e', 'tell application "System Events" to set frontmost of first process whose unix id is ' + next_instance + ' to true'])
        instances.remove(next_instance)
        instances.append(next_instance)


def auto_detect_instances():
    global instances
    instances.clear()
    print("Detecting Minecraft instances...")
    for process in psutil.process_iter():
        try:
            if "minecraft" in process.open_files().__str__():
                instances.append(process.pid.__str__())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    print("Found " + instances.__len__().__str__() + " Minecraft instances.")