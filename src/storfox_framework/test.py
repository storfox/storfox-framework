import os
import json
import asyncio
from typing import List

import pytest


async def update_sequence(db) -> None:
    for table_name, table in db.tables.items():
        if table.c.id.autoincrement:
            query = (
                f"SELECT SETVAL('{table_name}_id_seq', "
                f"(SELECT COALESCE(MAX(id), 1) FROM \"{table_name}\"))"
            )
            await db.status(query)


async def clear_tables(db):
    for table_name, table in db.tables.items():
        query = f"TRUNCATE \"{table_name}\" CASCADE"
        await db.status(query)


async def insert_fixtures(db, fixtures):
    for fixture in fixtures:
        file = open(os.path.join(self.fixture_path, fixture), "r")
        data = json.load(file)
        for datum in data:
            columns = ",".join(map(lambda x: f'"{x}"', datum["fields"].keys()))
            values = ",".join(map(_str_caster, datum["fields"].values()))
            query = """insert into "{}"({}) values ({})""".format(datum['table'], columns, values)
            await db.status(query)


def _dict_to_db_dict(data: dict):
    dict_values = []
    for field, value in data.items():
        if isinstance(value, str):
            dict_values.append(f'"{field}": "{value}"')
        elif isinstance(value, list):
            dict_values.append(f'"{field}": {_list_to_db_list(value)}')
        elif isinstance(value, dict):
            dict_values.append(f'"{field}": {_dict_to_db_dict(value)}')
        else:
            dict_values.append(f'"{field}": {value}')
    return "{%s}" % (",".join(dict_values))


def _list_to_db_list(data: list):
    values = []
    for datum in data:
        if isinstance(datum, str):
            values.append(f'"{datum}"')
        elif isinstance(datum, dict):
            values.append(_dict_to_db_dict(datum))
        else:
            values.append(datum)
    return f'\'[{",".join(values)}]\''


def _str_caster(val):
    if val is None:
        return "null"
    if isinstance(val, str):
        return f"'{val}'"
    elif isinstance(val, list):
        return _list_to_db_list(val)
    elif isinstance(val, dict):
        return _dict_to_db_dict(val)
    elif isinstance(val, bool):
        val = {True: "true", False: "false"}[val]
        return val
    return str(val)


class TestCase(object):
    fixtures: List[str] = []

    @property
    def loop(self):
        return asyncio.get_event_loop()

    @pytest.fixture(scope="class", autouse=True)
    async def initialize(self):
        await clear_tables(self.db)
        await insert_fixtures(self.db, self.fixtures)
        await update_sequence(self.db)
