from rest_framework import status
from rest_framework.test import APITestCase

from ripa_archive.accounts.models import User
from ripa_archive.documents.models import Folder, FolderCustomPermission
from ripa_archive.permissions.models import Permission, Group


class ActionsTestCase(APITestCase):
    def setUp(self):
        self.root_folder = Folder.objects.get(name="Root", parent=None)
        self.folder_1 = Folder.objects.create(name="Folder 1", parent = self.root_folder)
        self.folder_2 = Folder.objects.create(name="Folder 2", parent=self.root_folder)
        self.folder_3 = Folder.objects.create(name="Folder 3", parent=self.root_folder)

    def test_change_folder(self):
        input_data = {
            "to_folder": self.folder_1.pk,
            "folders": [self.folder_2.pk, self.folder_3.pk]
        }

        res = self.client.post("/documents/!action:change-folder/", input_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.folder_2.refresh_from_db()
        self.folder_3.refresh_from_db()

        self.assertEqual(self.folder_2.parent.pk, self.folder_1.pk)
        self.assertEqual(self.folder_3.parent.pk, self.folder_1.pk)


class PermissionsTestCase(APITestCase):
    def setUp(self):
        self.root_folder = Folder.objects.get(name="Root", parent=None)
        self.folder_1 = Folder.objects.create(name="Folder 1", parent=self.root_folder)
        self.folder_2 = Folder.objects.create(name="Folder 2", parent=self.root_folder)
        self.folder_3 = Folder.objects.create(name="Folder 3", parent=self.root_folder)

        self.user_1 = User.objects.create(email="user1@domain.ru")
        self.user_2 = User.objects.create(email="user2@domain.ru")
        self.user_3 = User.objects.create(email="user3@domain.ru")
        self.user_4 = User.objects.create(email="user4@domain.ru")

        self.folders_can_read_perm = Permission.objects.get(code="folders_can_read")
        self.folders_can_edit_prem = Permission.objects.get(code="folders_can_edit")

        group_1 = Group.objects.create(name="Group 1")
        group_1.permissions.add(self.folders_can_edit_prem)

        group_2 = Group.objects.create(name="Group 2")
        group_2.permissions.add(self.folders_can_read_perm)

        group_3 = Group.objects.create(name="Group 3")
        group_3.permissions.add(self.folders_can_read_perm)

        self.user_2.group = group_1
        self.user_2.save()

        self.user_3.group = group_2
        self.user_3.save()

        self.user_4.group = group_3
        self.user_4.save()

        self.custom_permission = FolderCustomPermission.objects.create()
        self.custom_permission.groups.add(group_3)
        self.custom_permission.for_instances.add(self.folder_2)

        # self.user_2.

    def test_has_perm(self):
        self.assertEqual(Folder.objects.for_user(None).all().count(), 0)
        self.assertEqual(Folder.objects.for_user(self.user_1, self.root_folder).all().count(), 0)

        self.assertEqual(Folder.objects.for_user(self.user_2, self.root_folder).all().count(), 0)
        self.assertEqual(Folder.objects.for_user(self.user_3, self.root_folder).all().count(), 3)

        self.folder_3.parent = self.folder_2
        self.folder_3.save()

        self.assertEqual(Folder.objects.for_user(self.user_3, self.folder_2).all().count(), 1)

        self.assertEqual(Folder.objects.for_user(self.user_4, self.root_folder).all().count(), 2)
        self.assertEqual(Folder.objects.for_user(self.user_4, self.folder_2).all().count(), 0)

        self.custom_permission.permissions.add(self.folders_can_read_perm)
        self.assertEqual(Folder.objects.for_user(self.user_4, self.folder_2).all().count(), 1)
