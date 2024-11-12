from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from Webapp.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
    return render(request,"index.html")#ส่งไฟล์ index.html ใน floder templates กลับไป

def product(request):
    all_Product = Product.objects.all()
    all_categories = Category.objects.all()
    context = {
        "all_Product": all_Product,
        "all_categories": all_categories,
    }
    return render(request,"product.html",context)

def data(request):
    all_Product = Product.objects.all()
    all_categories = Category.objects.all()
    
    # กำหนดค่าเริ่มต้นให้ context
    context = {
        "all_Product": all_Product,
        "all_categories": all_categories,
    }

    if request.method == "POST":
        # รับข้อมูลจากฟอร์ม
        category_id = request.POST.get("category")
        pname = request.POST.get("name")
        pdescription = request.POST.get("description")
        pprice = request.POST.get("price")
        pstock = request.POST.get("stock")
        pimage = request.FILES.get("image")

        # ตรวจสอบว่าข้อมูลครบถ้วนก่อนบันทึก
        if category_id and pname and pprice and pstock:
            # แปลง category_id เป็นอ็อบเจกต์ Categories
            try:
                selected_category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                context["error"] = "ไม่พบประเภทสินค้าที่เลือก"
                return render(request, "data.html", context)
            # บันทึกข้อมูลสินค้า
            newProduct = Product.objects.create(
                category=selected_category,
                name=pname,
                description=pdescription,
                price=pprice,
                stock=pstock,
                image=pimage
            )
            newProduct.save()
            messages.success(request, "เพิ่มสินค้าสำเร็จ!")
        
            # อัปเดตข้อมูลหลังจากเพิ่มสินค้าใหม่
            context["all_Product"] = Product.objects.all()  # รีเฟรชข้อมูลสินค้า
        else :
                messages.error( request,"กรุณากรอกข้อมูลให้ครบถ้วน")
            
        return redirect('/data')
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

def edit(request):

    return render(request, 'edit.html')

def delete(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request,"ลบข้อมูลเรียบร้อย")
    return HttpResponseRedirect('/data')

def login_view(request):
    form = AuthenticationForm()
    return render(request,'account/login.html',{
        'form': form,
    })