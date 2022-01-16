from Socket import Socket
from datetime import datetime, timedelta
from socket import SHUT_RDWR


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        self.users = []

    def set_up(self):
        self.socket.bind(("127.0.0.1", 2033))
        self.socket.listen(4)  # возможность подключение 4 человек одновременно
        self.socket.setblocking(False)
        print('Server is listening')

    async def send_data(self, data=None, listened_socket=None):
        for user in self.users:
            if user != listened_socket: # дублирование сообщения всем подключенным клиентам (кроме отправителя)
                await self.main_loop.sock_sendall(user, data)

    async def listen_socket(self, listened_socket=None, start_time=None):
        if not listened_socket:
            return

        while True:
            try:
                data = await self.main_loop.sock_recv(listened_socket, 2048)
                await self.send_data(data, listened_socket)
                print(f'{datetime.today().strftime("%H:%M")} : {data.decode("utf-8")}')
                if datetime.now() - start_time > timedelta(seconds=30):  # разрыв соединения если от клиента нет
                    self.users.remove(listened_socket)  # сообщений более 30 секунд
                    listened_socket.shutdown(SHUT_RDWR)
                    listened_socket.close()
                    return
                start_time = datetime.now()
            except ConnectionResetError:
                print("Client removed")
                self.users.remove(listened_socket)
                return

    async def accept_sockets(self):
        while True:
            user_socket, address = await self.main_loop.sock_accept(self.socket)
            print(f"User {address[0]} connected")
            self.users.append(user_socket)
            start_time = datetime.now()
            self.main_loop.create_task(self.listen_socket(user_socket, start_time))

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())


if __name__ == '__main__':
    server = Server()
    server.set_up()

    server.start()
