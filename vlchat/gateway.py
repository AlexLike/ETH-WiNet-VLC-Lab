from queue import Queue, Empty
from threading import Event
from time import sleep
from serial import Serial, SerialException
from shared.byte_coders import *
from queue import Queue

class Gateway():
  """An object that listens for messages arriving and sends messages from its queue."""

  def __init__(self, quit_event: Event, serial: Serial, recipient: str):
    self.quit_event = quit_event
    self.s = serial
    self.recipient = recipient
    self.send_queue = Queue(maxsize=10)
    self.receive_queue = Queue(maxsize=10)

  def enqueue_message_for_sending(self, string: str):
    """Enqueues the given message for the given recipient for sending. Throws a `queue.Full` exception, if the queue is full."""
    self.send_queue.put((string, self.recipient), timeout=0.1)

  def get_message(self) -> str | None:
    """Dequeues the oldest message from the receive queue. If no messages have arrived, `None` is returned."""
    try:
      message = self.receive_queue.get(timeout=0.1)
      self.receive_queue.task_done()
      return message
    except Empty:
      return None
  
  def send_from_queue(self):
    """If the send queue isn't empty, sends the oldest message via Serial."""
    try:
      (message, recipient) = self.send_queue.get(timeout=0.1)
      self.send_queue.task_done()
    except Empty:
      return
    raw_output = enc(f"m[{message}\0,{recipient}]\n")
    self.s.write(raw_output)
    response = self.receive()
    assert "1" in response
    while self.receive() != "m[D]":
      pass
  
  def receive(self) -> str:
    """Reads one line from serial. If a message arrives, adds it to the corresponding queue."""
    input = dec(self.s.read_until()).strip()
    if input.startswith("m[R,D,"):
      self.receive_queue.put((input[6:-1].strip(), self.recipient))
    return input

  def event_loop(self):
    try:
      while not self.quit_event.is_set():
        self.receive()
        self.send_from_queue()
    except SerialException:
      self.quit_event.set()
  
