import socket               # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   try:
      c, addr = s.accept()     # Establish connection with client.
      print('Got connection from', addr)
      output = 'Thank you for connecting'
      c.sendall(output.encode('utf-8'))
      data = c.recv(12345).decode()
      print('Recieved: ', data, " from client")
      if(data == 'What Up'):
         c.sendall('Hey Dude'.encode('utf-8'))
      elif(data == 'disconnect'):
         c.shutdown(socket.SHUT_RDWR)
         c.close()
         break
      else:
         print('Invalid data')
   except socket.error:
      print("An error has occurred... closing connection to client")
   finally:
      c.shutdown(socket.SHUT_RDWR)
      c.close()
