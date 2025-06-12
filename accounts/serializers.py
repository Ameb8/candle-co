from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AdminAccessRequest

class AdminAccessRequestSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = AdminAccessRequest
        fields = '__all__'
        read_only_fields = ['approved', 'reviewed_by', 'reviewed_at']
