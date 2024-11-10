from django.shortcuts import render,redirect
from django.http import HttpResponse
from Webapp.models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,"index.html")#ส่งไฟล์ index.html ใน floder templates กลับไป

def product(request):
    return render(request,"product.html")

def data(request):
    all_Product = Product.objects.all()
    all_categories = categories.objects.all()
    
    # กำหนดค่าเริ่มต้นให้ context
    context = {
        "all_Product": all_Product,
        "all_categories": all_categories,
    }

    if request.method == "POST":
        # รับข้อมูลจากฟอร์ม
        category_id = request.POST.get("categories")
        pname = request.POST.get("name")
        pdescription = request.POST.get("description")
        pprice = request.POST.get("price")
        pstock = request.POST.get("stock")

        # ตรวจสอบว่าข้อมูลครบถ้วนก่อนบันทึก
        if category_id and pname and pprice and pstock:
            # แปลง category_id เป็นอ็อบเจกต์ Categories
            try:
                selected_category = categories.objects.get(id=category_id)
            except categories.DoesNotExist:
                context["error"] = "ไม่พบประเภทสินค้าที่เลือก"
                return render(request, "data.html", context)
            else :
                context["error"] = "กรุณากรอกข้อมูลให้ครบถ้วน"
            # บันทึกข้อมูลสินค้า
            newProduct = Product.objects.create(
                categories=selected_category,
                name=pname,
                description=pdescription,
                price=pprice,
                stock=pstock
            )
            newProduct.save()
            # messages.success(request,"บันทึกข้อมูลเรียบร้อย")
            context["message"] = "เพิ่มสินค้าสำเร็จ!"
        
            # อัปเดตข้อมูลหลังจากเพิ่มสินค้าใหม่
            context["all_Product"] = Product.objects.all()  # รีเฟรชข้อมูลสินค้า

        return render(request, "data.html", context)
    else:
        # กรณี GET ให้ render ตามปกติ
        return render(request, "data.html", context)


    
def employee(request):
    # all_Employee = Employee.objects.filter(fname)
    all_Employee = Employee.objects.all()
    return render(request,"employee.html",{"all_Employee":all_Employee})

def report(request):
    return render(request,"report.html")

def setting(request):
    return render(request,"setting.html")

def profile(request):
    return render(request,"profile.html")