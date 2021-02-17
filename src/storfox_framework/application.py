from typing import Collection, Optional
from grpclib._typing import IServable

from .grpc import run_forever
from .configuration import config_vars
from .container import Container


current_app: 'Storfox'


class Storfox(object):
    """
    Creates an application instance
    **Parameters:**

    * **debug** - Boolean indicating if debug tracebacks should be returned on errors.
    * **handlers** - List of grpc handlers.
    * **handlers** - List of grpc handlers.

    """
    handlers: Optional[Collection['IServable']]
    debug: bool
    container: Container

    def __init__(
        self,
        handlers: Optional[Collection['IServable']] = None,
        debug: bool = False
    ) -> None:
        self.handlers = handlers
        self.debug = debug

    def __new__(cls, *args, **kwargs):
        global current_app
        instance = object.__new__(cls)
        current_app = instance

        return instance

    def run(self, host: str = '127.0.0.1', port: int = 50051):
        run_forever(self.handlers, host=host, port=port)


def create_app(
    handlers: Collection['IServable'],
    container: Container = None
) -> Storfox:
    if not container:
        container = Container()
        container.config.from_dict(config_vars())

    app = Storfox(handlers)
    app.container = container

    return app
