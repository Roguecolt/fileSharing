from django.db import models

# Create your models here.
class File(models.Model):
    name=models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name