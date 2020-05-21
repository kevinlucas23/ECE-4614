import socket
import sys

size = 5024
# try to connect to the server and report and error if it can't
try:
    clientS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = input("Please enter the server host and port number: ").split()
    clientS.connect((host, int(port)))
except socket.error as message:
    if clientS:
        print("Unable to open the socket: " + str(message))
        sys.exit(1)

filename = input("Enter file name to server: ")

if filename.startswith('/'):  # checks what does the filename start
    filename = filename[1:]

# gets the complete html request
request_f = "GET /" + filename + " HTTP/1.0\r\n\r\n"
clientS.sendall(request_f.encode())

lucas = ''
while True:
    data = clientS.recv(size)
    if len(data) <= 0:
        break
    lucas += data.decode()
clientS.close()
cnt = 1

# gets each line from the file requested
for line in lucas.splitlines():
    if len(line) == 0:
        break
    cnt += 1

gone = lucas.splitlines()[:cnt]
respond_he = ''
for i in gone:
    respond_he += i + '\n'
print(respond_he)

res = lucas.split(' ')[1]

duo = lucas.splitlines()[cnt:]  # gets the file content
cat = ''
for i in duo:
    cat += i + '\n'

# checks the status line to see if it encountered and errror
if res == '400' or res == '404':
    pass
else:  # if the server send an error it doesn't create the file
    f = open(filename, 'w+')
    f.write(cat)
    f.close()
