import asyncio
import websockets

async def send_gaze(websocket):  
    await asyncio.sleep(1)
    await websocket.send("fill:name:John Doe")
    await asyncio.sleep(1)
    await websocket.send("fill:email:john@example.com")
    await asyncio.sleep(1)
    await websocket.send("submit")

async def main():
    async with websockets.serve(send_gaze, "localhost", 5678):
        print("WebSocket server started on ws://localhost:5678")
        await asyncio.Future()  
asyncio.run(main())
