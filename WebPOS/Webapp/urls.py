from django.urls import path,re_path
from Webapp import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'Webapp'

urlpatterns = [
    path('',(views.index)),
    path('index',(views.index)),
    path('product',(views.product)),
    path('data',views.data),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('employee',views.employee),
    path('setting',views.setting),
    path('delete/<int:product_id>/', views.delete, name='delete_product'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/delete/<int:id>/', views.cart_delete, name='cart_delete'),
    re_path(r'cart/list/$', views.cart_list, name='cart_list'),

    path('checkout/', views.checkout, name='checkout'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('thank_you/<int:payment_id>/', views.thank_you, name='thank_you'),
    path('download_receipt/<int:payment_id>/', views.download_receipt, name='download_receipt'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)