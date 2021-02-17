import typing
import asyncio
from grpclib.utils import graceful_exit
from grpclib.server import Server


def run_forever(handlers: typing.List[typing.Any], host, port):
    async def start():
        server = Server(handlers)

        with graceful_exit([server]):
            await server.start(host, port)
            print(f"Serving on {host}:{port}")
            await server.wait_closed()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
