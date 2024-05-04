from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# pygments stuff
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


# Models Updated below
# Product Model
class Product(models.Model):
    vendor_sku = models.CharField(max_length=23, primary_key=True)
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)

# ProductType Model
class ProductType(models.Model):
    product_type_id = models.AutoField(primary_key=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_types')

# Individual Component Models
class CPU(models.Model):
    cpu_id = models.AutoField(primary_key=True)
    vendor_sku_id = models.CharField(max_length=23)
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=800)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cooler(models.Model):
    cooler_id = models.AutoField(primary_key=True)
    vendor_sku_id = models.CharField(max_length=23)
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=800)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)

class Motherboard(models.Model):
    mb_id = models.AutoField(primary_key=True)
    vendor_sku_id = models.CharField(max_length=23)
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=800)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)

class RAM(models.Model):
    ram_id = models.AutoField(primary_key=True)
    vendor_sku_id = models.CharField(max_length=23)
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=800)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)

class GPU(models.Model):
    gpu_id = models.AutoField(primary_key=True)
    vendor_sku_id = models.CharField(max_length=23)
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=800)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    
class Storage(models.Model):
    stg_id = models.AutoField(primary_key=True)
    vendor_sku_id = models.CharField(max_length=23)
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=800)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    
class PowerSupply(models.Model):
    ps_id = models.AutoField(primary_key=True)
    vendor_sku_id = models.CharField(max_length=23)
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=800)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)

class Tower(models.Model):
    t_id = models.AutoField(primary_key=True)
    vendor_sku_id = models.CharField(max_length=23)
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=800)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)

class OperatingSystem(models.Model):
    os_id = models.AutoField(primary_key=True)
    vendor_sku_id = models.CharField(max_length=23)
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=800)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)  

class Monitor(models.Model):
    mon_id = models.AutoField(primary_key=True)
    vendor_sku_id = models.CharField(max_length=23)
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=800)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)

# System Integrator Model
class SystemIntegrator(models.Model):
    system_builder_id = models.AutoField(primary_key=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    vendor_sku_id = models.CharField(max_length=23)
    pcsys_build_price = models.DecimalField(max_digits=6, decimal_places=2)

# BuildAPC_Config Model
class BuildAPC_Config(models.Model):
    cust_build_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    system_integrator = models.ForeignKey(SystemIntegrator, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    vendor_sku_id = models.CharField(max_length=23)

# Customer Model
class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=18)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=30)

# Review Model
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_review = models.CharField(max_length=50)
    system_integrator_review = models.CharField(max_length=50)

# Customer Wishlist Model
class CustomerWishList(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

# Human Resources Model
class HumanResource(models.Model):
    employee_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city_state_zip = models.CharField(max_length=255)
    birthdate = models.DateField()
    contact_number = models.CharField(max_length=20)
    salary = models.IntegerField()
    tenure = models.IntegerField()
    role_title = models.CharField(max_length=255)
    cost_center = models.IntegerField()

  
    highlighted = models.TextField()

    class Meta:
        ordering = ["created"]

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = "table" if self.linenos else False
        options = {"title": self.title} if self.title else {}
        formatter = HtmlFormatter(
            style=self.style, linenos=linenos, full=True, **options
        )
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title} - {self.id}"
