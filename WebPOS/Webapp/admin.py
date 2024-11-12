from django.contrib import admin
from Webapp.models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Employee)
admin.site.register(Order)
admin.site.register(Payment)