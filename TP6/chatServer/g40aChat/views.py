from django.shortcuts import render

def index(request):
    return render(request, 'g40aChat/index.html')