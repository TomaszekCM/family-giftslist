from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View


class HomeView(View):

    def get(self, request):
        return HttpResponse("mamy to, żye!")