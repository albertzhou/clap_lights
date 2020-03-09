import socket
import time
import json

# send message to designated IP and port, python is the client, IPDU is the server
# message options (send string to IPDU to perform command)
# analog_update - requests raw analog values
def send_message(IP, Port, Msg):
	TCP_IP = IP # IP in String form
	TCP_PORT = Port # Port in int form, defined here
	MESSAGE = Msg

	print("TCP target IP: " + TCP_IP)
	print("TCP target port: " + str(TCP_PORT))
	print("message: " + MESSAGE)

	# send message
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(MESSAGE)

	# receive message
	data = process_crlf(s, "\r\n")
	s.close()

def receive_message(IP, Port): # update this to work without sending random byte
	TCP_IP = IP # IP in String form
	TCP_PORT = Port # Port in int form, defined here

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send("a")
	data = process_crlf(s, "\r\n")
	print("Received data: " + data)
	s.close

# called in send_message
def process_crlf(s, crlf):
	data = ""
	while data[-len(crlf):] != crlf: # check if the end of "data" is crlf, if not continue parsing
		data += s.recv(1)
	return data

if __name__ == '__main__':
	send_message(IPDU_IP, IPDU_Port, "analog_update")
	# receive_message(IPDU_IP, IPDU_Port)
