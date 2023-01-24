from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from PIL import Image
import os
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from . models import resizer
#from cloudinary.api import resources
import cloudinary
import requests
from django.conf import settings
from django.core.files.storage import default_storage as storage
from io import BytesIO
import zipfile

def home(request):
    return render(request,'home.html')

def resize_image(request):
    return render(request,'resize_image.html')    

def resize_bulk(request):
    if request.method == 'POST':
        if not "resized" in os.listdir():
            os.mkdir("resized")
        list_images = request.FILES.getlist('image')
        resizeval = int(request.POST['resizeval'])
        response_images = []
        for ctr, i in enumerate(list_images, 1):
            img_name = i.name
            img_name = img_name.split('.')[0]
            img = Image.open(i)
            imgObj = img.resize((resizeval, resizeval), Image.ANTIALIAS)
            imagePath = f"resized/{img_name}{ctr}+.png"
            imgObj.save(imagePath)
            uploaded_image = cloudinary.uploader.upload(imagePath,
                                                        folder="resized_images",)
            response_images.append(uploaded_image['url'])
            os.remove(imagePath)
        print(response_images)
        """request.session['image_list'] = response_images
        return HttpResponseRedirect('/download_images/')"""
        return render(request,'download_images.html',{'image_list' : response_images})
        
    else:
        return render(request, 'resize_bulk.html')
        #return HttpResponse("Yeahhh")
"""          
def download_images(request):
    if request.method == 'GET':
        image_list = request.session.get('image_list')
        in_memory = BytesIO()
        zip = zipfile.ZipFile(in_memory, "w")
        for image_name in image_list:
            image_url = cloudinary.utils.cloudinary_url(image_name)
            image_data = requests.get(image_url).content
            zip.writestr(image_name, image_data)
        zip.close()
        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=images.zip"
        in_memory.seek(0)
        response.write(in_memory.read())
        response["Content-Length"] = in_memory.tell()
        return response
    
    return render(request, 'download_images.html', {'image_list': image_list})

    """