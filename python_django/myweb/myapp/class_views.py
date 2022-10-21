from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Pet
from .forms import PetForm
from django.urls import reverse_lazy

class PetListView(ListView):
    # biến 'model' attribute định nghĩa tạo list view cho model nào
    # 1. khi dùng ListView thì phải tạo ra thuộc tính 'model' hoặc 'queryset' hoặc ghi đè phương thức get_queryset()
    # 2. template mặc định render 'tên app'/'tên class_list.html'
    #   thay thế template mặc định thì thêm biến 'template_name' = template.html

    # 3. tên context mặc định bên template là object_list
    #   thay thế tên biến bằng cách thêm biến 'context_object_name'
    model = Pet
    template_name = 'class/pets.html'
    context_object_name = 'pets'

    # Phân trang: số lượng item hiển thị trên 1 trang, những thông tin bị ẩn thì chuyển sang trang tiếp theo
    paginate_by = 5


    def get_queryset(self):
        pets = Pet.objects.all()
        search = self.request.GET.get('search')
        if search:
            pets = Pet.objects.filter(name__icontains = search)
        return pets

class PetDetailView(DetailView):
    model = Pet
    context_object_name = 'pet'
    template_name = 'class/detail.html'

class PetUpdateView(UpdateView):
    model = Pet
    context_object_name = 'pet'
    template_name = 'class/update.html'

class PetCreateView(CreateView):
    model = Pet
    # fields = "__all__"
    form_class = PetForm
    template_name = 'class/create.html'
    # cần có fields tương tự như form
    success_url = reverse_lazy('class_pets')