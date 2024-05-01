import socket
import threading
import datetime
from colorama import Fore, init, Style
# Choosing a username
username = input("Choose your username: ")

# Choose a color
color = input("Choose your color (R, B, G, W): ")

# Connecting to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("10.36.19.153", 55555))

while True:
    if color == 'R':
        color = Fore.RED
    elif color == 'B':
        color = Fore.BLUE
    elif color == 'G':
        color = Fore.GREEN
    else:
        color = Fore.WHITE
    break



# Listening to the server and sending the username
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'USER':
                client.send(username.encode('ascii'))
            else:
                print_with_color(s=message, color=color)
        except:
            # Close connection since there is an error
            print("An error occurred!")
            client.close()
            break



# Sending messages to the server
def write():
    while True:
        try:
            # Add datetime
            date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = '{} {}: {}'.format(username, [date_time], input(''))
            client.send(message.encode('ascii'))
        except:
            pass

def print_with_color(s, color):
    """Utility function wrapping the regular print() function
    but with colors and brightness"""
    print(f"{color}{s}{Style.RESET_ALL}")

    
# Start threads for listening and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()