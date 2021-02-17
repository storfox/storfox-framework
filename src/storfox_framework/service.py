import typing


class Service(object):
    pass


__service: typing.List[Service] = []


def service(klass: Service) -> None:
    __service.append(klass)


def get_services() -> typing.List[typing.Any]:
    return __service
