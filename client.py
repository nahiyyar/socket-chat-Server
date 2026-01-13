import asyncio
import websockets

async def chat():
    uri = "ws://localhost:8000/chat"
    username = input("Enter username: ")

    async with websockets.connect(uri) as websocket:
        await websocket.send(username)

        print("Connected to chat server")
        loop = asyncio.get_event_loop()

        async def send():
            while True:
                msg = await loop.run_in_executor(None, input)
                await websocket.send(msg)

        async def receive():
            while True:
                msg = await websocket.recv()
                print(msg)

        await asyncio.gather(send(), receive())

asyncio.run(chat())
