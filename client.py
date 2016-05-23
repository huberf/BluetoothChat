from bluetooth import *
import sys

if sys.version < '3':
    input = raw_input

addr = None

if len(sys.argv) < 2:
    print("No device specified.  Searching all nearby bluetooth devices for other message enabled devices.")
else:
    addr = sys.argv[1]
    print("Searching for other chat enabled devices on %s" % addr)

# search for the SampleServer service
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_matches = find_service( uuid = uuid, address = addr )

if len(service_matches) == 0:
    print("Couldn't find another device.")
    print("Press enter to close...")
    input()
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("Connecting to \"%s\" on %s" % (name, host))

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))

print("Connected. Begin messaging...")
while True:
    data = input("> ")
    print("")
    if len(data) == 0: break
    sock.send(data)

sock.close()
