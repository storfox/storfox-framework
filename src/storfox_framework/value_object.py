class ValueObjectException(Exception):
    pass


class ValueObject(object):
    def __setattr__(self, key, value):
        raise ValueObjectException('Can\'t change value_object state')
