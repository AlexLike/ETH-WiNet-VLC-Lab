from threading import Event
from gateway import Gateway
from keyboard import add_hotkey

class CLI():
  """An object that handles user I/O and communicates with a provided Gateway."""

  def __init__(self, quit_event: Event, g: Gateway):
    self.quit_event = quit_event
    self.g = g
    self.isAcceptingUserInput = False
    add_hotkey("enter", self.prepare_for_user_input)
    
  def prepare_for_user_input(self):
    self.isAcceptingUserInput = True
  
  def event_loop(self):
    while not self.quit_event.is_set():
      # Attempt to receive a message.
      received_message = self.g.get_message()
      if received_message:
        (message, sender) = received_message
        print(f"{sender}: {message}")
      # Listen for user input, and send a message.
      if self.isAcceptingUserInput:
        input()
        message = input("> ")
        if len(message) <= 200:
          self.g.enqueue_message_for_sending(message)
        else:
          print("Maximum length exceeded. Please send multiple messages.")
        self.isAcceptingUserInput = False

        