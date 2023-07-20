import time
import traceback
from loguru import logger
from flask import request, Flask, send_file
import requests
import websockets
import asyncio
import json
import threading


app = Flask(__name__)
user_send_que = asyncio.Queue()
webclient_recv_que = asyncio.Queue()
websocket_chrome_client = set()
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

        async def clientRun():
            async with websockets.connect("ws://127.0.0.1:9999/user") as websocket:
                await websocket.send(json.dumps(info, separators=(',', ':')))
                return await websocket.recv()

        task = asyncio.ensure_future(clientRun())
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
        if path == '/chrome_client':
            logger.debug(f'there is an onOpen message: {message}, path: {path}')
            websocket_chrome_client.add(websocket)
            while 1:
                try:
                    await websocket.send(await user_send_que.get())
                    webclient_msg = await websocket.recv()
                    await webclient_recv_que.put(webclient_msg)
                    if webclient_msg == 'websocket_close':
                        logger.debug(websocket.id + ' close')
                        websocket_chrome_client.remove(websocket)
                        break
                except websockets.ConnectionClosed:
                    logger.debug("websocket_users old:" + str(websocket_chrome_client))
                    await webclient_recv_que.put('websocket something error, most possible is closed')
                    websocket_chrome_client.remove(websocket)
                    logger.debug("websocket_users new:" + str(websocket_chrome_client))
                    break
                except websockets.InvalidState:
                    traceback.print_exc()
                    await webclient_recv_que.put('websocket something error, most possible is InvalidState')
                    logger.debug("InvalidState...")  # 无效状态
                    break
                except Exception:
                    traceback.print_exc()

        elif path == '/user':
            if len(websocket_chrome_client) > 0:
                # logger.debug('que.empty():', user_send_que.empty())
                # logger.debug('que.full():', user_send_que.full())
                await user_send_que.put(message)
                return await websocket.send(await webclient_recv_que.get())
            await websocket.send('browser websocket not start.')



if __name__ == '__main__':
    threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 10000}).start()

    async def main():
        async with websockets.serve(handle, "127.0.0.1", 9999):
            await asyncio.Future()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
