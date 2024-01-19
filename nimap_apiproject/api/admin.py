from django.contrib import admin
from .models import client_model,project_model
# Register your models here.
@admin.register(client_model)
class clientadmin(admin.ModelAdmin):
    list_display=["id","client_name","created_at","created_by","updated_at"]
    
    
@admin.register(project_model)
class clientadmin(admin.ModelAdmin):
    list_display=["id","project_name","client","users","created_at","created_by"]
    
