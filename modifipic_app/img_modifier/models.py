from django.db import models


class Image(models.Model):
    file = models.ImageField(blank=False, null=False)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
