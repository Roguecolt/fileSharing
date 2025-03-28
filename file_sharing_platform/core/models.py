from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.
class File(models.Model):
    name=models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_file_type(self):
        return os.path.splitext(self.uploaded_file.name)[1].lower()

    def __str__(self):
        return f"{self.name} ({self.get_file_type()})"
    
class SharedFile(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User,on_delete=models.CASCADE,related_name="shared_files")
    shared_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('file', 'shared_with') # preventing duplicate sharing

    def __str__(self):
        return f"{self.file.name} shared with {self.shared_with.username}"