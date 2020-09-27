from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
request = HttpRequest()

def home_page(request):
    response = HttpResponse()
    response.content = '<html><title>To-Do</title></html>'
    return response
