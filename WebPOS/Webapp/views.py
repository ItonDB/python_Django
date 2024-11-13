from django.shortcuts import render,redirect,get_object_or_404
from Webapp.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.http import FileResponse
import os
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

@login_required(login_url='/login')
# Create your views here.
def index(request):
    return render(request,"index.html")#ส่งไฟล์ index.html ใน floder templates กลับไป

@login_required(login_url='/login')
def product(request):
    all_Product = Product.objects.all()
    all_categories = Category.objects.all()
    context = {
        "all_Product": all_Product,
        "all_categories": all_categories,
    }
    return render(request,"product.html",context)

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def employee(request):
    # all_Employee = Employee.objects.filter(fname)
    all_Employee = Employee.objects.all()
    return render(request,"employee.html",{"all_Employee":all_Employee})

@login_required(login_url='/login')
def setting(request):
    return render(request,"setting.html")

@login_required(login_url='/login')
def edit(request):
    return render(request, 'edit.html')

@login_required(login_url='/login')
def delete(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request,"ลบข้อมูลเรียบร้อย")
    return HttpResponseRedirect('/data')

def login_view(request):

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('/index')
        else:
            messages.error(request,"Username หรือ Password ไม่ถูกต้อง")
    else:
        form = AuthenticationForm()
    return render(request,'account/login.html',{
        'form': form,
    })

@login_required(login_url='/login')
def logout_view(request):
    if request.method=='POST':
        logout(request)
        messages.success(request,"ออกจากระบบเรียบร้อย")
        return redirect('/login')

@login_required(login_url='/login')
def cart_add(request, id):
    product = get_object_or_404(Product, id=id)
    cart_items = request.session.get('cart_items') or []

    # update
    duplicated = False
    for c in cart_items:
        if c.get('id') == product.id:
            c['qty'] = int(c.get('qty') or '1') + 1
            duplicated = True

    # insert
    if not duplicated:
        cart_items.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'qty': 1,
        })

    # เซฟข้อมูลใน session
    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('Webapp:cart_list'))

@login_required(login_url='/login')
def cart_list(request):
    cart_items = request.session.get('cart_items') or []
    total_price = 0
    total_qty = 0

    for c in cart_items:
        total_qty = total_qty + c.get('qty')
        total_price += c.get('price') * c.get('qty')

    request.session['cart_qty'] = total_qty
    request.session['cart_total_price'] = total_price
    return render(request, 'cart.html',{
        'cart_items':cart_items,
        'total_price': total_price,
    })

@login_required(login_url='/login')
def cart_delete(request, id):
    cart_items = request.session.get('cart_items') or []
    print(cart_items)

    for i  in range(len(cart_items)):
        if cart_items[i]['id']== id:
            del cart_items[i]
            break
    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('Webapp:cart_list', kwargs={}))

def checkout(request):
    cart_items = request.session.get('cart_items') or []
    if not cart_items:
        messages.error(request, "ตะกร้าสินค้าไม่มีสินค้า!")
        return redirect('Webapp:cart_list')

    total_price = 0
    # เพิ่มการคำนวณ total ของแต่ละสินค้า
    for item in cart_items:
        item['total'] = item['price'] * item['qty']
        total_price += item['total']

    # ส่งข้อมูลไปยังเทมเพลต
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def process_payment(request):
    cart_items = request.session.get('cart_items') or []
    if not cart_items:
        messages.error(request, "ตะกร้าสินค้าไม่มีสินค้า!")
        return redirect('Webapp:cart_list')

    total_price = 0
    for item in cart_items:
        total_price += item['price'] * item['qty']

    # เพิ่มข้อมูลคำสั่งซื้อในฐานข้อมูล
    orders = []
    for item in cart_items:
        product = Product.objects.get(id=item['id'])
        order = Order.objects.create(
            product=product,
            quantity=item['qty'],
            price=item['price'],
            total=item['price'] * item['qty']
        )
        orders.append(order)
        # ลด stock ของสินค้า
        product.stock -= item['qty']
        product.save()

    # เพิ่มข้อมูลการชำระเงิน
    payment_method = request.POST.get('payment_method')
    payment = Payment.objects.create(
        order=orders[0],
        amount=total_price,
        payment_method=payment_method,
    )

    # ลบสินค้าจากตะกร้า
    request.session['cart_items'] = []

    # ส่งผู้ใช้ไปยังหน้าขอบคุณ
    return redirect('Webapp:thank_you', payment_id=payment.id)

def thank_you(request, payment_id):
    payment = Payment.objects.get(id=payment_id)  # ดึงข้อมูลการชำระเงินจากฐานข้อมูล
    return render(request, 'thank_you.html', {'payment_id': payment_id, 'payment': payment})


def generate_receipt(payment):
    # กำหนดชื่อไฟล์ PDF
    file_name = f"receipt_{payment.id}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    # สร้าง PDF
    c = canvas.Canvas(file_path, pagesize=letter)

    # โหลดฟอนต์ TH Sarabun New
    font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'THSarabunNew.ttf')

    # ตรวจสอบว่าฟอนต์มีอยู่หรือไม่
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")

    pdfmetrics.registerFont(TTFont('THSarabun', font_path))

    # ตั้งค่าฟอนต์และขนาด
    c.setFont('THSarabun', 16)

    # เขียนคำว่า "ใบเสร็จรับเงิน" ตรงกลาง
    width, height = letter
    c.drawCentredString(width / 2, 750, "ใบเสร็จ")

    # สร้างตารางข้อมูลการสั่งซื้อ
    table_top = 700
    table_left = 100
    row_height = 30
    col_widths = [200, 100, 100, 100]  # ความกว้างของแต่ละคอลัมน์
    data = [
        ("หมายเลขคำสั่งซื้อ:", str(payment.order.id)),
        ("จำนวนเงินที่ชำระ:", f"{payment.amount} บาท"),
        ("วิธีการชำระเงิน:", payment.payment_method),
        ("วันที่ชำระเงิน:", payment.payment_date.strftime('%d-%m-%Y %H:%M')),
    ]

    # เขียนข้อมูลทั่วไป
    for row_num, (label, value) in enumerate(data):
        y_position = table_top - (row_num * row_height)
        c.drawString(table_left + 5, y_position - row_height + 5, label)
        c.drawRightString(table_left + sum(col_widths) - 5, y_position - row_height + 5, value)

    # เพิ่มช่องว่างก่อนเริ่มตารางรายการสินค้า
    table_top -= (len(data) * row_height) + 20

    # ข้อมูลสินค้าในคำสั่งซื้อ (จาก order_items)
    c.drawString(table_left, table_top, "รายการสินค้า")
    table_top -= row_height  # ลดตำแหน่งสำหรับแถวถัดไป

    # หัวตารางสินค้า
    c.drawString(table_left, table_top, "สินค้า")
    c.drawString(table_left + col_widths[0], table_top, "จำนวน")
    c.drawString(table_left + col_widths[0] + col_widths[1], table_top, "ราคา")
    c.drawString(table_left + col_widths[0] + col_widths[1] + col_widths[2], table_top, "ยอดรวม")
    table_top -= row_height  # ลดตำแหน่งสำหรับแถวถัดไป

    # ดึงข้อมูลรายการสินค้าจาก order_items
    for order_item in payment.order.order_items.all():
        c.drawString(table_left, table_top, order_item.product.name)
        c.drawString(table_left + col_widths[0], table_top, str(order_item.quantity))
        c.drawRightString(table_left + col_widths[0] + col_widths[1], table_top, f"{order_item.price} บาท")
        c.drawRightString(table_left + col_widths[0] + col_widths[1] + col_widths[2], table_top, f"{order_item.total} บาท")
        table_top -= row_height  # ลดตำแหน่งสำหรับแถวถัดไป

    # บันทึกและปิด PDF
    c.save()

    # ส่งไฟล์ PDF กลับไปให้ผู้ใช้
    return file_path


def download_receipt(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    pdf_path = generate_receipt(payment)
    return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')