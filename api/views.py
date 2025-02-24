from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Faculty
from .serializers import FacultySerializer
import face_recognition
import numpy as np
import json

@api_view(['POST'])
def admin_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    print(username, password)
    
    if username == "user1" and password == "123456":
        return Response({'message': 'Login successful'})
    return Response({'message': 'Invalid credentials'}, status=401)

@api_view(['POST'])
def admin_logout(request):
    # Since we're using token-based auth, we just need to return a success response
    # The frontend will handle clearing the auth state
    return Response({'message': 'Logged out successfully'})

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            faculty = serializer.save()
            
            # Process face encoding
            image = face_recognition.load_image_file(faculty.image.path)
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) > 0:
                faculty.face_encoding = face_encodings[0].tobytes()
                faculty.save()
                return Response(serializer.data, status=201)
            else:
                faculty.delete()
                return Response({'error': 'No face detected'}, status=400)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def verify_face(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=400)

    # Load and encode the uploaded image
    image = face_recognition.load_image_file(request.FILES['image'])
    face_encodings = face_recognition.face_encodings(image)
    
    if len(face_encodings) == 0:
        return Response({'error': 'No face detected'}, status=400)
    
    unknown_encoding = face_encodings[0]
    
    # Compare with all faculty faces
    for faculty in Faculty.objects.all():
        stored_encoding = np.frombuffer(faculty.face_encoding)
        result = face_recognition.compare_faces([stored_encoding], unknown_encoding)[0]
        
        if result:
            return Response({
                'match': True,
                'faculty': {
                    'name': faculty.name,
                    'department': faculty.department
                }
            })
    
    return Response({'match': False})