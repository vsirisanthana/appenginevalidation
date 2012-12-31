import datetime

import unittest2
from google.appengine.ext import db, testbed

from appenginevalidation import clean


class TestClean(unittest2.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()

    def tearDown(self):
        self.testbed.deactivate()

    class DummyClean(db.Model):
        number = db.IntegerProperty()
        name = db.StringProperty()
        anniversary = db.DateProperty()
        created = db.DateTimeProperty()
        last_modified = db.DateTimeProperty()
    DummyCleanContent = DummyClean

    def test_clean(self):
        self.assertEqual(clean({
            'number': '1',
            'name': 'dummy',
            'anniversary': '2012-11-23',
            'created': '2012-11-23 08:30:00',
            'last_modified': '2012-11-24 00:00:00.123000'
        }, self.DummyCleanContent), {
            'number': 1,
            'name': 'dummy',
            'anniversary': datetime.date(2012, 11, 23),
            'created': datetime.datetime(2012, 11, 23, 8, 30, 00),
            'last_modified': datetime.datetime(2012, 11, 24, 0, 0, 0, 123000)
        })

    def test_clean__properties(self):
        self.assertEqual(clean({
            'number': '1',
            'name': 'dummy',
            'anniversary': '2012-11-23',
            'created': '2012-11-23 08:30:00',
            'last_modified': '2012-11-24 00:00:00.123000'
        }, self.DummyCleanContent.properties()), {
            'number': 1,
            'name': 'dummy',
            'anniversary': datetime.date(2012, 11, 23),
            'created': datetime.datetime(2012, 11, 23, 8, 30, 00),
            'last_modified': datetime.datetime(2012, 11, 24, 0, 0, 0, 123000)
        })
