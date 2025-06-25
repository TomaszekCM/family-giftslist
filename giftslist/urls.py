"""
URL configuration for giftslist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wishlist.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name="landing"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('home', HomePage.as_view(), name="home"),
    path('add_gift/', add_gift, name="add_gift"),
    path('delete_gift/', delete_gift, name='delete_gift'),
    path('edit_gift/', edit_gift, name='edit_gift'),
    path('user_data/<int:user_id>/', user_data, name='user_data'),
    path('edit_user_data/', edit_user_data, name='edit_user_data'),
    path('get_user_data_form/', get_user_data_form, name='get_user_data_form'),
    path('get_important_date_form/', get_important_date_form, name='get_important_date_form'),
    path('get_important_date_form/<int:date_id>/', get_important_date_form, name='get_important_date_form_edit'),
    path('add_important_date/', add_important_date, name='add_important_date'),
    path('edit_important_date/<int:date_id>/', edit_important_date, name='edit_important_date'),
    path('delete_important_date/<int:date_id>/', delete_important_date, name='delete_important_date'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/add_ajax/', add_user_ajax, name='user_add_ajax'),
]
