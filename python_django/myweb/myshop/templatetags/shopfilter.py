from django import template
from myshop.models import Product, Promotion, Order
from django.utils import timezone

register = template.Library()

@register.filter
def check_sale(product_id):
    try:
        product_in_promotion = Promotion.objects.get(
            product_id = product_id,
            start_date__lte = timezone.now(),
            end_date__gt = timezone.now(),
        )
        return True
    except Promotion.DoesNotExist:
        return False

@register.filter
def price_sale(product_id):
    try:
        product_in_promotion = Promotion.objects.get(
            product_id = product_id,
            start_date__lte = timezone.now(), # __lt(e): nhỏ hơn hoặc (bằng)
            end_date__gt = timezone.now(), # __gt(e): lớn hơn hoặc (bằng)
        )
        return int(product_in_promotion.product.price / (1-product_in_promotion.discount/100))
    except Promotion.DoesNotExist:
        return ""


@register.filter
def price_after_discount(product_id):
    try:
        product_in_promotion = Promotion.objects.get(
            product_id = product_id,
            start_date__lte = timezone.now(), # __lt(e): nhỏ hơn hoặc (bằng)
            end_date__gt = timezone.now(), # __gt(e): lớn hơn hoặc (bằng)
        )
        return product_in_promotion.discount
    except Product.DoesNotExist:
        return ''

@register.filter
def count_product_in_cart(logged_user):
    try:
        sum_item = 0
        user_ordered = Order.objects.get(user = logged_user, status = 0) # đếm sản phẩm chưa thanh toán
        for item in user_ordered.orderdetail_set.all():
            sum_item = sum_item + item.quantity
        return sum_item
    except:
        return 0