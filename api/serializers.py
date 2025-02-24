from rest_framework import serializers
from .models import Faculty

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name', 'department', 'image']