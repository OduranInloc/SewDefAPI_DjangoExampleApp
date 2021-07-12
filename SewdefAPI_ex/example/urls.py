from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('jobs', views.jobs, name='jobs'),
    path('contracts', views.contracts, name='contracts'),
    path('', views.index, name='index')
    ]