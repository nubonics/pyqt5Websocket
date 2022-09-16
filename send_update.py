import websocket
from websocket import create_connection

ws = create_connection("ws://127.0.0.1:8000/ws/send_update")
print('sending hello world')
ws.send('page_number_1')
print('sent')
print('waiting for response')
result = ws.recv()
print(f'response: {result}')
ws.close(websocket.STATUS_PROTOCOL_ERROR)
