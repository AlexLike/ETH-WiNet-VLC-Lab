from threading import Event
from time import sleep
import serial
from serial.serialposix import Serial
from serial.serialutil import SerialException
from utils import enc, dec
from queue import Queue

class Gateway():
  def __init__(self, quit_event: Event, serial: Serial):
    self.quit_event = quit_event
    self.s = serial
    self.send_queue = Queue(maxsize=10)
    self.receive_queue = Queue(maxsize=10)

  # Enqueues the given message for the given recipient for sending. Throws a `Queue.Full` exception, if the queue is full.
  def send_message(self, utf8_string, recipient):
    self.send_queue.put((utf8_string, recipient), timeout=5)

  # Dequeues the oldest message from the receive queue. If no messages have arrived, `None` is returned.
  def get_message(self):
    try:
      message = self.receive_queue.get(0.1)
      self.receive_queue.task_done()
      return message
    except Queue.empty:
      return None

  def event_loop(self):
    try:
      # Repeat until interrupted:
      while not self.quit_event.is_set():
        raw_input = dec(self.s.read_until())
        print(f"Received raw: {raw_input}")

    except serial.SerialException:
      self.quit_event.set()
  
