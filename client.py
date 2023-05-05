import asyncio
import json
import websockets
from concurrent.futures import ThreadPoolExecutor
import settings as cfg

# This function manages the main loop for the client, allowing it to send and receive messages.
async def irc_client():
    async with websockets.connect(f'ws://{cfg.server}:{cfg.port}') as websocket:
        # Start the background task to receive messages from the server.
        recv_task = asyncio.create_task(receive_messages(websocket))

        with ThreadPoolExecutor() as executor:
            while True:
                # Read user input in a non-blocking manner.
                message = await asyncio.get_event_loop().run_in_executor(executor, input, '')
                if message.startswith('/'):  # Check if the input is a command.
                    await handle_command(websocket, message)  # Handle the command.
                else:
                    # Send the message to the server as a regular chat message.
                    await websocket.send(json.dumps({'type': 'message', 'content': message}))

        # Cancel the receive_messages task when the main loop ends.
        recv_task.cancel()

# This function handles incoming messages from the server.
async def receive_messages(websocket):
    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            if data['type'] == 'message':
                print(f"{data['content']}")
        except websockets.ConnectionClosed:
            print("Connection closed by the server")
            break

# This function processes user commands and sends them to the server.
async def handle_command(websocket, command):
    cmd_parts = command.split(' ', 1)
    cmd_name = cmd_parts[0].lower()
    cmd_args = cmd_parts[1] if len(cmd_parts) > 1 else ''

    if cmd_name == '/nick':
        if cmd_args:
            # Send the nickname change command to the server.
            await websocket.send(json.dumps({'type': 'nick', 'content': cmd_args}))
        else:
            print('Error: Please provide a nickname')

# Connect to the WebSocket server and start the main client loop.
# Make sure to replace 'localhost' and '8080' in settings.py with the appropriate IP address and port number, if you're intending to run in a web facing environment.
asyncio.get_event_loop().run_until_complete(irc_client())
