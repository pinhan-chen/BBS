# BBS (Bulletin Board System)

This is the final project of Fall 2020 Network Programming in National Chiao Tung University. The system supports multi-user registration, login, posting messages, and creating/joining chatrooms. It uses both TCP and UDP protocols for communication.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Server](#running-the-server)
  - [Running the Client](#running-the-client)
  - [Commands](#commands)
    - [Registration and Login](#registration-and-login)
    - [User and Chatroom Management](#user-and-chatroom-management)
    - [Post Management](#post-management)
- [Contributing](#contributing)
- [License](#license)

## Features
- User registration and login
- Create, read, update, and delete posts
- Create and join chatrooms
- List users and chatrooms
- TCP and UDP communication

## Requirements
- Python 3.x
- `argparse` module (usually included with Python)
- `socket` module (usually included with Python)

## Installation
1. Clone the repository:
```sh
    git clone https://github.com/pinhan-chen/BBS.git
    cd BBS
```

## Usage
### Running the Server
1. Navigate to the directory containing the server file.

2. Run the server:
    ```sh
        python server.py [port]
    ```
    - Replace [port] with the desired port number. If not specified, the default port is 8000.

### Running the Client
1. Navigate to the directory containing the client file.

2. Run the client:
    ```sh
    python client.py [host] [port]
    ```
    - Replace [host] with the server's IP address. If not specified, the default is 127.0.0.1.
    - Replace [port] with the server's port number. If not specified, the default is 8000.

### Commands
The client supports several commands that can be entered after connecting to the server.

### Registration and Login
- Register a new user:

    ```sh
        register <username> <email> <password>
    ```
- Login:
    ```
        login <username> <password>
    ```
- Logout:
    ```
        logout
    ```

### User and Chatroom Management
- List all users:
    ```
        list-user
    ```
- Create a chatroom:
    ```
        create-chatroom <port>
    ```
- Join a chatroom:
    ```
        join-chatroom <chatroom_name>
    ```
- Restart a chatroom:
    ```
        restart-chatroom
    ```
- Leave a chatroom:
    ```
        leave-chatroom
    ```
- Attach to a chatroom:
    ```
        attach
    ```
- Detach from a chatroom:
    ```
        detach
    ```

### Post Management
- Create a chatroom:
    ```
        create-chatroom <port>
    ```
- Join a chatroom:
    ```
        join-chatroom <chatroom_name>
    ```
- Restart a chatroom:
```
    restart-chatroom
```
- Leave a chatroom:
    ```
        leave-chatroom
    ```

### Post Management
- Create a board:
    ```
        create-board <board_name>
    ```
- List all boards:
    ```
        list-board
    ```
- Create a post:
    ```
        create-post <board_name> --title <title> --content <content>
    ```
- List all posts in a board:
    ```
        list-post <board_name>
    ```
- Read a post:
    ```
        read <post_id>
    ```
- Delete a post:
    ```
        delete-post <post_id>
    ```
- Update a post:
    ```
        update-post <post_id> --title <new_title>
        update-post <post_id> --content <new_content>
    ```
- Comment on a post:
    ```
        comment <post_id> <comment>
    ```



## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

