from django.test import TestCase

from ripa_archive.permissions.models import Group
from ripa_archive.permissions.models import Permission


class PermissionsTestCase(TestCase):
    def setUp(self):
        folders_can_read_perm = Permission.objects.get(code="folders_can_read")
        folders_can_delete = Permission.objects.get(code="folders_can_delete")
        folders_can_edit = Permission.objects.get(code="folders_can_edit")

        self.group_1 = Group.objects.create(name="Group 1")
        self.group_1.permissions.add(folders_can_read_perm)

        self.group_2 = Group.objects.create(name="Group 2")
        self.group_2.permissions.add(folders_can_delete)
        self.group_2.inherit.add(self.group_1)

        self.group_3 = Group.objects.create(name="Group 3")
        self.group_3.permissions.add(folders_can_edit)
        self.group_3.inherit.add(self.group_1)
        self.group_3.inherit.add(self.group_2)

    def test_has_perm(self):
        self.assertEqual(self.group_1.has_permission("folders_can_read"), True)
        self.assertEqual(self.group_1.has_permission("folders_can_delete"), False)
        self.assertEqual(self.group_1.has_permission("folders_can_edit"), False)

        self.assertEqual(self.group_2.has_permission("folders_can_read"), True)
        self.assertEqual(self.group_2.has_permission("folders_can_delete"), True)
        self.assertEqual(self.group_2.has_permission("folders_can_edit"), False)

        self.assertEqual(self.group_3.has_permission("folders_can_read"), True)
        self.assertEqual(self.group_3.has_permission("folders_can_delete"), True)
        self.assertEqual(self.group_3.has_permission("folders_can_edit"), True)
