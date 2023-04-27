# from django.db import models
# import os

# # Create your models here.
# def filepath(request, filename):
#     old_filename = filename
#     return os.path.join('orignal/images', filename)

# def bgfilepath(request, filename):
#     old_filename = filename
#     return os.path.join('background/images', filename)
    

# class Image(models.Model):
#     orignal_image=models.ImageField(upload_to=filepath, null=True, blank=True)
#     Background_image=models.ImageField(upload_to=bgfilepath, null=True, blank=True)
   

from django.db import models
import os

# def filepath(request, filename):
#     old_filename = filename
#     return os.path.join('media', filename)

class Image(models.Model):
    name = models.CharField(max_length=100)
    original_image = models.ImageField(upload_to='original')
    masked_image = models.ImageField(upload_to='masked')