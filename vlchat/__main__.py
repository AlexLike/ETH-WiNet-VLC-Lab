from sys import path
path.append(".")

from shared.utils import *
from shared.byte_coders import *
from shared.serial_setup import *
from threading import Event, Thread
from signal import signal, SIGINT
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
DEFAULT_PORT = default_port()
port = prompt_with_default("Use this serial port", DEFAULT_PORT)

# Prompt address selection.
DEFAULT_ADDRESS = "AA"
address = prompt_with_default("Use this as my hex-encoded address", DEFAULT_ADDRESS)

# Prime the microcontroller.
print("Establishing serial connection to transceiver...")
serial = serial_setup(port, address)
print("Done.")

# Prompt recipient selection.
DEFAULT_RECIPIENT_ADDRESS = "AB"
recipient_address = prompt_with_default("Communicate with this hex-encoded address' owner", DEFAULT_RECIPIENT_ADDRESS)

print("Listening... Press ⮐  to open the message prompt.\n")


# ---------------------
# PARALLEL SERVICES
# - - - - - - - - - - -

# Exit on keyboard interrupts.
quit_event = Event()
quit_event.clear()
def quit(*_):
  quit_event.set()
  print("\nQuitting execution...")
  exit()
signal(SIGINT, quit)

# Instantiate a gateway thread that sends and receives messages.
gateway = Gateway(quit_event, serial, recipient_address)
gateway_thread = Thread(target=gateway.event_loop)
gateway_thread.start()

# Run the CLI that handles user I/O on the main thread.
cli = CLI(quit_event, gateway)
cli.event_loop()

gateway_thread.join()