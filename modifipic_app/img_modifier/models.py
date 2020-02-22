from django.db import models

CATEGORIES=[
    (0, "Raw"),
    (1, "Blurred"),
    (2, 'Gray'),
    (3, 'Flipped horizontally'),
    (4, "Sepia")
]

class Image(models.Model):
    file = models.ImageField(blank=False, null=False, upload_to='images', max_length=256)
    upload_date = models.DateTimeField(auto_now_add=True)
    category = models.IntegerField(choices=CATEGORIES, default=0)

    def __str__(self):
        return self.file.name
