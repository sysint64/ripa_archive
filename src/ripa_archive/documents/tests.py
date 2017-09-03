from rest_framework import status
from rest_framework.test import APITestCase

from ripa_archive.accounts.models import User
from ripa_archive.documents import strings
from ripa_archive.documents.models import Folder, FolderCustomPermission, Document
from ripa_archive.permissions import codes
from ripa_archive.permissions.models import Permission, Group


class ActionsTestCase(APITestCase):
    def setUp(self):
        self.root_folder = Folder.objects.get(name="Root", parent=None)
        self.folder_1 = Folder.objects.create(name="Folder 1", parent = self.root_folder)
        self.folder_2 = Folder.objects.create(name="Folder 2", parent=self.root_folder)
        self.folder_3 = Folder.objects.create(name="Folder 3", parent=self.root_folder)

    # def test_change_folder(self):
    #     input_data = {
    #         "to_folder": self.folder_1.pk,
    #         "folders": [self.folder_2.pk, self.folder_3.pk]
    #     }
    #
    #     res = self.client.post("/documents/!action:change-folder/", input_data)
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #
    #     self.folder_2.refresh_from_db()
    #     self.folder_3.refresh_from_db()
    #
    #     self.assertEqual(self.folder_2.parent.pk, self.folder_1.pk)
    #     self.assertEqual(self.folder_3.parent.pk, self.folder_1.pk)


class I18NTestCase(APITestCase):
    def test_(self):
        # i18n_format
        expected = {
            "__code_string": "test {arg1}, {arg2}",
            "arg1": "hello",
            "arg2": "world"
        }
        f = strings.i18n_format("test {arg1}, {arg2}", arg1="hello", arg2="world")
        self.assertEqual(expected, f)

        # _parse_string
        self.assertEqual(strings._parse_string(f), "test hello, world")
        self.assertEqual(strings._parse_string("Hello world"), "Hello world")

        # _get_code
        self.assertEqual(strings._get_code(f), "test {arg1}, {arg2}")
        self.assertEqual(strings._get_code("Hello world"), "Hello world")

        # _get_text
        f = strings.i18n_format(strings.ACTIVITY_MOVE_FOLDER, new_path="", old_path="a")
        self.assertEqual(
            strings._get_text(f, strings.ACTIVITY_STRINGS, "en"),
            strings.ACTIVITY_MOVE_FOLDER.format(new_path="", old_path="a")
        )
        self.assertEqual(
            strings._get_text("Hello world!", strings.ACTIVITY_STRINGS, "en"),
            "Hello world!"
        )
        self.assertEqual(
            strings._get_text(f, strings.ACTIVITY_STRINGS, "ru"),
            strings.ACTIVITY_STRINGS[strings.ACTIVITY_MOVE_FOLDER]["ru"].format(new_path="", old_path="a")
        )
        self.assertEqual(
            strings._get_text("Hello world!", strings.ACTIVITY_STRINGS, "en", True),
            None
        )

        # get_activity_text

        self.assertEqual(
            strings.get_activity_text(strings.ACTIVITY_COPY_DOCUMENT, "en"),
            strings.ACTIVITY_COPY_DOCUMENT
        )

        self.assertEqual(
            strings.get_activity_text(strings.ACTIVITY_COPY_DOCUMENT, "ru"),
            strings.ACTIVITY_STRINGS[strings.ACTIVITY_COPY_DOCUMENT]["ru"]
        )

        self.assertEqual(
            strings.get_activity_text("Hello, my name is Andrey!", "ru"),
            "Hello, my name is Andrey!"
        )

        self.assertEqual(
            strings.get_activity_text("Hello, my name is Andrey!", "en"),
            "Hello, my name is Andrey!"
        )

        f = strings.i18n_format(strings.ACTIVITY_MOVE_FOLDER, new_path="test", old_path="test_old")
        self.assertEqual(
            strings.get_activity_text(f, "en"),
            strings.ACTIVITY_MOVE_FOLDER.format(new_path="test", old_path="test_old")
        )

        self.assertEqual(
            strings.get_activity_text(f, "ru"),
            strings.ACTIVITY_STRINGS[strings.ACTIVITY_MOVE_FOLDER]["ru"].format(new_path="test", old_path="test_old")
        )

        # get_notification_text

        self.assertEqual(
            strings.get_notification_text(strings.ACTIVITY_COPY_DOCUMENT, "en"),
            strings.ACTIVITY_COPY_DOCUMENT
        )

        self.assertEqual(
            strings.get_notification_text(f, "en"),
            strings.ACTIVITY_MOVE_FOLDER.format(new_path="test", old_path="test_old")
        )

        self.assertEqual(
            strings.get_notification_text(f, "ru"),
            strings.ACTIVITY_STRINGS[strings.ACTIVITY_MOVE_FOLDER]["ru"].format(new_path="test", old_path="test_old")
        )

        self.assertEqual(
            strings.get_notification_text("Regular text", "ru"),
            "Regular text"
        )

        self.assertEqual(
            strings.get_notification_text("Regular text", "en"),
            "Regular text"
        )

        self.assertEqual(
            strings.get_notification_text(strings.NOTIFICATION_REMARK_ACCEPTED, "en"),
            strings.NOTIFICATION_REMARK_ACCEPTED
        )

        self.assertEqual(
            strings.get_notification_text(strings.NOTIFICATION_REMARK_ACCEPTED, "ru"),
            strings.NOTIFICATION_STRINGS[strings.NOTIFICATION_REMARK_ACCEPTED]["ru"]
        )


class PermissionsTestCase(APITestCase):
    def setUp(self):
        self.root_folder = Folder.objects.get(name="Root", parent=None)
        self.folder_1 = Folder.objects.create(name="Folder 1", parent=self.root_folder)
        self.folder_2 = Folder.objects.create(name="Folder 2", parent=self.root_folder)
        self.folder_3 = Folder.objects.create(name="Folder 3", parent=self.root_folder)

        self.status_open = Document.Status.OPEN
        self.document_1 = Document.objects.create(parent=self.root_folder, status=self.status_open)
        self.document_2 = Document.objects.create(parent=self.root_folder, status=self.status_open)
        self.document_3 = Document.objects.create(parent=self.folder_1, status=self.status_open)
        self.document_4 = Document.objects.create(parent=self.folder_1, status=self.status_open)
        self.document_5 = Document.objects.create(parent=self.folder_2, status=self.status_open)
        self.document_6 = Document.objects.create(parent=self.folder_3, status=self.status_open)
        self.document_7 = Document.objects.create(parent=self.folder_3, status=self.status_open)

        self.user_1 = User.objects.create(email="user1@domain.ru")
        self.user_2 = User.objects.create(email="user2@domain.ru")
        self.user_3 = User.objects.create(email="user3@domain.ru")
        self.user_4 = User.objects.create(email="user4@domain.ru")

        self.folders_can_read_perm = Permission.objects.get(code=codes.FOLDERS_CAN_READ)
        self.documents_can_read_perm = Permission.objects.get(code=codes.DOCUMENTS_CAN_READ)
        self.folders_can_edit_prem = Permission.objects.get(code=codes.FOLDERS_CAN_EDIT)

        group_1 = Group.objects.create(name="Group 1")
        group_1.permissions.add(self.folders_can_edit_prem)

        group_2 = Group.objects.create(name="Group 2")
        group_2.permissions.add(self.folders_can_read_perm)
        group_2.permissions.add(self.documents_can_read_perm)

        group_3 = Group.objects.create(name="Group 3")
        group_3.inherit.add(group_2)

        self.user_2.group = group_1
        self.user_2.save()

        self.user_3.group = group_2
        self.user_3.save()

        self.user_4.group = group_3
        self.user_4.save()

        self.custom_permission = FolderCustomPermission.objects.create(for_instance=self.folder_2)
        self.custom_permission.groups.add(group_3)

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

        # Documents
        self.assertEqual(Document.objects.for_user(None).all().count(), 0)
        self.assertEqual(Document.objects.for_user(self.user_1, self.root_folder).all().count(), 0)

        self.assertEqual(Document.objects.for_user(self.user_2, self.root_folder).all().count(), 0)
        self.assertEqual(Document.objects.for_user(self.user_3, self.root_folder).all().count(), 2)

        self.assertEqual(Document.objects.for_user(self.user_3, self.folder_1).all().count(), 2)

        self.assertEqual(Document.objects.for_user(self.user_4, self.folder_2).all().count(), 0)

        self.custom_permission.permissions.add(self.documents_can_read_perm)
        self.assertEqual(Document.objects.for_user(self.user_4, self.folder_2).all().count(), 1)
