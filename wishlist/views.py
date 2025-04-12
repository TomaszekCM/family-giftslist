from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect


class LandingPage(View):

    def get(self, request):
        return render(request, "landing.html")
