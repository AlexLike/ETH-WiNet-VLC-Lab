from threading import Event, Thread
import serial
from signal import signal, SIGINT
from sys import platform
from time import sleep
from utils import *
from gateway import Gateway
from cli import CLI

print("""
        __    ___ _           _    
/\   /\/ /   / __\ |__   __ _| |_  
\ \ / / /   / /  | '_ \ / _` | __| 
 \ V / /___/ /___| | | | (_| | |_  
  \_/\____/\____/|_| |_|\__,_|\__|

by Cedric Keller & Alexander Zank.\n
""")

# ---------------------
# SEQUENTIAL SETUP
# - - - - - - - - - - -

# Prompt port selection.
DEFAULT_PORT = "/dev/tty.usbmodem212201" if platform.lower() == "darwin" else "COM4"
port = prompt_with_default("Use this serial port", DEFAULT_PORT)


# Prompt address selection.
DEFAULT_ADDRESS = "AA"
address = prompt_with_default("Use this as my hex-encoded address", DEFAULT_ADDRESS)

print("Establishing serial connection to transceiver...")

# Open the serial port and reset the device.
try:
  s = serial.Serial(port=port, baudrate=115200, timeout=1)
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

print("Done.")

# Prompt recipient selection.
DEFAULT_RECIPIENT_ADDRESS = "AB"
recipient_address = prompt_with_default("Communicate with this hex-encoded address' owner", DEFAULT_RECIPIENT_ADDRESS)


# ---------------------
# PARALLEL SERVICES
# - - - - - - - - - - -

# Exit on keyboard interrupts.
quit_event = Event()
quit_event.clear()
def quit(sig, frame):
  quit_event.set()
  print("\nQuitting execution...")
  exit()
signal(SIGINT, quit)

# Instantiate a gateway thread that sends and receives messages.
gateway = Gateway(quit_event, s)
gateway_thread = Thread(target=gateway.event_loop)
gateway_thread.start()

# Instantiate a CLI thread that handles user I/O.
cli = CLI(quit_event, gateway)
cli_thread = Thread(target=cli.event_loop)
cli_thread.start()

gateway_thread.join()
cli_thread.join()