import time
import traceback
from loguru import logger
from flask import request, Flask, send_file
import requests
import websockets
import asyncio
import json
import threading
import uuid


app = Flask(__name__)
websocket_chrome_client = set()
socket_map = {}
repeat_time = 0
proxy_lock = threading.Lock()


@app.route('/proxy', methods=['GET', 'POST'])
def proxy():
    """SwitchyOmega2.5.20 will send twice request bug?  And SwitchyOmega2.5.21 fix this bug"""
    global repeat_time, proxy_lock
    with proxy_lock:
        if time.time() - repeat_time > 2:
            proxy = requests.get('http://192.168.20.205:13025/get_qg_ip', timeout=30).text  # proxy = '120.111.12.18:8888'
            text = """function FindProxyForURL(url, host) {return "PROXY %s"}""" % proxy
            with open('proxy.pac', "w", encoding='utf-8') as f:
                f.write(text)
    repeat_time = time.time()
    return send_file('proxy.pac')


@app.route('/transpond', methods=['GET', 'POST'])
def transpond():
    try:
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        info = {
            'params': dict(request.args),
            'method': request.method.upper(),
            'data': None,
            'headers': dict(request.headers),
            'cookies': dict(request.cookies),
        }
        if request.method.upper() == 'POST':
            info['data'] = request.json

        async def client_run():
            async with websockets.connect("ws://127.0.0.1:9999/user") as ws:
                await ws.send(json.dumps(info, separators=(',', ':')))
                return await ws.recv()

        task = asyncio.ensure_future(client_run())
        asyncio.get_event_loop().run_until_complete(asyncio.wait([task]))
        message = task.result()
        logger.debug(message)
        return json.dumps({"message": message})
    except:
        traceback.print_exc()
        return "启动接口失败."


async def handle(websocket, path):
    async for message in websocket:
        # logger.debug(path, message)
        logger.debug(f"recv {websocket} , {path}")
        if path == '/chrome_client':
            logger.debug(f'there is an message: {message}, path: {path}')
            if message.endswith('hello1'):
                websocket_chrome_client.add(websocket)      # first on open send
            else:
                uuid4, info = message.split('|||', 1)
                client_socket = socket_map.pop(uuid4)
                await client_socket.send(info)

        elif path == '/user':
            for chrome_client in websocket_chrome_client:       # todo for in remove will cause an error
                                                                # todo websocket_chrome_client should be a class, its init function accept href, its inner maintains many chrome clients
                try:
                    uuid4 = str(uuid.uuid4())
                    await chrome_client.send(f'{uuid4}|||'+message)
                    socket_map[uuid4] = websocket
                    break
                except websockets.ConnectionClosed:
                    logger.debug("websocket_users old:" + str(websocket_chrome_client))
                    websocket_chrome_client.remove(chrome_client)
                    logger.debug("websocket_users new:" + str(websocket_chrome_client))
                    break
                except websockets.InvalidState:
                    traceback.print_exc()
                    logger.debug("InvalidState...")  # 无效状态
                    break
                except Exception:
                    logger.debug('cannot call recv while another coroutine is already waiting for the next message')
                    # traceback.print_exc()
            else:
                await websocket.send('browser websocket not start.')




if __name__ == '__main__':
    threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 10000}).start()

    async def main():
        async with websockets.serve(handle, "127.0.0.1", 9999):
            await asyncio.Future()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
