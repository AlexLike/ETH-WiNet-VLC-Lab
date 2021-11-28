def prompt_with_default(instructions, default):
  user_input = input(f"{instructions} (default is {default}): ")
  return default if (user_input == "" or user_input.isspace()) else user_input.strip()

def enc(utf8_string):
  return utf8_string.encode("ascii")

def dec(bytes):
  return bytes.decode("ascii")