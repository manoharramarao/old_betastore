"""
Custom handlers may be created to handle other objects. Each custom handler
must derive from :class:`jsonpickle.handlers.BaseHandler` and
implement ``flatten`` and ``restore``.

A handler can be bound to other types by calling :func:`jsonpickle.handlers.register`.

:class:`jsonpickle.customhandlers.SimpleReduceHandler` is suitable for handling
objects that implement the reduce protocol::

    from jsonpickle import handlers

    class MyCustomObject(handlers.BaseHandler):
        ...

        def __reduce__(self):
            return MyCustomObject, self._get_args()

    handlers.register(MyCustomObject, handlers.SimpleReduceHandler)

"""

import collections
import copy
import datetime
import decimal
import re
import sys
import time

from jsonpickle import util
from jsonpickle.compat import unicode
from jsonpickle.compat import queue


class Registry(object):

    def __init__(self):
        self._handlers = {}

    def get(self, class_name):
        return self._handlers.get(class_name)

    def register(self, cls, handler):
        """Register the a custom handler for a class

        :param cls: The custom object class to handle
        :param handler: The custom handler class

        """
        class_name = util.importable_name(cls)
        self._handlers[class_name] = handler

    def unregister(self, cls):
        class_name = util.importable_name(cls)
        try:
            del self._handlers[class_name]
        except KeyError:
            pass


registry = Registry()
register = registry.register
unregister = registry.unregister
get = registry.get


class BaseHandler(object):

    def __init__(self, context):
        """
        Initialize a new handler to handle a registered type.

        :Parameters:
          - `context`: reference to pickler/unpickler

        """
        self.context = context

    def flatten(self, obj, data):
        """
        Flatten `obj` into a json-friendly form and write result to `data`.

        :param object obj: The object to be serialized.
        :param dict data: A partially filled dictionary which will contain the
            json-friendly representation of `obj` once this method has
            finished.
        """
        raise NotImplementedError('You must implement flatten() in %s' %
                                  self.__class__)

    def restore(self, obj):
        """
        Restore an object of the registered type from the json-friendly
        representation `obj` and return it.
        """
        raise NotImplementedError('You must implement restore() in %s' %
                                  self.__class__)

    @classmethod
    def handles(self, cls):
        """
        Register this handler for the given class. Suitable as a decorator,
        e.g.::

            @SimpleReduceHandler.handles
            class MyCustomClass:
                def __reduce__(self):
                    ...
        """
        registry.register(cls, self)
        return cls


class DatetimeHandler(BaseHandler):

    """Custom handler for datetime objects

    Datetime objects use __reduce__, and they generate binary strings encoding
    the payload. This handler encodes that payload to reconstruct the
    object.

    """
    def flatten(self, obj, data):
        pickler = self.context
        if not pickler.unpicklable:
            return unicode(obj)
        cls, args = obj.__reduce__()
        flatten = pickler.flatten
        payload = util.b64encode(args[0])
        args = [payload] + [flatten(i, reset=False) for i in args[1:]]
        data['__reduce__'] = (flatten(cls, reset=False), args)
        return data

    def restore(self, data):
        cls, args = data['__reduce__']
        unpickler = self.context
        restore = unpickler.restore
        cls = restore(cls, reset=False)
        value = util.b64decode(args[0])
        params = (value,) + tuple([restore(i, reset=False) for i in args[1:]])
        return cls.__new__(cls, *params)


DatetimeHandler.handles(datetime.datetime)
DatetimeHandler.handles(datetime.date)
DatetimeHandler.handles(datetime.time)


class RegexHandler(BaseHandler):
    """Flatten _sre.SRE_Pattern (compiled regex) objects"""

    def flatten(self, obj, data):
        data['pattern'] = obj.pattern
        return data

    def restore(self, data):
        return re.compile(data['pattern'])

RegexHandler.handles(type(re.compile('')))


class SimpleReduceHandler(BaseHandler):
    """Follow the __reduce__ protocol to pickle an object.

    As long as the factory and its arguments are pickleable, this should
    pickle any object that implements the reduce protocol.

    """
    def flatten(self, obj, data):
        flatten = self.context.flatten
        data['__reduce__'] = [flatten(i, reset=False) for i in obj.__reduce__()]
        return data

    def restore(self, data):
        restore = self.context.restore
        factory, args = [restore(i, reset=False) for i in data['__reduce__']]
        return factory(*args)


class OrderedDictReduceHandler(SimpleReduceHandler):
    """Serialize OrderedDict on Python 3.4+

    Python 3.4+ returns multiple entries in an OrderedDict's
    reduced form.  Previous versions return a two-item tuple.
    OrderedDictReduceHandler makes the formats compatible.

    """
    def flatten(self, obj, data):
        # __reduce__() on older pythons returned a list of
        # [key, value] list pairs inside a tuple.
        # Recreate that structure so that the file format
        # is consistent between python versions.
        flatten = self.context.flatten
        reduced = obj.__reduce__()
        factory = flatten(reduced[0], reset=False)
        pairs = [list(x) for x in reduced[-1]]
        args = flatten((pairs,), reset=False)
        data['__reduce__'] = [factory, args]
        return data


SimpleReduceHandler.handles(time.struct_time)
SimpleReduceHandler.handles(datetime.timedelta)
if sys.version_info >= (2, 7):
    SimpleReduceHandler.handles(collections.Counter)
    if sys.version_info >= (3, 4):
        OrderedDictReduceHandler.handles(collections.OrderedDict)
    else:
        SimpleReduceHandler.handles(collections.OrderedDict)

if sys.version_info >= (3, 0):
    SimpleReduceHandler.handles(decimal.Decimal)

try:
    import posix
    SimpleReduceHandler.handles(posix.stat_result)
except ImportError:
    pass


class QueueHandler(BaseHandler):
    """Opaquely serializes Queue objects

    Queues contains mutex and condition variables which cannot be serialized.
    Construct a new Queue instance when restoring.

    """
    def flatten(self, obj, data):
        return data

    def restore(self, data):
        return queue.Queue()

QueueHandler.handles(queue.Queue)


class CloneFactory(object):
    """Serialization proxy for collections.defaultdict's default_factory"""

    def __init__(self, exemplar):
        self.exemplar = exemplar

    def __call__(self, clone=copy.copy):
        """Create new instances by making copies of the provided exemplar"""
        return clone(self.exemplar)

    def __repr__(self):
        return ('<CloneFactory object at 0x%x (%s)>' % (id(self), self.exemplar))
