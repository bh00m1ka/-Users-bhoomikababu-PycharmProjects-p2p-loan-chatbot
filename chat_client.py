import asyncio
import websockets
import json


async def chat():
    uri = "ws://localhost:8000/ws/chat"
    async with websockets.connect(uri) as websocket:
        print("Connected to chatbot.\nType 'exit' to quit.")

        while True:
            message = input("You: ")
            if message.lower() == "exit":
                break

            payload = {
                "message": message,
                "language": "fr"  # or "en", "es"
            }

            await websocket.send(json.dumps(payload))
            response = await websocket.recv()
            data = json.loads(response)
            print("Bot:", data["response"])


asyncio.run(chat())
