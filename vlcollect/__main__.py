from math import dist
from sys import path

from scipy.spatial import distance
path.append(".")

from shared.utils import *
from shared.serial_setup import *
from measurer import Measurer
from time import sleep

print("""
        __    ___      _ _           _   
/\   /\/ /   / __\___ | | | ___  ___| |_ 
\ \ / / /   / /  / _ \| | |/ _ \/ __| __|
 \ V / /___/ /__| (_) | | |  __/ (__| |_ 
  \_/\____/\____/\___/|_|_|\___|\___|\__|

by Cedric Keller & Alexander Zank.\n                                       
""")

DEFAULT_PORT = default_port()
port = prompt_with_default("Use this serial port", DEFAULT_PORT)

is_measuring = prompt_with_default("This station sends payloads and does the measuring", "yes").lower() == "yes"
address = "AA" if is_measuring else "AB"

if (is_measuring):
  DEFAULT_DISTANCE = 4
  distance_cm = prompt_with_default("The two stations' distance in cm", DEFAULT_DISTANCE)

  DEFAULT_PAYLOAD_SIZE = 64
  payload_size = prompt_with_default("Send payloads of this length in B", DEFAULT_PAYLOAD_SIZE)

  DEFAULT_MAX_RUNNING_TIME = 20
  max_running_time_s = prompt_with_default("Measure for at most this amount of seconds", DEFAULT_MAX_RUNNING_TIME)

print("Establishing serial connection to transceiver...")
serial = serial_setup(port, address)
print("Done. Now Measuring...")

try:
  if (is_measuring):
    measurer = Measurer(distance_cm, payload_size, max_running_time_s, serial)
    measurer.measure()
    measurer.print_and_save_stats()
  else:
    print("Acknowledging everything I receive...")
    while True:
      serial.read_until()
      sleep(0.01)
except KeyboardInterrupt:
  print("\nQuitting execution...")
  exit()