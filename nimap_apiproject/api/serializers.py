from rest_framework import serializers
from .models import client_model,project_model
from django.contrib.auth.models import User

#client serializer
class client_serializer(serializers.ModelSerializer):
    created_by=serializers.SerializerMethodField()
    class Meta:
        model=client_model
        fields='__all__'
    def get_created_by(self,obj):
        return obj.created_by.username if obj.created_by else None
    
#project serializer
class project_serializer(serializers.ModelSerializer):
    created_by=serializers.SerializerMethodField()
    users=serializers.SerializerMethodField()
    class Meta:
        model=project_model
        fields='__all__'
    def get_created_by(self,obj):
        return obj.created_by.username if obj.created_by else None
    def get_users(self,obj):
        return obj.created_by.username if obj.users else None

    