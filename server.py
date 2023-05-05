import asyncio
import json
import websockets
import settings as cfg

clients = {}

# This function handles the connection and interaction with each client.
async def handle_client(websocket, path):
    clients[websocket] = {'nick': 'Guest'}
    print(f'Client connected: {websocket.remote_address}')
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f'Received message: {data}')
            if data['type'] == 'message':
                # Format the received message and broadcast it to other clients.
                message = f"<{clients[websocket]['nick']}> {data['content']}"
                await broadcast(message, websocket)
            elif data['type'] == 'nick':
                # Handle nickname changes.
                await change_nick(websocket, data['content'])
    except websockets.ConnectionClosed:
        print('Connection closed by client')
    finally:
        # Remove the client from the list when they disconnect.
        clients.pop(websocket, None)
        print(f'Client disconnected: {websocket.remote_address}')

# This function broadcasts a message to all connected clients except the sender.
async def broadcast(message, sender_websocket):
    sender_nick = clients[sender_websocket]['nick']
    formatted_message = f' {message}'
    print(f"Broadcasting message: {formatted_message}")
    for client_websocket in clients:
        if client_websocket is not sender_websocket:
            try:
                print(f"Sending message to client: {clients[client_websocket]['nick']}")
                await client_websocket.send(json.dumps({'type': 'message', 'content': formatted_message}))
            except websockets.ConnectionClosed:
                print("Error: Connection closed while trying to send message")

# This function handles nickname changes and informs other clients about the change.
async def change_nick(websocket, new_nick):
    old_nick = clients[websocket]['nick']
    clients[websocket]['nick'] = new_nick
    print(f'Changing nick: {old_nick} -> {new_nick}')
    await websocket.send(json.dumps({'type': 'info', 'content': f'You are now known as {new_nick}'}))
    await broadcast(f'{old_nick} is now known as {new_nick}', websocket)

# Start the WebSocket server and handle incoming client connections.
start_server = websockets.serve(handle_client, cfg.server, cfg.port, ping_timeout=cfg.ping_TimeOut, ping_interval=cfg.ping_Interval)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
