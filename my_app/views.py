from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


# render home.html
def home(request):
    return render(request, 'home.html')
