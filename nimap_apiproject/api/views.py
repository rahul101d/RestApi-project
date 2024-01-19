from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewUserForm
from .models import client_model,project_model
from .serializers import client_serializer,project_serializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import status
from django.utils import timezone
from rest_framework import viewsets

# Create your views here.

#for user registration
def register(request):
    if request.method=='POST':
        form=NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('created')
    return render(request,'api/register.html')


#client CRUD operation using viewsets
class client_viewset(viewsets.ViewSet):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    def list(self, request):
        c=client_model.objects.all()
        serializer=client_serializer(c,many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        id=pk
        c=client_model.objects.get(id=id)
        serializer=client_serializer(c)
        return Response(serializer.data)
    
    def create(self, request):
        data=request.data
        c=client_model.objects.filter(client_name=data["client_name"])
        if not c:
            client=client_model.objects.create(client_name=data["client_name"],created_by=request.user)
        else:
            return Response("client is already exits")
        return Response("client is created",status=status.HTTP_201_CREATED)
         
    def update(self,request,pk=None):
        id=pk
        try:
            client=client_model.objects.get(id=id)
        except:
            return Response("Not client with given id") 
        serializer=client_serializer(client,data=request.data,partial=True)
        if serializer.is_valid():
            client.updated_at=timezone.now()
            serializer.save()
            return Response('data Updated')
        return Response(serializer.errors)
        
    def destroy(self,request,pk=None):
        id=pk
        try:
            c=client_model.objects.get(id=id)
        except:
            return Response("This client does not exist...")
        c.delete()
        return Response("Data Deleted successfully...")
        

#project get and post operation using viewsets
class project_viewset(viewsets.ViewSet):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    def list(self, request):
        project=project_model.objects.filter(created_by=request.user)
        serializer=project_serializer(project,many=True)
        resp=[{'id':i['id'],"project_name":i['project_name'],"created_by":i['created_by'],'created_at':i['created_at']} for i in serializer.data]
        return Response(resp)
    
    def create(self, request,id):
        data=request.data        
        print(data)
        print(data["user"]["id"])
        print(id)
        try:
            user=User.objects.filter(id=data['user']['id'],username=data['user']['name'])
            print(user)
            if not user:
                return Response('No User Found with given id', status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response('There is no such user wih given id')
        try:
            serializer1=client_model.objects.get(id=id)
        except:
            return Response('There is no such a client', status=status.HTTP_404_NOT_FOUND)
        project=project_model.objects.create(project_name=data["project_name"],users=User.objects.get(id=data['user']['id']),client=client_model.objects.get(id=id),created_by=request.user)
        # if serializer1.is_valid():
        #     serializer1.save()
        #     return Response("Project created successfully",status=status.HTTP_201_CREATED)
        # return Response(serializer1.error,status=status.HTTP_403_FORBIDDEN)
        return Response("Project Created Success")
  

#fetch all client details or by id
class clientdetails_viewset(viewsets.ViewSet):
    def list(self, request,id=None):
        if id is not None:
            client=client_model.objects.get(id=id)
            project=project_model.objects.filter(users=client.created_by)
            resp=[{
                "id":client.id,
                "client_name":client.client_name,
                'project':[{
                    "id":i.id,
                    "name":i.project_name
                }for i in project],
                "created_at":client.created_at,
                "created_by":client.created_by.username,
                "update_at":client.updated_at
            }]
            return Response(resp)
        project=project_model.objects.all() 
        ser=project_serializer(project,many=True)
        return Response(ser.data)


   