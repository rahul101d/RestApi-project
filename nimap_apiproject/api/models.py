from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#client model
class client_model(models.Model):
    client_name=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    updated_at=models.DateTimeField(null=True)

#project model
class project_model(models.Model):
    project_name=models.CharField(max_length=50)
    client=models.ForeignKey(client_model,on_delete=models.CASCADE)
    users=models.ForeignKey(User,on_delete=models.CASCADE,related_name='assigned_users')
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_by')
   
    