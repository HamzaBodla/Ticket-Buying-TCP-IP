import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())     # To get the local IP
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# global variables to be used later
name = None
ticket_type = None
ticket_a_quantity = None
ticket_c_quantity = None
day = None
total_cost = None

# allows clients to connect
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# tickets capped
def check_availability(conn):
    if int(ticket_a_quantity) > 20 or int(ticket_c_quantity) > 25:
        conn.send("Too many tickets, sorry not allowed".encode(FORMAT))

    # if int(ticket_a_quantity_act) > 20 or int(ticket_c_quantity_act) > 25:
    #     conn.send("Too many tickets, sorry not allowed".encode(FORMAT))

# calculate total cost
def calc_cost():
    global total_cost
    global ticket_type
    global ticket_c_quantity
    global ticket_a_quantity
    global day

    if ticket_type == 'VIP':
        total_cost = (int(ticket_a_quantity) * 50) + (int(ticket_c_quantity) * 25)

    elif day == 'Saturday':
        total_cost = (int(ticket_a_quantity) * 25) + (int(ticket_c_quantity) * 20)

    elif day == 'Sunday':
        total_cost = (int(ticket_a_quantity) * 10) + (int(ticket_c_quantity) * 7.5)

    else:
        total_cost = (int(ticket_a_quantity) * 30) + (int(ticket_c_quantity) * 22)


# check ticket type
def check_type(conn):
    global ticket_type

    if ticket_type != "VIP" and ticket_type != "STANDARD":
        conn.send("Wrong ticket type entered".encode(FORMAT))

    else:
        check_discount(conn)

# check for discount
def check_discount(conn):
    global total_cost

    if total_cost > 500:
        total_cost = total_cost - (total_cost * 0.1)
        conn.send(f"{name} your ticket for the festival booked and cost ${total_cost}, discount given".encode((FORMAT)))

    elif total_cost > 0 and total_cost <= 500:
        conn.send(f"{name} your ticket for the festival booked and cost ${total_cost}, discount not given".encode((FORMAT)))

    else:
        conn.send(f"You entered wrong amounts".encode(FORMAT))


# receive name from client
def user_name(conn):
    global name
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        name = conn.recv(msg_length).decode(FORMAT)

# receive ticket type from client
def tick_type(conn):
    global ticket_type
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        ticket_type = conn.recv(msg_length).decode(FORMAT)

# receive adult ticket quantity from client
def tick_a_quantity(conn):
    global ticket_a_quantity
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        ticket_a_quantity = conn.recv(msg_length).decode(FORMAT)

# receive child ticket quantity from client
def tick_c_quantity(conn):
    global ticket_c_quantity
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        ticket_c_quantity = conn.recv(msg_length).decode(FORMAT)

# receive the day selected from client
def which_day(conn):
    global day
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        day = conn.recv(msg_length).decode(FORMAT)

# start the server connection
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=new_handle_client, args=(conn, addr))
        thread.start()

# communication with client, sending messages and receiving them
def new_handle_client(conn, addr):

    connected = True
    while connected:
        conn.send("Hi there! Welcome to the Coventry Yearly Festival, Please make your booking".encode(FORMAT))

        conn.send("Your name : ".encode(FORMAT))
        user_name(conn)

        conn.send("Ticket type(VIP/Standard) : ".encode(FORMAT))
        tick_type(conn)

        conn.send("How many tickets for adults : ".encode(FORMAT))
        tick_a_quantity(conn)

        conn.send("How many tickets for children : ".encode(FORMAT))
        tick_c_quantity(conn)

        conn.send("Day : ".encode(FORMAT))
        which_day(conn)
        calc_cost()
        check_availability(conn)

        if ticket_type != "VIP" and ticket_type != "STANDARD":
            conn.send("Wrong ticket type entered".encode(FORMAT))

        else:
            check_discount(conn)


        connected = False


print("[STARTING] server is starting...")

start()
