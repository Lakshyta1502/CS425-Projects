import socket
import threading

BUFFER_SIZE = 1024

def handle_server_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode()
            if not message:
                print("Disconnected from server.")
                break
            print(message)
        except Exception as e:
            print(f"Error: {e}")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(('127.0.0.1', 12345))
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return

    print("Connected to the server.")

    # Authentication
    username_prompt = client_socket.recv(BUFFER_SIZE).decode()
    username = input(username_prompt)
    client_socket.sendall(username.encode())

    password_prompt = client_socket.recv(BUFFER_SIZE).decode()
    password = input(password_prompt)
    client_socket.sendall(password.encode())

    response = client_socket.recv(BUFFER_SIZE).decode()
    print(response)

    if "Authentication failed" in response:
        client_socket.close()
        return

    # Start thread for receiving messages from the server
    receive_thread = threading.Thread(target=handle_server_messages, args=(client_socket,))
    receive_thread.daemon = True  # Allows the program to exit even if this thread is running
    receive_thread.start()

    # Send messages to the server
    while True:
        message = input()
        if message:
            client_socket.sendall(message.encode())
            if message == "/exit":
                print("Exiting...")
                client_socket.close()
                break

if __name__ == "__main__":
    main()
