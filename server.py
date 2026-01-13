from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime,timezone
app = FastAPI()

users = {}  # username -> websocket
msg_queue = {}

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    
    try:
        # first message = username
        username = await websocket.receive_text()

        if username in users:
            await websocket.send_text("Username already taken")
            await websocket.close()
            return

        users[username] = websocket

        if username in msg_queue:
            for msg in msg_queue[username]:
                await websocket.send_text(
                    f"[{msg['timestamp']}][Offline from {msg['from']}]: {msg['text']}"
                )
            del msg_queue[username]
        # notify others
        for user, ws in users.items():
            if ws != websocket:
                await ws.send_text(f"{username} joined")

        while True:
            message = await websocket.receive_text()
            timestamp = datetime.now().strftime("%H:%M")

            # PRIVATE MESSAGE
            if message.startswith("/dm"):
                parts = message.split(" ", 2)

                if len(parts) < 3:
                    await websocket.send_text("Usage: /dm <username> <message>")
                    continue

                target, text = parts[1], parts[2]

                if target in users:
                    await users[target].send_text(
                        f"[{timestamp}][DM from {username}]: {text}"
                    )
                else:
                    if target not in msg_queue:
                        msg_queue[target]=[]
                    msg_queue[target].append({
                            "from":username,
                            "text":text,
                            "timestamp":timestamp
                    })
                    print(msg_queue)
                    await websocket.send_text(
                        f"User '{target}' is not online"
                        
                    )

            # PUBLIC MESSAGE
            else:
                full_msg = f"[{timestamp}][{username}]: {message}"
                for ws in users.values():
                    await ws.send_text(full_msg)
                    
    except WebSocketDisconnect:
        users.pop(username, None)

        for ws in users.values():
            await ws.send_text(f"{username} left")
