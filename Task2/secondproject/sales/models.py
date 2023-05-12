from django.db import models

# Create your models here.

class SalesData(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_id = models.TextField()
    order_date = models.DateField()
    ship_date = models.DateField()
    ship_mode = models.TextField()
    customer_id = models.TextField()
    customer_name = models.TextField()
    segment = models.TextField()
    country = models.TextField()
    city = models.TextField()
    state = models.TextField()
    postal_code = models.TextField()
    region = models.TextField()
    product_id = models.TextField()
    category = models.TextField()
    sub_category = models.TextField()
    product_name = models.TextField()
    sales = models.DecimalField(max_digits=10, decimal_places=2)

