import socket
import os
import os.path
import sys
import time
import pickle
import threading


class ServerWeb(object):
    def __init__(self):  # initialize all the port and host
        self.host = ""
        port = input("Enter port number: ")
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def shutdown(self):
        # shutdown the socket in case an error was encountered
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            pass

    def start(self):
        # try to bind to the socket and report error if port is used
        try:
            print("starting server on {host} port: {port}".format(host=self.host, port=self.port))
            self.socket.bind((self.host, self.port))
        except Exception as e:
            print("Error encountered. Unable to bind to this port: {port}".format(port=self.port))
            self.shutdown()
            self.__init__()     # initializes all the variables
            self.start()    # starts the new connection
        self._listen()



    def forHeader(self, response_code):  # define all the possible error messages available
        header = ''
        if response_code == 200:
            header += 'HTTP/1.0 200 ok'
            header += '\r\n'
        elif response_code == 404:
            header += 'HTTP/1.0 404 Not Found'
            header += '\r\n\r\n'
        elif response_code == 400:
            header += 'HTTP/1.0 400 Bad Request'
            header += '\r\n\r\n'
        return header

    def _listen(self):  # listens for any data encountered from the client
        self.socket.listen(5)
        count = 0
        while True:
            (client, address) = self.socket.accept()
            count += 1
            print("Welcome new client. Connection served {count}".format(count=count))
            threading.Thread(target=self.forClient, args=(client, address)).start()  # creates a thread for the new
            # connection

    def forClient(self, client, address):
        size = 5024
        while True:
            data = client.recv(size).decode()  # decodes the data received
            if not data:
                break

            request_m = data.split(' ')[0]  # stores the method
            request_f = data.split(' ')[1]  # stores the filename
            if request_m == "GET" and (data.endswith('\r\n\r\n') == True):
                if request_f.startswith('/'):
                    request_f = "." + request_f

                # try open the file if it exists
                try:
                    file = open(request_f, 'rb')
                    response_d = file.read()
                    response_length = os.path.getsize(request_f)
                    file.close()
                    response_h = self.forHeader(200)
                    response_h += ('Content-Length: {fox}\r\n'.format(fox=response_length))
                    response_h += '\r\n'
                    response = response_h + response_d.decode()
                    response = response.encode()

                except Exception as e:
                    response_h = self.forHeader(404)
                    response = response_h.encode()
                client.send(response)
                client.close()
                break
            else:
                response_h = self.forHeader(400)
                response = response_h.encode()
                client.send(response)


if __name__ == '__main__':
    server = ServerWeb()
    server.start()
