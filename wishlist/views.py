from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from wishlist.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from wishlist.models import *
from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest


class LandingPage(View):
    """First page, visible once user enters the page"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
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


@login_required
def delete_gift(request):
    if request.method == 'POST':
        gift_id = request.POST.get('gift_id')
        try:
            gift = Gift.objects.get(id=gift_id, who_wants_it=request.user)
            gift.delete()
            return JsonResponse({'success': True})
        except Gift.DoesNotExist:
            return HttpResponseBadRequest("Nie znaleziono prezentu.")
    else:
        return HttpResponseNotAllowed(['POST'])


@require_POST
@login_required
def edit_gift(request):
    gift_id = request.POST.get('gift_id')
    gift = get_object_or_404(Gift, id=gift_id, who_wants_it=request.user)

    form = GiftForm(request.POST, instance=gift)
    if form.is_valid():
        updated_gift = form.save()
        return render(request, 'partials/gift_item.html', {'gift': updated_gift})
    else:
        return JsonResponse({'errors': form.errors}, status=400)
