import typing
from sqlalchemy.sql import ClauseElement  # type: ignore
from databases import Database


class Repository(object):
    database: Database

    def __init__(self, database: Database):
        self.database = database

    async def fetch_all(
        self, query: typing.Union[ClauseElement, str], values: dict = None
    ) -> typing.List[typing.Mapping]:
        return await self.database.fetch_all(query=query, values=values)

    async def fetch_one(
        self, query: typing.Union[ClauseElement, str], values: dict = None
    ) -> typing.Optional[typing.Mapping]:
        return await self.database.fetch_one(query=query, values=values)

    async def fetch_val(
        self,
        query: typing.Union[ClauseElement, str],
        values: dict = None,
        column: typing.Any = 0,
    ) -> typing.Any:
        return await self.database.fetch_val(query=query, values=values, column=column)

    async def execute(self, query: typing.Union[ClauseElement, str], values: dict = None):
        return await self.database.execute(query=query, values=values)

    async def execute_many(
        self, query: typing.Union[ClauseElement, str], values: list
    ) -> None:
        return await self.database.execute_many(query=query, values=values)

    async def iterate(
        self, query: typing.Union[ClauseElement, str], values: dict = None
    ) -> typing.AsyncGenerator[typing.Mapping, None]:
        async for record in self.database.iterate(query=query, values=values):
            yield record

    async def transaction(self, force_rollback: bool = False, **kwargs: typing.Any):
        return await self.transaction(force_rollback=force_rollback, **kwargs)
