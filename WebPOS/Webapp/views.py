from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request,"index.html")#ส่งไฟล์ index.html ใน floder templates กลับไป

def product(request):
    return render(request,"product.html")

def data(request):
    return render(request,"data.html")

def employee(request):
    return render(request,"employee.html")

def report(request):
    return render(request,"report.html")

def setting(request):
    return render(request,"setting.html")

def profile(request):
    return render(request,"profile.html")