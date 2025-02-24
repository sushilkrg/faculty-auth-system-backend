from django.db import models

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    image = models.ImageField(upload_to='faculty_images/')
    face_encoding = models.BinaryField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name