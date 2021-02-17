import re

from dependency_injector import containers, providers


def convert(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
