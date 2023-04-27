from django.shortcuts import render
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

import os

def remove_background(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        name = fs.save(uploaded_image.name, uploaded_image)
        original_image_path = os.path.join(BASE_DIR, "media", name)

        output_path = os.path.join(BASE_DIR, "media", name)
        input = open(original_image_path, 'rb').read()
        subject = remove(input, alpha_matting=True, alpha_matting_foreground_threshold=70)

        with open(output_path, 'wb') as f:
            f.write(subject)

        masked_image_path = os.path.join(BASE_DIR, "media", name)
        Image.objects.create(name=name, original_image=original_image_path, masked_image=masked_image_path)

        request.session['image_name'] = name

        return redirect('result')
    return render(request, 'remove_background.html')

def result(request):
    image_name = request.session.get('image_name', None)
    if image_name:
        image = Image.objects.get(name=image_name)
        context = {'image': image}
        return render(request, 'result.html', context)
    return redirect('remove_background')



import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def change_background(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        name = fs.save(uploaded_image.name, uploaded_image)

        original_image_path = os.path.join(settings.BASE_DIR, 'media', 'original', name)
        original_image_url = fs.url(name)

        output_path = os.path.join(settings.BASE_DIR, 'media', 'masked', name)
        input = open(original_image_path, 'rb').read()
        subject = remove(input, alpha_matting=True, alpha_matting_foreground_threshold=70)

        with open(output_path, 'wb') as f:
            f.write(subject)

        masked_image_url = os.path.join(settings.MEDIA_URL, 'masked', name)

        return render(request, 'change_background.html', {'original_image': original_image_url, 'masked_image': masked_image_url})
    
    return render(request, 'change_background.html')


import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def change_background(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        name = fs.save(uploaded_image.name, uploaded_image)
        original_image_path = os.path.join(BASE_DIR, 'media',  name)
        original_image_url = fs.url(name)

        output_path = os.path.join(BASE_DIR, 'media', name)
        input = open(original_image_path, 'rb').read()
        subject = remove(input, alpha_matting=True, alpha_matting_foreground_threshold=70)

        with open(output_path, 'wb') as f:
            f.write(subject)

        masked_image_url = os.path.join('/', 'media', name)
        return render(request, 'change_background.html', {'original_image': original_image_url, 'masked_image': masked_image_url})

    return render(request, 'change_background.html')

import os
from django.conf import settings
from django.shortcuts import render
from PIL import Image




def process_image(request):
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'original'), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'masked'), exist_ok=True)

    # Get the uploaded image from the request
    uploaded_image = request.FILES.get('image')
    img = Image.open(uploaded_image)

    # Save the original image to disk
    name = uploaded_image.name
    original_image_path = os.path.join(settings.MEDIA_ROOT, 'original', name)
    with open(original_image_path, 'wb') as f:
        f.write(uploaded_image.read())

    # Remove the background
    with open(os.path.join(settings.MEDIA_ROOT, 'masked', 'img.png'), 'wb') as f:
        input = open(original_image_path, 'rb').read()
        subject = remove(input, alpha_matting=True, alpha_matting_foreground_threshold=70)
        f.write(subject)

    # Paste the foreground on the background
    background_path = os.path.join(settings.MEDIA_ROOT, 'original', 'background.jpg')
    background_img = Image.open(background_path)
    background_img = background_img.resize((img.width, img.height)) 
    foreground_path = os.path.join(settings.MEDIA_ROOT, 'masked', 'img.png')
    foreground_img = Image.open(foreground_path)
    background_img.paste(foreground_img, (0,0), foreground_img)

    # Save the result
    result_path = os.path.join(settings.MEDIA_ROOT, 'masked', 'result.png')
    background_img.save(result_path, format='png')

    # Render the template with the result and the original image path
    return render(request, 'process_image.html', {'result_path': result_path, 'original_image_path': original_image_path})
