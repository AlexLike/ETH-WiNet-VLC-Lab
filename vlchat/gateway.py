import queue
from threading import Event
from time import sleep
from serial import Serial, SerialException
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
  def enqueue_message_for_sending(self, utf8_string):
    self.send_queue.put((utf8_string, self.recipient), timeout=0.1)

  # Dequeues the oldest message from the receive queue. If no messages have arrived, `None` is returned.
  def get_message(self):
    try:
      message = self.receive_queue.get(timeout=0.1)
      self.receive_queue.task_done()
      return message
    except queue.Empty:
      return None
  
  def send_from_queue(self):
    try:
      (message, recipient) = self.send_queue.get(timeout=0.1)
      self.send_queue.task_done()
    except queue.Empty:
      return
    raw_output = enc(f"m[{message}\0,{recipient}]\n")
    self.s.write(raw_output)
    response = self.receive()
    assert "1" in response

  
  def receive(self):
    input = dec(self.s.read_until()).strip()
    if input.startswith("m[R,D,"):
      self.receive_queue.put((input[6:-1].strip(), self.recipient))
    return input.strip() if input else None

  def event_loop(self):
    try:
      while not self.quit_event.is_set():
        self.receive()
        self.send_from_queue()
    except SerialException:
      self.quit_event.set()
  
