from django.shortcuts import render, redirect
from .models import Brand, Category, Product, Order, OrderDetail
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max
from django.utils.timezone import now
from django.http.response import JsonResponse
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def test(request):
    return render(request=request,template_name='test.html')

def index(request):
    brands = Brand.objects.all()
    products = Product.objects.all()
    categories = Category.objects.filter(category_parent__isnull=True)
    category_search = request.GET.get('category')
    brand_search = request.GET.get('brand')
    brand_display = ''
    category_display = ''
    min_price = products.aggregate(Min('price'))
    max_price = products.aggregate(Max('price'))
    if category_search:
        category_display = Category.objects.get(name = category_search)
        products = Product.objects.filter(category = category_display)
    if brand_search:
        brand_display = Brand.objects.get(name = brand_search)
        products = Product.objects.filter(brand = brand_display)
    return render(
        request=request,
        template_name='index.html',
        context={
            'categories': categories,
            'products': products,
            'brand_display': brand_display,
            'category_display': category_display,
            'brands': brands,
            'min_price': min_price['price__min'],
            'max_price': max_price['price__max'],
        },
    )

@login_required(login_url='/myshop/login')
def view_product(request, product_id):
    try:
        brands = Brand.objects.all()
        products = Product.objects.all()
        categories = Category.objects.filter(category_parent__isnull=True)
        product_data = Product.objects.get(id = product_id)
        category_search = request.GET.get('category')
        brand_search = request.GET.get('brand')
        min_price = products.aggregate(Min('price'))
        max_price = products.aggregate(Max('price'))
        brand_display = ''
        category_display = ''
        if category_search:
            category_display = Category.objects.get(name = category_search)
            products = Product.objects.filter(category = category_display)
        if brand_search:
            brand_display = Brand.objects.get(name = brand_search)
            products = Product.objects.filter(brand = brand_display)
        return render(
            request=request,
            template_name= 'product-details.html',
            context={
                'products': products,
                'product_data': product_data,
                'min_price': min_price['price__min'],
                'max_price': max_price['price__max'],
                'brand_display': brand_display,
                'category_display': category_display,
                'categories': categories,
                'brands': brands,
            }
        )
    except Product.DoesNotExist:
        return render(
            request=request,
            template_name='404.html',
        )

@login_required(login_url='/myshop/login')
def add_to_cart(request, product_id):
    try:
        logged_user = request.user

        product_data = Product.objects.get(id=product_id) # kiểm tra xem người dùng có giỏ hàng nào chưa thành công (status = 0)
        user_has_ordered = Order.objects.get(user = logged_user, status = 0)

        # người dùng có 1 order chưa thành công:
            # 1.thêm 1 sản phẩm đã có trong giỏ hàng
            # 2.thêm 1 sản phẩm chưa có trong giỏ hàng

        # 1. Người dùng  thêm sản phẩm trùng với sản phẩm có sẵn trong giỏ hàng thì số lượng tăng 1 và cập nhật lại tổng tiền      
        order = user_has_ordered # chỉ là đổi lại tên để dễ xử lý
        orderdetail = OrderDetail.objects.get(order = order, product = product_data)
        orderdetail.quantity += 1
        orderdetail.amount = orderdetail.quantity * product_data.price
        orderdetail.save()
    except Product.DoesNotExist: 
        pass

    except Order.DoesNotExist: # 2. nếu rớt vào đây thì tạo mới 1 đơn hàng
        new_order = Order.objects.create(
            user = logged_user,
            status = 0,
            create_date = now(),
            phone = '',
            address = 'Nam Định',
            total_amount = 0,
        )
        
        OrderDetail.objects.create( # order không có thông tin sản phẩm nên cần tạo thêm 1 orderdetail
            product = product_data,
            order = new_order,
            quantity = 1,
            amount = product_data.price,
        )

    except OrderDetail.DoesNotExist:
        OrderDetail.objects.create(
            product = product_data,
            order = order,
            amount = product_data.price,
            quantity = 1,
        )

    sum_item = 0
    user_ordered = Order.objects.get(user = logged_user, status = 0) # đếm sản phẩm chưa thanh toán
    for item in user_ordered.orderdetail_set.all():
        sum_item = sum_item + item.quantity

    return JsonResponse(data={'quantity': sum_item})

@login_required(login_url='/myshop/login')
def cart(request):

    orderdetail = []
    message = ''
    total = 0

    try:
        logged_user = request.user
        order = Order.objects.get(user = logged_user, status = 0)
        orderdetail = order.orderdetail_set.all()
        if len(orderdetail) == 0:
            message = 'Chưa có sản phẩm nào trong giỏ hàng!'

        else:
            for item in orderdetail:
                total += item.amount

    except :
        message = 'Chưa có sản phẩm nào trong giỏ hàng!'

    return render(
            request = request,
            template_name='cart.html',
            context={
                'orderdetails': orderdetail,
                'message': message,
                'total': total,
            }
        )

def change_quantity(request, action, product_id):
    logged_user = request.user
    product_data = Product.objects.get(id = product_id)
    order = Order.objects.get(user = logged_user, status = 0)
    orderdetail = OrderDetail.objects.get(order = order, product = product_data)
    
    if action == 'increase':
        orderdetail.quantity += 1
        orderdetail.amount = product_data.price * orderdetail.quantity
        orderdetail.save()
    
    if action == 'decrease':

        if orderdetail.quantity == 1:
            orderdetail.delete()

        else:
            orderdetail.quantity -= 1
            orderdetail.amount = product_data.price * orderdetail.quantity
            orderdetail.save()
   
    return redirect('cart')

def delete_in_cart(request, product_id):
    logged_user = request.user
    product_data = Product.objects.get(id = product_id)
    order = Order.objects.get(user = logged_user, status = 0)
    orderdetail = OrderDetail.objects.get(product = product_data, order = order)
    orderdetail.delete()
    return redirect('cart')

@login_required(login_url='/myshop/login')
def checkout(request):

    orderdetail = []
    total = 0
    total_order = 0

    logged_user = request.user
    order = Order.objects.get(user = logged_user, status = 0)
    orderdetail = order.orderdetail_set.all()

    for item in orderdetail:
        total_order += item.amount
        
    if request.method == 'POST':
        order.phone = request.POST['phone']
        order.address = request.POST['address']
        order.total_amount = total_order
        order.status = 1
        order.save()
        for od_detail in orderdetail:
            od_detail.product.stock_quantity -= od_detail.quantity
            od_detail.product.save()

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [logged_user.email]
        subject = 'Thank you for your checkout!'
        message = f'''Hi {logged_user.first_name}!
        Thanks for your checkout on my shop.
        Your total amount: {intcomma(order.total_amount)}đ
        Thank you!
            Nam's shop '''
        

        send_mail(subject, message, from_email, recipient_list)

        return redirect('index')

    return render(
        request=request,
        template_name='checkout.html',
        context={
            'orderdetails': orderdetail,
            'total': total,
        }
    )