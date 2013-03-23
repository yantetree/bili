from django.shortcuts import render_to_response
from utils.decorators import check_method

@check_method('GET')
def home(request):
    return render_to_response('home.html')

