from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from wishlist.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from wishlist.models import *
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django import forms
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


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
    important_dates = ImportantDate.objects.filter(user=profile_user).order_by('date')
    context = {
        'user_data': profile_user,
        'profile_user_ext': user_ext,
        'gifts_list': gifts_list,
        'important_dates': important_dates,
    }
    return render(request, 'user_data.html', context)

@require_POST
@login_required
def edit_user_data(request):
    user_form = UserDataForm(request.POST, instance=request.user)
    user_ext = UserExt.objects.get(user=request.user)
    
    if user_form.is_valid():
        user_form.save()
        user_ext.dob = user_form.cleaned_data['birth_date']
        user_ext.names_day = user_form.cleaned_data['name_day']
        user_ext.description = user_form.cleaned_data['description']
        user_ext.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({
            'success': False,
            'errors': user_form.errors
        }, status=400)


@login_required
def get_user_data_form(request):
    user_ext = UserExt.objects.get(user=request.user)
    initial_data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'birth_date': user_ext.dob,
        'name_day': user_ext.names_day,
        'description': user_ext.description,
        'is_superuser': request.user.is_superuser,
    }
    form = UserDataForm(initial=initial_data, instance=request.user)
    return render(request, 'partials/user_data_form.html', {'form': form})

@login_required
def get_important_date_form(request, date_id=None):
    if date_id:
        date = get_object_or_404(ImportantDate, id=date_id, user=request.user)
        form = ImportantDateForm(instance=date)
    else:
        form = ImportantDateForm()
    return render(request, 'partials/important_date_form.html', {'form': form})

@login_required
def add_important_date(request):
    if request.method == 'POST':
        form = ImportantDateForm(request.POST)
        if form.is_valid():
            date = form.save(commit=False)
            date.user = request.user
            date.save()
            return JsonResponse({
                'status': 'success',
                'date': {
                    'id': date.id,
                    'name': date.name,
                    'date': f"{str(date.date['day']).zfill(2)}.{str(date.date['month']).zfill(2)}"
                }
            })
        return JsonResponse({
            'status': 'error',
            'errors': {field: errors for field, errors in form.errors.items()}
        }, status=400)
    return HttpResponseBadRequest()

@login_required
@require_POST
def edit_important_date(request, date_id):
    date = get_object_or_404(ImportantDate, id=date_id, user=request.user)
    form = ImportantDateForm(request.POST, instance=date)
    if form.is_valid():
        date = form.save()
        return JsonResponse({
            'status': 'success',
            'date': {
                'id': date.id,
                'name': date.name,
                'date': f"{str(date.date['day']).zfill(2)}.{str(date.date['month']).zfill(2)}"
            }
        })
    return JsonResponse({
        'status': 'error',
        'errors': {field: errors for field, errors in form.errors.items()}
    }, status=400)

@login_required
@require_POST
def delete_important_date(request, date_id):
    date = get_object_or_404(ImportantDate, id=date_id, user=request.user)
    date.delete()
    return JsonResponse({'success': True})

class UserListView(LoginRequiredMixin, ListView):

    def get(self, request):
        all_users = User.objects.all().select_related('userext').order_by('last_name', 'first_name')
        return render(request, 'user_list.html', {'users': all_users})
    

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user_add.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password1'])
        if form.cleaned_data.get('is_superuser'):
            user.is_superuser = True
            user.is_staff = True
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        # Keep form data on validation error
        return self.render_to_response(self.get_context_data(form=form))

@user_passes_test(lambda u: u.is_superuser)
def add_user_ajax(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'partials/user_add_form.html', {'form': form})
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Render only <tr> for new user
            row_html = render_to_string('partials/user_row.html', {'this_user': user, 'user': request.user})
            return HttpResponse(row_html)
        else:
            return render(request, 'partials/user_add_form.html', {'form': form}, status=400)
    else:
        return HttpResponseBadRequest()


def edit_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    user = get_object_or_404(User, id=user_id)
    user_ext, _ = UserExt.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.is_superuser = form.cleaned_data['is_superuser']
            user.save()

            user_ext.dob = form.cleaned_data['birth_date']
            user_ext.names_day = form.cleaned_data['name_day']
            user_ext.description = form.cleaned_data['description']
            user_ext.save()
            return JsonResponse({'success': True})
        else:
            html = render_to_string('partials/edit_user_form.html', {
                'form': form,
                'user_id': user.id
            }, request=request)
            return JsonResponse({'form_html': html}, status=400)

    else:  # GET
        form = UserEditForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_superuser': user.is_superuser,
            'birth_date': user_ext.dob,
            'name_day': user_ext.names_day,
            'description': user_ext.description,
        })

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('partials/edit_user_form.html', {'form': form, 'user_id': user.id}, request=request)
            return JsonResponse({'form_html': html})

        return render(request, 'users/edit_page.html', {'form': form, 'user_id': user.id})