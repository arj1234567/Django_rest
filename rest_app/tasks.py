from celery import shared_task
from django.utils.timezone import now
from rest_app.models import Product

@shared_task
def update_product_status():
    product = Product.objects.filter(product_validity__lte = now(),product_status = True)
    product.update(product_status = False)
    