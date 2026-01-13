# Real-Time Chat Server (WebSocket-Based)

A backend-focused real-time chat server built using **Python** and **FastAPI WebSockets**.
The system supports **public chat**, **private direct messages (DMs)**, and **offline message
delivery** with correct server-side timestamping.

This project focuses on backend engineering concepts such as real-time communication,
async concurrency, message routing, and state management rather than UI or frontend work.

---

## Features

### Public Chat
- All connected users can send messages to a shared public chat
- Messages are broadcast in real time using WebSockets

### Private Messaging (DM)
- Users can send private messages using:
  ```
  /dm <username> <message>
  ```
- Messages are routed by the server
- Clients never communicate directly with each other

### Offline Message Support
- If a user is offline, private messages are stored in a per-user queue
- When the user reconnects:
  - All queued messages are delivered in FIFO order
  - Original timestamps are preserved

### Server-Side Timestamps
- Timestamps are generated once, at message creation time
- All timestamps use UTC
- Offline message delivery reuses stored timestamps

### Asynchronous Concurrency
- Built using async/await
- Handles multiple concurrent WebSocket connections
- Avoids blocking I/O

---

## Architecture Overview

Client (CLI)
   |
WebSocket (TCP)
   |
FastAPI Server
   |
In-Memory State

---

## Core Data Structures

```python
users = {
    "username": websocket
}

msg_queue = {
    "offline_user": [
        {
            "from": "sender",
            "text": "message",
            "timestamp": "ISO-UTC"
        }
    ]
}
```

---

## Message Flow

Public Message:
Client -> Server -> All connected clients

Private Message (Online):
Sender -> Server -> Target user

Private Message (Offline):
Sender -> Server -> Offline Queue
User reconnects -> Server -> Deliver queued messages

---

## Tech Stack

- Python 3.10+
- FastAPI
- WebSockets
- asyncio

---

## Setup & Run

Install dependencies:
```
pip install fastapi uvicorn websockets
```

Start the server:
```
uvicorn server:app --reload
```

Server runs at:
ws://localhost:8000/chat

Start a client:
```
python client.py
```

Open multiple terminals to simulate multiple users.

---

## Limitations

- In-memory storage only
- Messages are lost if the server restarts
- Single-server architecture
- No authentication or encryption

---
-
