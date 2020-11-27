from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import io
import os
from google.cloud import vision
from google.cloud import language_v1
import requests
import geocoder

endpoint_url = "https://api.spotify.com/v1/recommendations?"
url_post = "https://api.spotify.com/v1/playlists/2u5QonjDWwcrwBI5FWU8QP/tracks"
limit=10


# Create your views here.


def home(request):
    if request.method == 'POST' and request.FILES['myfile']:
        client_id = '9b381c643c0a49ca9efe47017dcc8948'
        client_secret  = '=274b790478014cb1826297e65e50cb44'
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        #Detection objects
        client = vision.ImageAnnotatorClient()
        with io.open('C:/Users/Avner Anjos/Desktop/git/FellDbit/media/'+filename, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        img_txt = ''
        img_labels = []
        for label in labels:
            img_txt = img_txt + "\n" + label.description  
            img_labels.append(label.description)
        print(img_txt)
        #detect sentiments
        seed_genres = 'mpb'
        client1 = language_v1.LanguageServiceClient()
        document = language_v1.Document(content=img_txt, type_=language_v1.Document.Type.PLAIN_TEXT)
        annotations = client1.analyze_sentiment(request={'document': document})
        target_danceability = annotations.sentences[0].sentiment.score
        g = geocoder.ip('me')
        market = g.geojson["features"][0]['properties']['country']
        query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={0.1}'
        response = requests.get(query,headers={"Content-Type":"application/json","Authorization":"Bearer BQDW2-11YlcjYw9hbX235MRHltAWSbXRegBRojfwSWwX1sIlyF-Rrd6gD2Dw65VX_r3kqW-QlRF8GK5c68PCF5MkEI8LUaEON0HQmwhRYNRgi7WPcwzPfBTpB1fE3HWD-bLhAqzH9MvbSZ0gBWAcqLklc6VpU0HeV1bE-SJuxojXbNCMpbcZpaJik2VT7OLIOYdvbLAL42BNYaCSn7-eJy1a5Hp77dCm6AJrIuHyA6RMsFxYxUB-uvXwBu_zQJehCwcfiv4b2ZaZcSX4lOrxbv_q"})
        json_response = response.json()
        requests.post(url_post, data = json_response)
        for i in json_response['tracks']:
            track_uri = str({i['uri']}).replace(":","%3A")
            post_url = "https://api.spotify.com/v1/playlists/2u5QonjDWwcrwBI5FWU8QP/tracks?uris="+track_uri[2:-2]
            print(post_url)
            requests.post(post_url, headers={"Content-Type": "application/json" , "Authorization": "Bearer BQDW2-11YlcjYw9hbX235MRHltAWSbXRegBRojfwSWwX1sIlyF-Rrd6gD2Dw65VX_r3kqW-QlRF8GK5c68PCF5MkEI8LUaEON0HQmwhRYNRgi7WPcwzPfBTpB1fE3HWD-bLhAqzH9MvbSZ0gBWAcqLklc6VpU0HeV1bE-SJuxojXbNCMpbcZpaJik2VT7OLIOYdvbLAL42BNYaCSn7-eJy1a5Hp77dCm6AJrIuHyA6RMsFxYxUB-uvXwBu_zQJehCwcfiv4b2ZaZcSX4lOrxbv_q"})
            print(track_uri)
        return render(request,'feel/home.html')
    return render(request,'feel/home.html')



