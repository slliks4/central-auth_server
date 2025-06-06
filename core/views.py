from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['GET'])
def end_points(request):
    return Response(data=[
        
    ])

def home_page(request):
    return render (request, 'index.html')