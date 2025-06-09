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
from django.http import JsonResponse, HttpResponseBadRequest


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


@require_POST
@login_required
def add_gift(request):
    form = GiftForm(request.POST)
    if form.is_valid():
        gift = form.save(commit=False)
        gift.who_wants_it = request.user
        gift.save()
        return render(request, 'partials/gift_item.html', {'gift': gift})
    else:
        return JsonResponse({'errors': form.errors}, status=400)


@require_POST
@login_required
def delete_gift(request):
    gift_id = request.POST.get('gift_id')
    try:
        gift = Gift.objects.get(id=gift_id, who_wants_it=request.user)
        gift.delete()
        return JsonResponse({'success': True})
    except Gift.DoesNotExist:
        return HttpResponseBadRequest("Nie znaleziono prezentu.")


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

@login_required
def user_data(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    user_ext = UserExt.objects.get(user=profile_user)
    gifts_list = Gift.objects.filter(who_wants_it=profile_user).order_by('name')
    context = {
        'user_data': profile_user,
        'profile_user_ext': user_ext,
        'gifts_list': gifts_list,
    }
    return render(request, 'user_data.html', context)

@require_POST
@login_required
def edit_user_data(request):
    user_form = UserDataForm(request.POST, instance=request.user)
    user_ext = UserExt.objects.get(user=request.user)
    
    if user_form.is_valid():
        user = user_form.save()
        user_ext.dob = user_form.cleaned_data['birth_date']
        user_ext.names_day = user_form.cleaned_data['name_day']
        user_ext.description = user_form.cleaned_data['description']
        user_ext.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'errors': user_form.errors}, status=400)


@login_required
def get_user_data_form(request):
    user_ext = UserExt.objects.get(user=request.user)
    initial_data = {
        'birth_date': user_ext.dob,
        'name_day': user_ext.names_day,
        'description': user_ext.description,
    }
    form = UserDataForm(instance=request.user, initial=initial_data)
    return render(request, 'partials/user_data_form.html', {'form': form})
