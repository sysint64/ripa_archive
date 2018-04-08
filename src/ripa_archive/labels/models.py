from django.db import models


class Label(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=255)
    hex_color = models.CharField(max_length=6)

    @property
    def ref(self):
        return self.id

    def __str__(self):
        return self.code + " - " + self.name
