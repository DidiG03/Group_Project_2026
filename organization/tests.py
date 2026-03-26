from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Department


class OrganizationTests(TestCase):
    def test_department_delete_blocked_when_two_or_less_exist(self):
        d1 = Department.objects.create(name="D1", leader_name="L1", specialisation="S1")
        Department.objects.create(name="D2", leader_name="L2", specialisation="S2")

        with self.assertRaises(ValidationError):
            d1.delete()
