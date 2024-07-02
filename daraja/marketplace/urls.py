from django.urls import path 

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('accounts/register/', views.register_view, name='register'),
        path('accounts/login/', views.login_view, name='login'),
        path('logout/', views.logout_view, name='logout'),

        path('express/', views.stkpush, name='stk'),
        # htmx call
        path('stkpush/', views.init_stk, name='stkpush'),
        ]

