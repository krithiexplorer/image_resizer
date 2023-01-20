from django.shortcuts import render,redirect
from django.http import HttpResponse
from PIL import Image
import os
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from . models import resizer

def home(request):
    return render(request,'home.html')

def resize_image(request):
    return render(request,'resize_image.html')    

def resize_bulk(request):
    if request.method == 'POST':
        if not "resized" in os.listdir():
            os.mkdir("resized")
        list_images = request.FILES.getlist('image')
        response_images = []
        for i in list_images:
            img_name = i.name
            img_name = img_name.split('.')[0]
            img = Image.open(i)
            imgObj = img.resize((128,128),Image.ANTIALIAS)
            imgObj.save("resized\\" + f'{img_name}_resized.png')
            response_images.append(imgObj.name)
        return render(request,{'results':response_images})    
    else:
        return render(request,'resize_bulk.html')