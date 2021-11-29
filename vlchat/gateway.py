import queue
from threading import Event
from time import sleep
import serial
from serial.serialposix import Serial
from serial.serialutil import SerialException
from utils import enc, dec
from queue import Queue

class Gateway():
  def __init__(self, quit_event: Event, serial: Serial, recipient: str):
    self.quit_event = quit_event
    self.s = serial
    self.recipient = recipient
    self.send_queue = Queue(maxsize=10)
    self.receive_queue = Queue(maxsize=10)

  # Enqueues the given message for the given recipient for sending. Throws a `Queue.Full` exception, if the queue is full.
  def send_message(self, utf8_string):
    self.send_queue.put((utf8_string, self.recipient), timeout=5)

  # Dequeues the oldest message from the receive queue. If no messages have arrived, `None` is returned.
  def get_message(self):
    try:
      message = self.receive_queue.get(timeout=0.1)
      self.receive_queue.task_done()
      return message
    except queue.Empty:
      return None

  def event_loop(self):
    try:
      while not self.quit_event.is_set():
        # Try to read input.
        raw_input = dec(self.s.read_until())
        if raw_input.strip() != "":
          self.receive_queue.put((f"Received raw message: {raw_input}", "sender"), timeout=1)
        # TODO: Send output.
    except serial.SerialException:
      self.quit_event.set()
  
