from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
# Ultralytics
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import base64
import io

class ModelYolo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = YOLO('model/best.onnx')

    def post(self, request):
        try:
            file_obj = request.data['file']
            image = Image.open(file_obj).convert('RGB')

            img = np.array(image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            results = self.model.predict(source=[img])
            
            annotated_img = self.annotate_image(results)

            # Convert the image to base64
            buffered = io.BytesIO()
            annotated_img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            return Response({'annotated_image': img_str}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def annotate_image(self, results):
        for result in results:
            annotated_img = Image.fromarray(cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB))
        return annotated_img

            