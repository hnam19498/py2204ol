from . import views, user_views
from django.urls import re_path
from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^test$', views.test, name='test'),
    re_path(r"^product/(?P<product_id>[0-9]+)$", views.view_product, name='view_product'),
    re_path(r"^add_to_cart/(?P<product_id>[0-9]+)$", views.add_to_cart, name='add_to_cart'),
    re_path(r"^delete_in_cart/(?P<product_id>[0-9]+)$", views.delete_in_cart, name='delete_in_cart'),
    re_path(r"^change_quantity/(?P<action>[a-z]+)/(?P<product_id>[0-9]+)$", views.change_quantity, name='change_quantity'),
    re_path(r"^signup$", user_views.register_user, name='signup'),
    re_path(r"^checkout$", views.checkout, name='checkout'),
    re_path(r'^validate$', user_views.validate_username, name='validate_username'),
    re_path(r"^login$", user_views.login_user, name='login'),
    re_path(r"^cart$", views.cart, name='cart'),
    re_path(r"^logout$", auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]