from django.shortcuts import render
# from .forms import ImageForm
# from .models import Image

# # Create your views here.
# def index(request):
#     if request.method == "POST":
#         form=ImageForm(data=request.POST,files=request.FILES)
#         if form.is_valid():
#             form.save()
#             obj=form.instance
#             return render(request,"index.html",{"obj":obj})

#     else:
#         form=ImageForm()
#     img=Image.objects.all()
#     return render(request,"index.html",{"img":img,"form":form})


import cv2
from rembg import remove
import os

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from .models import Image


def index(request):
    return render(request, 'index.html')

BASE_DIR = Path(__file__).resolve().parent.parent

def remove_background(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        name = fs.save(uploaded_image.name, uploaded_image)
        original_image_url = fs.url(name)

        output_path = 'media/masked/' + name
        input = open('media/' + name, 'rb').read()
        subject = remove(input, alpha_matting=True, alpha_matting_foreground_threshold=70)

        with open(output_path, 'wb') as f:
            f.write(subject)

        masked_image_url = '/media/masked/' + name
        Image.objects.create(name=name, original_image=original_image_url, masked_image=masked_image_url)

        return redirect('result')
    return render(request, 'remove_background.html')


def change_background(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        name = fs.save(uploaded_image.name, uploaded_image)
        original_image_url = fs.url(name)

        output_path = 'media/masked/' + name
        input = open('media/original/' + name, 'rb').read()
        subject = remove(input, alpha_matting=True, alpha_matting_foreground_threshold=70)

        with open(output_path, 'wb') as f:
            f.write(subject)

        return render(request, 'change_background.html', {'original_image': original_image_url, 'masked_image': '/'+output_path})
    return render(request, 'change_background.html')


def result(request):
    images = Image.objects.all()
    return render(request, 'result.html', {'images': images})
