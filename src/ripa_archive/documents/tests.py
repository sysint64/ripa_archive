from rest_framework import status
from rest_framework.test import APITestCase

from ripa_archive.documents.models import Folder


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
