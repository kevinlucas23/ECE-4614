
Version: 3.8.1

Operating System: Windows 10
 
Description and Implementation:

The aim of this project was to design and implement a simplified version of an HTTP client and server program using sockets programming without the help of build in classes like HttpURLConnection class and the code can be written in any programming language. For this project I used python to code this webserver program. To implement this project, it was divided into two parts: client and server side.
a)	Server:

For this server side, I ask the user on which port number he wants to run the server. The server tries to bind to that port and check if the port is used. If it is, it queries the user for a new port number. The server is started on the port number and awaits the client connection. The server gets the data received from the server and decodes it. It checks if the data has the correct HTTP request message which is GET file HTTP/1.0\r\n\r\n. if it does, the server open the file path and get the content of the file. It sends back the content of the file using the correct HTTP response message which is:
HTTP/1.0 200 OK

Content-Length: size of the file in bytes



File content below.

If the file doesn’t exist on the server, it sends a 404 Not Found HTTP response message. If the HTTP request message is incorrect, it sends a 400 Bad Request to the client. After sending all the data to the client, it
closes the connection with the client and awaits a new connection from the client on the same port number.
 
b)	Client:

For the server side, the client queries the user for the server port number and host. The client tries to connect to the host and port number given. If an error occurs, the client shutdown and returns an error. If the client was able to connect the server, the client asks the user for the filename he wants to access on the server. The client gets the response and sends it in the correct HTTP request message format which is GET filename HTTP/1.0\r\n\r\n. The client awaits the response from the server. It checks if the response contains a Bad Request or Not Found. If it does, the client prints out the data. If it doesn’t the client creates a file locally and save the file content on the user local and closes the connection.