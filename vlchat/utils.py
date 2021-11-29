def prompt_with_default(instructions, default):
  user_input = input(f"{instructions} (default is {default}): ")
  return default if (user_input == "" or user_input.isspace()) else user_input.strip()

def enc(utf8_string):
  return utf8_string.encode("ascii")

def dec(bytes):
  return bytes.decode("ascii")

from sys import platform
from glob import glob

def default_port():
  if platform.startswith("win"):
    return "COM4"
  elif platform.startswith("linux") or platform.startswith("cygwin"):
    return next(iter(glob("/dev/tty[A-Za-z]*")), "none")
  elif platform.startswith("darwin"):
    return next(iter([x for x in glob("/dev/tty.*") if not "Bluetooth" in x]), "none")
  else:
    return "none"