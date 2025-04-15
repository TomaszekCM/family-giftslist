from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from wishlist.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from wishlist.models import *
from django.http import HttpResponseNotAllowed, JsonResponse


class LandingPage(View):
    """First page, visible once user enters the page"""

    def get(self, request):
        return render(request, "landing.html")


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

        form.add_error(None, "Zły email lub hasło")

        return render(request, "login.html", {"form": form})


def logout_view(request):
    """Simple logout address, with no html assigned"""
    logout(request)
    return redirect('landing')


class HomePage(LoginRequiredMixin, View):
    """Initial page for logged-in users"""

    def get(self, request):
        gifts_list = Gift.objects.filter(who_wants_it=request.user).order_by('name')
        form = GiftForm()
        context = {
            'gifts_list': gifts_list,
            'form': form
        }
        return render(request, 'home.html', context)


def add_gift(request):
    if request.method == 'POST':
        form = GiftForm(request.POST)
        if form.is_valid():
            gift = form.save(commit=False)
            gift.who_wants_it = request.user
            gift.save()
            return render(request, 'partials/gift_item.html', {'gift': gift})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])
