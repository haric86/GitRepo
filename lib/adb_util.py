import time
from core.shell import run_cmd

adb = r'C:\Android_Appium\platform-tools\adb.exe'

KEY_CODES = {
    'tab': 'KEYCODE_TAB',
    'enter': 'KEYCODE_ENTER',
}


def send_key(keycode: str, count: int = 1):
    keycode = KEY_CODES[keycode.lower()]
    for _ in range(count):
        run_cmd(f'{adb} shell input keyevent {keycode}')
        time.sleep(0.1)
    time.sleep(1)


def send_txt(txt: str):
    txt = txt.replace(' ', '%s')
    run_cmd(f'{adb} shell input text "{txt}"')


def swipe(direction: str, count: int = 1):
    if direction == 'tb':
        cmd = f'{adb} shell input swipe 500 700 500 1200'
    elif direction == 'bt':
        cmd = f'{adb} shell input swipe 500 1200 500 700'
    elif direction == 'lr':
        cmd = f'{adb} shell input swipe 100 100 800 100'
    elif direction == 'rl':
        cmd = f'{adb} shell input swipe 800 100 100 100'
    else:
        raise ValueError('Invalid direction')
    for _ in range(count):
        run_cmd(cmd)
        time.sleep(0.1)
