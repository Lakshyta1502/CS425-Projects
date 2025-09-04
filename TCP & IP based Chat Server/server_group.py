import socket
import threading

PORT = 12345
BUFFER_SIZE = 1024

clients = {}  # Dictionary to hold username to socket mapping
groups = {}   # Dictionary to hold group name to members mapping
lock = threading.Lock()  # Lock for thread safety

def load_users(filename='users.txt'):
    users = {}
    with open(filename, 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users[username] = password
    return users

def authenticate(username, password, users):
    return users.get(username) == password

def send_message(client_socket, message):
    client_socket.sendall(message.encode())

def handle_client(client_socket):
    username = None
    users = load_users()  # Load users from file

    # Authentication
    send_message(client_socket, "Enter username: ")
    username = client_socket.recv(BUFFER_SIZE).decode().strip()

    send_message(client_socket, "Enter password: ")
    password = client_socket.recv(BUFFER_SIZE).decode().strip()

    if authenticate(username, password, users):
        send_message(client_socket, "Welcome to the server.\n")
        with lock:
            clients[username] = client_socket
    else:
        send_message(client_socket, "Authentication failed.\n")
        client_socket.close()
        return

    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode().strip()
            if not message:
                break

            print(f"{username}: {message}")

            # Command handling
            if message.startswith("/msg"):
                parts = message.split(" ", 2)
                if len(parts) < 3:
                    send_message(client_socket, "Usage: /msg <username> <message>\n")
                    continue
                target_user = parts[1]
                msg = parts[2]
                with lock:
                    if target_user in clients:
                        send_message(clients[target_user], f"{username} (private): {msg}\n")
                    else:
                        send_message(client_socket, "User  not found.\n")
            elif message.startswith("/broadcast"):
                msg = message[len("/broadcast "):]
                with lock:
                    for client in clients.values():
                        send_message(client, f"{username} (broadcast): {msg}\n")
            elif message.startswith("/create_group"):
                group_name = message[len("/create_group "):].strip()
                if group_name:
                    with lock:
                        groups[group_name] = {username}
                    send_message(client_socket, f"Group {group_name} created.\n")
                else:
                    send_message(client_socket, "Please provide a group name.\n")
            elif message.startswith("/join_group"):
                group_name = message[len("/join_group "):].strip()
                with lock:
                    if group_name in groups:
                        groups[group_name].add(username)
                        send_message(client_socket, f"Joined group {group_name}.\n")
                    else:
                        send_message(client_socket, "Group not found.\n")
            elif message.startswith("/leave_group"):
                group_name = message[len("/leave_group "):].strip()
                with lock:
                    if group_name in groups:
                        groups[group_name].discard(username)
                        send_message(client_socket, f"Left group {group_name}.\n")
                    else:
                        send_message(client_socket, "Group not found.\n")
            elif message.startswith("/group_msg"):
                parts = message.split(" ", 3)
                if len(parts) < 3:
                    send_message(client_socket, "Usage: /group_msg <group_name> <message>\n")
                    continue
                group_name = parts[2]
                msg = parts[3] if len(parts) > 3 else ""
                with lock:
                    if group_name in groups:
                        for member in groups[group_name]:
                            if member in clients:
                                send_message(clients[member], f"{username} (group {group_name}): {msg}\n")
                    else:
                        send_message(client_socket, "Group not found.\n")
        except Exception as e:
            print(f"Error: {e}")
            break

    # Cleanup
    with lock:
        if username in clients:
            del clients[username]
    client_socket.close()
    print(f"{username} has disconnected.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", PORT))
    server_socket.listen(5)
    print(f"Server listening on port {PORT}")

    try:
        while True:
            client_socket, _ = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket,)).start()
    except KeyboardInterrupt:
        print("Shutting down the server.")
    finally:
        server_socket.close()
        print("Server closed.")

if __name__ == "__main__":
    main()