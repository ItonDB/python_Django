from django.urls import path
from Webapp import views
from django.conf import settings
from django.conf.urls.static import static

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)