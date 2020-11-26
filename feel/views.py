from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import io
import os
from google.cloud import vision

# Create your views here.

def home(request):
    if request.method == 'POST' and request.FILES['myfile']:
        client_id = '9b381c643c0a49ca9efe47017dcc8948'
        client_secret  = '=274b790478014cb1826297e65e50cb44'
        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        client = vision.ImageAnnotatorClient()
        with io.open(filename, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        img_labels = []
        for label in labels:
            img_labels.append(label)
        return render(request,'feel/home.html')
    return render(request,'feel/home.html')

