import socket
import threading
import datetime

# Connection information
ip = "10.36.19.153"
port = 55555

# Start the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((ip, port))
except socket.error as e:
    str(e)
server.listen()
print("Waiting for a connection, Server Started")

# Variables
clients = []
usernames = []
admin = []
numClients = 0


# Sending a message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Handling messages from clients
def handle(client):
    message = None
    while True:
        try:
            # Broadcast the message
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing clients
            try:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                username = usernames[index]
                broadcast('{} left.'.format(username).encode('ascii'))
                usernames.remove(username)
            except:
                pass
            break

        # Check if admin is kicking client
        message = message.decode('ascii')
        if 'kick' in message and client == admin[0]:
            for i in range(1, len(usernames)):
                if usernames[i] in message:
                    kclient = clients[i]
                    clients.remove(kclient)
                    kclient.close()
                    username = usernames[i]
                    broadcast('{} has been kicked'.format(username).encode('ascii'))
                    usernames.remove(username)
        elif 'kick' in message and client != admin[0]:
            index = clients.index(client)
            username = usernames[index]
            broadcast('{} you do not have permission to do that'.format(username).encode('ascii'))


# Receiving function
def receive():
    numClients = 0
    while True:
        # Accept connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Store username
        client.send('USER'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        # Add datetime
        date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Print and broadcast username
        print("Username is {}".format(username))
        broadcast("{} has joined the chat ".format(username).encode('ascii'))
        broadcast("{} ".format(date_time).encode('ascii'))

        # If first client to join, make them admin, then add one to numClients
        if numClients == 0:
            admin.append(client)
        numClients = numClients + 1

        # Start thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# Start receiving function to accept new clients
receive()
