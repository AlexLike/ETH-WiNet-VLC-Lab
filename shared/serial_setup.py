from serial import Serial
from time import sleep
from .byte_coders import *

def serial_setup(port: str, address: str) -> Serial:
  """Primes the microcontroller with sensible defaults."""
  # Open the serial port and reset the device.
  try:
    s = Serial(port=port, baudrate=115200, timeout=1)
  except:
    print(f"Could not open port {port}. Please try again.")
    exit()
  sleep(2)
  # Set the address.
  s.write(enc(f"a[{address}]\n"))
  sleep(0.1)
  assert dec(s.read_until()) == f"a[{address}]\n"
  # Set the retransmission limit.
  s.write(enc("c[1,0,5]\n"))
  sleep(0.1)
  assert dec(s.read_until()) == "c[1,0,5]\n"
  # Set the FEC threshold.
  s.write(enc("c[0,1,30]\n"))
  sleep(0.1)
  assert dec(s.read_until()) == "c[0,1,30]\n"
  return s