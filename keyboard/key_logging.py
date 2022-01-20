import json
from threading import Timer
from pynput import keyboard
import os


def main():
  cached_key = []
  keylogs = {}

  vk_keymap = {
    "8": "BACKSPACE",
    "9": "TAB",
    '13': "ENTER",
    "16": "SHIFT",
    "17": "CTRL",
    "18": "ALT",
    "19": "PAUSE",
    "20": "CAPSLOCK",
    "32": "SPACEBAR",
    "33": "PAGEUP",
    "34": "PAGEDOWN",
    "35": "END",
    "36": "HOME",
    "37": "LEFTARROW",
    "38": "UPARROW",
    "39": "RIGHTARROW",
    "40": "DOWNARROW",
    "41": "SELECT",
    "42": "PRINT",
    "43": "EXECUTE",
    "44": "PRTSC",
    "45": "INSERT",
    "46": "DELETE",
    "47": "HELP",
    "91": "LWIN",
    "92": "RWIN",
  }


  def on_press(key):
    if key not in cached_key:
      cached_key.append(key)

    

  def on_release(key):
    pressed = []
    try:
      pressed = list(map(lambda x: x.char, cached_key))
    except AttributeError:
      pass
    if 'e' in pressed and 'x' in pressed and 'i' in pressed and 't' in pressed:
      print("Saving data and exiting program now..")
      save_file(keylogs, 'keylogged.json')
      os._exit(1)
    if key in cached_key:
      cached_key.remove(key)
    try:
      key_name = ""
      if hasattr(key, 'char') and key.char is not None:
        key_name = key.char
      elif hasattr(key, 'name') and key.name is not None:
        key_name = key.name
      elif hasattr(key, 'value') and key.value is not None:
        key_name = vk_keymap.get(key.value.vk)
      elif hasattr(key, 'vk') and key.vk is not None:
        if 96 <= key.vk <= 105:
          key_name = f'VK_NUMPAD{key.vk-96}'
        else:
          key_name = f'VK_{key.vk}'
      else:
        key_name = "None"
      if key_name in keylogs:
        keylogs[key_name] += 1
      else:
        keylogs[key_name] = 1
    except AttributeError:
      print(key) 


  def scheduler(interval, action, actionargs=()):
    t = Timer(interval=interval, function=scheduler, args=(interval, action, actionargs))
    t.start()
    action(*actionargs)
  
  def open_file(file_path):
    file = {}
    if (os.path.isfile(file_path)):
      with open(file_path, 'r') as f:
        file = json.load(f)
    return file
  def save_file(dict_obj, file_path):
    with open(file_path, 'w+') as f:
      json.dump(dict_obj, f)

  keylogs = open_file('keylogged.json')

  with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
  
  

  scheduler(10, save_file, (keylogs, 'keylogged.json'))
  




  

if __name__ == '__main__':
  main()

