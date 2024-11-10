from django.urls import path
from Webapp import views

urlpatterns = [
    path('',views.index),
    path('index',views.index),
    path('product',views.product),
    path('data',views.data),
    path('employee',views.employee),
    path('report',views.report),
    path('setting',views.setting),
    path('profile',views.profile)
]