import asyncio
import websockets
import base64
import os
import json

async def chat():
    uri = "ws://localhost:8000/chat"
    username = input("Enter username: ")

    async with websockets.connect(uri) as websocket:
        await websocket.send(username)

        print("Connected to chat server")
        print("Commands: /dm <user> <msg>, /send-file <user> <filepath>")
        loop = asyncio.get_event_loop()

        async def send():
            while True:
                msg = await loop.run_in_executor(None, input)
                
                # Handle file sending
                if msg.startswith("/send-file"):
                    parts = msg.split(" ", 2)
                    if len(parts) < 3:
                        print("Usage: /send-file <username> <filepath>")
                        continue
                    
                    target_user = parts[1]
                    filepath = parts[2]
                    
                    if not os.path.exists(filepath):
                        print(f"File not found: {filepath}")
                        continue
                    
                    try:
                        with open(filepath, "rb") as f:
                            file_data = f.read()
                        
                        filename = os.path.basename(filepath)
                        encoded_data = base64.b64encode(file_data).decode('utf-8')
                        
                        file_msg = {
                            "type": "file",
                            "target": target_user,
                            "filename": filename,
                            "data": encoded_data
                        }
                        
                        await websocket.send(json.dumps(file_msg))
                        print(f"File '{filename}' sent to {target_user}")
                    except Exception as e:
                        print(f"Error sending file: {e}")
                else:
                    await websocket.send(msg)

        async def receive():
            while True:
                msg = await websocket.recv()
                
                try:
                    data = json.loads(msg)
                    if data.get("type") == "file":
                        filename = data.get("filename")
                        file_data = base64.b64decode(data.get("data", ""))
                        from_user = data.get("from")
                        
                        # Save received file locally
                        os.makedirs("received_files", exist_ok=True)
                        filepath = os.path.join("received_files", f"{from_user}_{filename}")
                        with open(filepath, "wb") as f:
                            f.write(file_data)
                        
                        print(f"\n[File received from {from_user}]: {filename} saved to {filepath}")
                        print("> ", end="", flush=True)
                    else:
                        print(msg)
                except json.JSONDecodeError:
                    print(msg)

        await asyncio.gather(send(), receive())

asyncio.run(chat())