
def prompt_with_default(instructions, default):
  user_input = input(f"{instructions} (default is {default}): ")
  return default if (user_input == "" or user_input.isspace()) else user_input.strip()
