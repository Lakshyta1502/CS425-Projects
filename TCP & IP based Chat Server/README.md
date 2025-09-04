# Chat Server Implementation

## Introduction

This project implements a multi-threaded chat server that supports private messaging, group communication, and user authentication using Python's socket programming and threading.

## Features

- **User Authentication**: Users must provide valid credentials from `users.txt`.
- **Private Messaging**: Send messages to specific users using `/msg <username> <message>`.
- **Broadcast Messaging**: Broadcast messages to all connected users using `/broadcast <message>`.
- **Group Management**:
  - Create a group using `/create_group <group_name>`.
  - Join a group using `/join_group <group_name>`.
  - Send group messages using `/group_msg <group_name> <message>`.
  - Leave a group using `/leave_group <group_name>`.
- **Concurrent Connections**: The server handles multiple clients simultaneously using threads.

## Installation and Setup

### Prerequisites

Ensure Python is installed on your system.

### Running the Server

1. Open a terminal and navigate to the project directory.
2. Run the server using:
   ```sh
   python server_group.py
   ```
3. The server will start listening for client connections on port 12345.

### Running the Client

1. Open a new terminal.
2. Start the client using:
   ```sh
   python client_group.py
   ```
3. Enter your username and password when prompted.
4. Use the supported commands to communicate.

## How the Code Works

### Server (`server_group.py`)

1. **Starting the Server**:

   - The server starts by binding to a specified port and listens for incoming connections.
   - It runs in an infinite loop, accepting client connections and creating a new thread for each connected client.

2. **User Authentication**:

   - When a client connects, the server prompts for a username and password.
   - The server checks the credentials against `users.txt` and allows or denies access.

3. **Handling Clients**:

   - Each client runs on a separate thread.
   - The server continuously listens for messages from clients and processes them accordingly.

4. **Message Processing**:

   - Private messages are sent using `/msg <username> <message>`.
   - Broadcast messages are relayed to all users using `/broadcast <message>`.
   - Group management commands allow users to create, join, leave, and send messages to groups.
   - Thread-safe mechanisms (`threading.Lock`) ensure data consistency while modifying client and group lists.

5. **Disconnection Handling**:
   - When a client disconnects, the server removes the user from active client lists.
   - The connection socket is closed to free system resources.

### Client (`client_group.py`)

1. **Connecting to the Server**:

   - The client establishes a connection to the server using `socket.connect()`.
   - It sends login credentials and waits for authentication.

2. **Receiving Messages**:

   - A separate thread listens for messages from the server and prints them to the console.

3. **Sending Messages**:

   - The user inputs messages, which are sent to the server via the socket.
   - Commands such as `/msg`, `/broadcast`, `/group_msg` are interpreted and relayed accordingly.

4. **Exiting the Client**:
   - If the user types `/exit`, the client disconnects and closes the socket connection.

## Testing Methodology

### Correctness Testing

To ensure the server functions correctly, we tested:

- **User Authentication**: Verified that valid users can log in, and invalid users are rejected.
- **Messaging System**: Sent private messages, broadcast messages, and group messages to confirm they reach the correct recipients.
- **Command Handling**: Tested all supported commands to ensure they behave as expected.
- **Client Disconnection Handling**: Verified that users who disconnect are properly removed from active lists.

### Stress Testing

To evaluate the server’s ability to handle multiple clients:

- **Concurrent Clients**: Simulated multiple clients connecting simultaneously and exchanging messages.
- **Rapid Message Exchange**: Sent messages in quick succession to check for lag, dropped messages, or crashes.
- **Extended Load Test**: Kept clients connected for an extended period while continuously sending and receiving messages.

The server successfully handled multiple concurrent connections and sustained message exchange under load without crashes or significant delays.

## Conclusion

This chat server effectively manages user authentication, private messaging, group chats, and concurrent connections. The testing confirmed its stability and correctness under normal and high-load conditions.
