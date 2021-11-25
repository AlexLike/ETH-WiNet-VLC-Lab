import serial
from time import sleep
from utils import prompt_with_default

print("""
        __    ___ _           _    
/\   /\/ /   / __\ |__   __ _| |_  
\ \ / / /   / /  | '_ \ / _` | __| 
 \ V / /___/ /___| | | | (_| | |_  
  \_/\____/\____/|_| |_|\__,_|\__|

by Cedric Keller & Alexander Zank.\n
""")

# Prompt port selection.
DEFAULT_PORT = "COM4"
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
sleep(2.5)
# Set the address.
s.write(f"a[{address}]\n")
sleep(0.1)
assert str(s.read_until()) == f"a[{address}]"
# Set the retransmission limit.
s.write("c[1,0,5]\n")
sleep(0.1)
assert str(s.read_until()) == f"c[1,0,5]"
# Set the FEC threshold.
s.write("c[0,1,30]\n")
sleep(0.1)
assert str(s.read_until()) == f"c[0,1,30]"

print("Done.")

# Prompt recipient selection.
DEFAULT_RECIPIENT_ADDRESS = "AB"
recipient_address = prompt_with_default("Communicate with this hex-encoded address' owner", DEFAULT_RECIPIENT_ADDRESS)