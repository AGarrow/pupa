import os
import time
import json
import datetime
from validictory.validator import SchemaValidator
from bson import ObjectId


def makedirs(dname, clean=False):
    if not os.path.isdir(dname):
        os.makedirs(dname)
    elif clean:
        raise NotImplementedError('XXX')


class DatetimeValidator(SchemaValidator):
    """ add 'datetime' type that verifies that it has a datetime instance """

    def validate_type_datetime(self, x):
        return isinstance(x, (datetime.date, datetime.datetime))


class JSONEncoderPlus(json.JSONEncoder):
    """
    JSONEncoder that encodes datetime objects as Unix timestamps and mongo
    ObjectIds as strings.
    """
    def default(self, obj, **kwargs):
        if isinstance(obj, datetime.datetime):
            return time.mktime(obj.utctimetuple())
        elif isinstance(obj, datetime.date):
            return time.mktime(obj.timetuple())
        elif isinstance(obj, ObjectId):
            return str(obj)

        return super(JSONEncoderPlus, self).default(obj, **kwargs)