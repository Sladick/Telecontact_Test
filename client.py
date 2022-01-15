from Socket import Socket
from datetime import datetime
import asyncio
from os import system


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()

        self.messages = ""

    def set_up(self):
        try:
            self.socket.connect(("127.0.0.1", 2033))
        except ConnectionRefusedError:
            print("Server offline")
            exit(0)
        self.socket.setblocking(False)

    async def listen_socket(self, listened_socket=None):
        while True:
            data = await self.main_loop.sock_recv(self.socket, 2048)
            self.messages += f'{datetime.today().strftime("%H:%M")} : {data.decode("utf-8")}\n'
            system("cls")
            print(self.messages)

    async def send_data(self, data=None):
        while True:
            data = await self.main_loop.run_in_executor(None, input, "---->")
            await self.main_loop.sock_sendall(self.socket, data.encode("UTF-8"))

    async def main(self):
        await asyncio.gather(
            self.main_loop.create_task(self.listen_socket()),
            self.main_loop.create_task(self.send_data())
        )


if __name__ == '__main__':
    client = Client()
    client.set_up()

    client.start()