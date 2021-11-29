from threading import Event
from time import sleep
from gateway import Gateway
from keyboard import add_hotkey, is_pressed

class CLI():
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
      # Stop receiving, listen for user input, and send a message.
      if self.isAcceptingUserInput:
        input()
        message = input("> ")
        if len(message) <= 180:
          self.g.send_message(message)
          self.isAcceptingUserInput = False
        else:
          print("Maximum length exceeded. Please send multiple messages.")

        