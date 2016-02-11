from django.test import TestCase

from corehq.apps.repeaters.dbaccessors import (
    get_pending_repeat_record_count,
    get_success_repeat_record_count,
    get_failure_repeat_record_count,
    get_repeaters_by_domain,
    get_repeat_records,
)
from corehq.apps.repeaters.models import RepeatRecord, CaseRepeater


class TestRepeatRecordDBAccessors(TestCase):
    dependent_apps = ['corehq.apps.repeaters', 'corehq.couchapps']
    repeater_id = '1234'
    domain = 'test-domain'

    @classmethod
    def setUpClass(cls):
        failed = RepeatRecord(
            domain=cls.domain,
            failure_reason='Some python error',
            repeater_id=cls.repeater_id,
        )
        success = RepeatRecord(
            domain=cls.domain,
            succeeded=True,
            repeater_id=cls.repeater_id,
        )
        pending = RepeatRecord(
            domain=cls.domain,
            succeeded=False,
            repeater_id=cls.repeater_id,
        )

        cls.records = [
            failed,
            success,
            pending,
        ]

        for record in cls.records:
            record.save()

    @classmethod
    def tearDownClass(cls):
        for record in cls.records:
            record.delete()

    def test_get_pending_repeat_record_count(self):
        count = get_pending_repeat_record_count(self.domain, self.repeater_id)
        self.assertEqual(count, 1)

    def test_get_success_repeat_record_count(self):
        count = get_success_repeat_record_count(self.domain, self.repeater_id)
        self.assertEqual(count, 1)

    def test_get_failure_repeat_record_count(self):
        count = get_failure_repeat_record_count(self.domain, self.repeater_id)
        self.assertEqual(count, 1)

    def test_get_repeat_records(self):
        records = get_repeat_records(self.domain)
        self.assertEqual(len(records), 3)


class TestRepeatersDBAccessors(TestCase):
    dependent_apps = ['corehq.apps.repeaters', 'corehq.couchapps']
    domain = 'test-domain'

    @classmethod
    def setUpClass(cls):
        repeater = CaseRepeater(
            domain=cls.domain,
        )
        cls.repeaters = [
            repeater
        ]

        for repeater in cls.repeaters:
            repeater.save()

    @classmethod
    def tearDownClass(cls):
        for repeater in cls.repeaters:
            repeater.save()

    def test_get_repeaters_by_domain(self):
        repeaters = get_repeaters_by_domain(self.domain)
        self.assertEqual(len(repeaters), 1)
        self.assertEqual(repeaters[0].__class__, CaseRepeater)
