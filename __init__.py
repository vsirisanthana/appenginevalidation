__all__ = ['clean']
__author__ = 'pique'


import datetime
import inspect
from google.appengine.ext import db


def clean(content, model_or_properties):
    """Clean content against give model or properties dict.
    """
    properties = model_or_properties.properties() \
                 if inspect.isclass(model_or_properties) and issubclass(model_or_properties, db.Model) \
                 else model_or_properties
    return _clean_content(content, properties)

def _clean_content(content, properties):
    result = {}
    for key, value in content.items():
        property = properties.get(key)
        if property:
            value = _clean_value(value, property)
        result[key] = value
    return result

def _clean_value(value, property):
    if value is not None:
        if isinstance(property, db.IntegerProperty):
            value = None if value == '' else int(value)
        elif isinstance(property, db.DateProperty):
            value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
        elif isinstance(property, db.DateTimeProperty):
            try:
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return value