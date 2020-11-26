import io
import os
from google.cloud import vision
client = vision.ImageAnnotatorClient()


file_name = os.path.abspath('C:/Users\Avner Anjos/Desktop/git/FellDbit/teste.jpg')

with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)
