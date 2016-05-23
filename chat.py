from bluetooth import *
import winsound
import threading
import sys


def server():
  freq = 1000
  dur = 500

  server_sock=BluetoothSocket( RFCOMM )
  server_sock.bind(("",PORT_ANY))
  server_sock.listen(1)

  port = server_sock.getsockname()[1]

  uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

  advertise_service( server_sock, "SampleServer",
                     service_id = uuid,
                     service_classes = [ uuid, SERIAL_PORT_CLASS ],
                     profiles = [ SERIAL_PORT_PROFILE ],
#                   protocols = [ OBEX_UUID ]
                      )
                     
  print("Waiting for connection on RFCOMM channel %d" % port)

  client_sock, client_info = server_sock.accept()
  print("Accepted connection from ", lookup_name(client_info[0]) )

  try:
      while True:
          data = client_sock.recv(1024)
          if len(data) == 0: break
          print("")
          print(lookup_name( client_info[0] ) + "> " + str(data))
          winsound.Beep(freq, dur)
  except IOError:
      pass

  print("disconnected")

  client_sock.close()
  server_sock.close()
  print("all done")

t = threading.Thread(target=server)
t.daemon = True
t.start()

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
    data = input()
    if len(data) == 0: break
    sock.send(data)

sock.close()
