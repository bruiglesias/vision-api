# flake8: noqa
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2
import numpy as np
from ultralytics import YOLO
from collections import Counter
from ultralytics.utils.plotting import Annotator
import random


class ModelAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({"API": "OK"}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        # Verifique se a imagem foi enviada na solicitação POST
        if 'image' not in request.data:
            return Response({'error': 'A imagem não foi fornecida.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtenha a imagem da solicitação
        image_data = request.data['image']

        try:
            # Carregue o modelo YOLO e as configurações
            model = YOLO('application/ai/best_model.pt')
    

            # Carregue a imagem em formato OpenCV
            image = cv2.imdecode(np.fromstring(image_data.read(), np.uint8), cv2.IMREAD_COLOR)
            print(image.shape)

            # Realize as inferências no modelo YOLO
            results = model(image, conf=0.40)

            detections = []

            colors = [(random.randint(0, 255), random.randint(0, 255 ), random.randint(0, 255 )) for j in range(10)]
         

            for result in results:

                for r in result.boxes.data.tolist():

                    x1, y1, x2, y2, score, class_id = r
                    x1, y1, x2, y2, class_id = int(x1), int(y1), int(x2), int(y2), int(class_id)
      
                    cv2.rectangle(image, (x1, y1), (x2, y2), (colors[class_id % len(colors)]), 3)
                    detections.append(model.names[class_id])


            contagem = Counter(detections)
            cont_dict = {}


            for valor, frequencia in contagem.items():
                cont_dict[valor] = frequencia

            if "Coliform" not in cont_dict:
                cont_dict["Coliform"] = "Ausente"
            
            if "E.coli" not in cont_dict:
                cont_dict["E.coli"] = "Ausente"

            if "Coliform10E3" not in cont_dict:
                cont_dict["Coliform10E3"] = "Ausente"

            if "E.coli10E3" not in cont_dict:
                cont_dict["E.coli10E3"] = "Ausente"



            # Salve a imagem com as bounding boxes em uma pasta
            output_image_path = os.path.join(settings.MEDIA_ROOT, 'output.jpg')
            cv2.imwrite(output_image_path, image)

            # Construa a URL para acessar a imagem
            output_image_url = os.path.join(settings.MEDIA_URL, 'output.jpg')


            return Response({'image_url': output_image_url, 'deteccoes': cont_dict}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
