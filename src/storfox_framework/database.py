from typing import Optional
from ssl import SSLContext, create_default_context
from sqlalchemy.engine.url import URL

from .configuration import conf


def get_bind() -> URL:
    """Generate a url for db connection."""
    return URL(
        drivername=conf.DATABASE.get("DRIVER", "postgresql"),
        host=conf.DATABASE.get("HOST", "localhost"),
        port=conf.DATABASE.get("PORT", 5432),
        database=conf.DATABASE.get("NAME", "postgres"),
        username=conf.DATABASE.get("USER", "postgres"),
        password=conf.DATABASE.get("PASSWORD", ""),
    )


def get_ssl() -> Optional[SSLContext]:
    """Return ssl_object"""
    ssl_enable = conf.DATABASE.get("SSL", False)

    if ssl_enable:
        return create_default_context(cadata=conf.DATABASE["CA_CERT"])

    return None
