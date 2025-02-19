"""
Use DRF's Serializer for input validation, separating validation logic from the view.
"""
from rest_framework import serializers

class TodoSerializer(serializers.Serializer):
    description = serializers.CharField(
        required=True, 
        allow_blank=False, 
        trim_whitespace=True
    )