from threading import Event
from time import sleep
from gateway import Gateway

class CLI():
  def __init__(self, quit_event: Event, g: Gateway):
    self.quit_event = quit_event
    self.g = g
  
  def event_loop(self):
    while not self.quit_event.is_set():
      print("> ")
      sleep(0.2)