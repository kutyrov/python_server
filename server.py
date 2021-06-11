import asyncio

global_data = {}


def process_data(data):
    command, args = data.split(' ', 1)
    if command == 'put':
        name, value, time = args.split(' ', 2)
        try:
            value = float(value)
            time = int(time)
        except ValueError:
            resp = 'error\nwrong command\n\n'
            return resp
        if name not in global_data:
            global_data[name] = {}
        global_data[name][time] = value
        resp = 'ok\n\n'
        return resp
    if command == 'get':
        if len(args.split(' ')) != 1:
            resp = 'error\nwrong command\n\n'
            return resp
        if args == '*\n':
            resp = 'ok'
            for name in global_data:
                for key in global_data[name]:
                    resp += '\n' + name + ' ' + \
                        str(global_data[name][key]) + ' ' + str(key)
            resp += '\n\n'

        else:
            args = args.replace('\n', '')
            if args not in global_data:
                resp = 'ok\n\n'
            else:
                resp = 'ok'
                for key in global_data[args]:
                    resp += '\n' + args + ' ' + \
                        str(global_data[args][key]) + ' ' + str(key)
                resp += '\n\n'
        print("get", resp)
        return resp

    resp = 'error\nwrong command\n\n'
    return resp


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        # print("Connection made ", transport) # это неважно
        self.transport = transport

    def data_received(self, data):
        print("data received ", data)  # данные пришли
        resp = process_data(data.decode())  # обработали сформировари ответ
        self.transport.write(resp.encode())  # отправили


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
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


#run_server('127.0.0.1', 8888)
