from django.shortcuts import render
import cv2
from rembg import remove
import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from .models import Image


# def index(request):
#     return render(request, 'index.html')

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
from PIL import Image
from rembg import remove

def change_background(request):
    if request.method == 'POST':
        original_image = request.FILES['original_image']
        background_image = request.FILES['background_image']
        
        original_image_path = os.path.join(BASE_DIR, "media", original_image.name)
        with open(original_image_path, 'wb') as f:
            f.write(original_image.read())
        
        background_image_path = os.path.join(BASE_DIR, "media", background_image.name)
        with open(background_image_path, 'wb') as f:
            f.write(background_image.read())
        
        masked_image_path = os.path.join(BASE_DIR, "media", original_image.name)
        with open(original_image_path, 'rb') as f:
            input = f.read()
            subject = remove(input, alpha_matting=True, alpha_matting_foreground_threshold=70)
        with open(masked_image_path, 'wb') as f:
            f.write(subject)
        
        background_img = Image.open(background_image_path)
        realimage = Image.open(original_image_path)
        background_img = background_img.resize((realimage.width, realimage.height)) 
        
        foreground_img = Image.open(masked_image_path)
        background_img.paste(foreground_img, (0,0), foreground_img)
        
        result_image_path = os.path.join(BASE_DIR, "media", "result.png")
        background_img.save(result_image_path, format='png')
        
        return render(request, 'change_background.html', {'result_image_path': result_image_path})
    else:
        return render(request, 'upload.html')
