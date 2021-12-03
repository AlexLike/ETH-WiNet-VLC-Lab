def prompt_with_default(instructions: str, default):
  """Prompts the user for input and returns the default value if nothing is entered."""
  user_input = input(f"{instructions} (default is {default}): ").strip()
  return default if not user_input else type(default)(user_input)

def default_port():
  """"Returns a default serial port guess. On macOS and Linux, returns some available tty interface. On Windows, returns constant COM4."""
  from sys import platform
  from glob import glob
  if platform.startswith("win"):
    return "COM4"
  elif platform.startswith("linux") or platform.startswith("cygwin"):
    return next(iter(glob("/dev/tty[A-Za-z]*")), "none")
  elif platform.startswith("darwin"):
    return next(iter([x for x in glob("/dev/tty.*") if not "Bluetooth" in x]), "none")
  else:
    return "none"