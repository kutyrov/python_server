import asyncio


def process_data(data):
    return "123"


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        # print("Connection made ", transport) # это неважно
        self.transport = transport

    def data_received(self, data):
        print("data received ", data)  # данные пришли
        resp = process_data(data.decode())  # обработали сформировари ответ
        self.transport.write(resp.encode())  # отправили


loop = asyncio.get_event_loop()
coro = loop.create_server(
    ClientServerProtocol,
    '127.0.0.1', 8888
)

server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    #print('shut this beatiful server up')
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
