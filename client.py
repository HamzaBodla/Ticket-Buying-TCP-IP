import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())     # getting local ip
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# send messages/info to server
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

# communication with server
def make_booking():
    print(client.recv(2048).decode(FORMAT))     # receive and print message from server
    print(client.recv(2048).decode(FORMAT))
    name = input()
    send(name)

    # send ticket type info
    print(client.recv(2048).decode(FORMAT))
    tick_type = input()
    tick_type = tick_type.upper()
    send(tick_type)

    # send adult ticket quantity info
    print(client.recv(2048).decode(FORMAT))
    tick_a_quantity = input()
    send(tick_a_quantity)

    # send children ticket quantity info
    print(client.recv(2048).decode(FORMAT))
    tick_c_quantity = input()
    send(tick_c_quantity)

    # send day selected info
    print(client.recv(2048).decode(FORMAT))
    day = input()
    day.capitalize()
    send(day)


    print(client.recv(2048).decode(FORMAT))


make_booking()

send(DISCONNECT_MESSAGE)    # disconnect from the server
