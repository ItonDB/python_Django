from django.db import models

# Create your models here.
class categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    categories = models.ForeignKey(categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product/',blank=True,null=True)
    def __str__(self):
        return self.name

class Employee(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    date = models.DateField()
    age = models.IntegerField()
    status = models.CharField(max_length=20,choices=[
        ('ทำงาน','ทำงาน'),
        ('ลาออก','ลาออก')
    ], default='ทำงาน')
    income = models.IntegerField()
    address = models.TextField(blank=False,null=False)

    def __str__(self):
        return f"{self.fname} {self.lname}"

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id}"

class Payment (models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[
        ('บัตรเครดิต','บัตรเครดิต'),
        ('เงินสด','เงินสด'),
        ('โอนผ่านธนาคาร','โอนผ่านธนาคาร'),
        ('สแกน qr code','สแกน qr code')
    ])
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"