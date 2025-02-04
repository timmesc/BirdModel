from django.shortcuts import render
from roboflow import Roboflow
from PIL import Image
import os
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse


# Initialize the Roboflow API and load the model
rf = Roboflow(api_key=os.getenv('ROBOFLOW_API_KEY'))
project = rf.workspace().project("bird-species-detector")
model = project.version(851).model

def predictor(request):
    return render(request, 'main.html')

def formInfo(request):
    if request.method == 'POST' and request.FILES['bird_image']:
        try:
            # Create media directory if it doesn't exist
            
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            
            # Get the uploaded image
            bird_image = request.FILES['bird_image']
            

            # Save the image temporarily on the server
            img_path = os.path.join(settings.MEDIA_ROOT, 'temp_bird_image.jpg')
            with open(img_path, 'wb+') as f:
                for chunk in bird_image.chunks():
                    f.write(chunk)
     
            
            # Use Roboflow to make the prediction
            prediction_result = model.predict(img_path)
            prediction_json = prediction_result.json()

            # Extract the prediction details
            predicted_class = prediction_json['predictions'][0]['top'] if prediction_json['predictions'] else 'Unknown'
            confidence = prediction_json['predictions'][0]['confidence'] if prediction_json['predictions'] else 0.0
            
            # Handle endangered species detection
            endangered_list = [
                'HELMET VANGA', 'JOCOTOCO ANTPITTA', 'JAVA SPARROW', 'OKINAWA RAIL',
                'GOULDIAN FINCH', 'ALTAMIRA YELLOWTHROAT', 'BORNEAN BRISTLEHEAD',
                'ASHY STORM PETREL', 'WATTLED CURASSOW', 'MALEO', 'HORNED GUANBUFFLEHEAD',
                'VISAYAN HORNBILL', 'TRICOLORED BLACKBIRD', 'KAGU'
            ]
            
            endangered_detected = predicted_class in endangered_list

            # Save the annotated image
            predicted_image_path = 'predicted_image.jpg'
            prediction_result.save(os.path.join(settings.MEDIA_ROOT, predicted_image_path))

            return render(request, 'result.html', {
                'prediction': predicted_class,
                'confidence': confidence * 100,
                'endangered_detected': endangered_detected,
                'predicted_image': predicted_image_path
            })
        except Exception as e:
            return render(request, 'main.html', {'error': f'An error occurred: {str(e)}'})

    return render(request, 'main.html', {'error': 'Please upload an image.'})
