from django.urls import re_path, path
from . import views, class_views, user_views
from django.contrib.auth import views as auth_views

app_name = 'myapp'

urlpatterns = [
    re_path(r"^my_view$", views.my_view, name='my_view'),
    re_path(r"^welcome$", views.welcome, name="welcome"),
    re_path(r"^students$", views.students, name="student"),
    re_path(r'^test_js$', views.test_js, name='test_js'),
    re_path(r'^add_student$', views.add_student, name='add_student'),
    re_path(r'^pets$', views.pets, name='pets'),
    re_path(r'^add_pet$', views.add_pet, name='add_pet'),
    # path('update_pet/<str:pet_id>', views.update_pet, name='update_pet'), 
    re_path(r"^update_pet/(?P<pet_id>[\w]+)$", views.update_pet, name='update_pet'),
    re_path(r"^signup$", user_views.register_user, name='signup'),
    re_path(r"^login$", user_views.login_user, name='login'),
    re_path(r"^logout$", auth_views.LogoutView.as_view(next_page='myapp:login'), name='logout'),
    re_path(r"^delete_pet/(?P<pet_id>[\w]+)$", views.delete_pet, name='delete_pet'),
    re_path(r'^class$', class_views.PetListView.as_view(), name='class_pets'),
    re_path(r'^class/view/(?P<pk>[\w]+)$', class_views.PetDetailView.as_view(), name='class_detail_pet'),
    re_path(r'^class/add$', class_views.PetCreateView.as_view(), name='class_add_pet'),
    re_path(r'^validate$', user_views.validate_username, name='validate_username'),
]