from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from myapp.forms import PetForm
from myapp.models import Pet, Student
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def test_js(request):
    return render(request, "test_js.html")

def my_view(request):
    # respone = HttpResponse()
    # respone.write("<h1>Hello 1</h1>")

    if request.method == 'POST':
        request.session['username'] = request.POST['name_username']

    return render(request, "myview.html")

def welcome(request):
    response = HttpResponse()
    response.write(f"Xin chào {request.session['username']}")
    return response

def students(request):
    students = Student.objects.all()
    # response = HttpResponse()
    # response.write("<h1>Danh sách học sinh</h1>")
    # response.write("<ol>")
    # for student in students:
    #     response.write(f"<li>Name: {student.name}, Age: {student.age}</li>")

    # response.write("</ol>")
    return render(
        request = request,
        template_name = 'students.html',
        context = {
            'students': students
            # 'key' : value 
        },
    )
    # value: giá trị của biến bên python truyền vào
    # key: tên biến sẽ dùng bên trang html, biến được truyền từ view sang template html

def add_student(request):
    if request.method == 'POST':
        Student.objects.create(
            name = request.POST['name'],
            age = int(request.POST['age']),
            gender = request.POST['gender'] == "True",
            email = request.POST['email'],
            phone = request.POST['phone'],
        )
        # return HttpResponseRedirect('/myapp/students')
        return redirect('students')
    return render(
        request=request,
        template_name='add_student.html',
    )

def pets(request):
    pets = Pet.objects.all()
    search = request.GET.get('search')
    if search:
        pets = Pet.objects.filter(name__icontains = search)
    
    page_number = request.GET.get('page')
    paginator = Paginator(object_list=pets, per_page=5)
    page_obj = paginator.get_page(number=page_number)
    
    message = 'zzz' if len(pets) == 0 else ''
    return render(
        request=request,
        template_name='pets.html',
        context={
            'message': message,
            'page_obj': page_obj, # có thông tin cả page, cả pets
        },
    )

@login_required(login_url='/myapp/login')
def add_pet(request):
    form = PetForm()
    if request.method == 'POST':
        form = PetForm(request.POST)
        # Pet.objects.create(
        #     id = request.POST['pet_id'],
        #     name = request.POST['pet_name'],
        #     age = int(request.POST['pet_age']),
        #     type = request.POST['pet_type'],
        #     weight = request.POST['pet_weight'],
        #     length = request.POST['pet_length'],
        #     color = request.POST['pet_color'],
        #     vacinated = request.POST.get('pet_vacinated', False),
        #     dewormed = request.POST.get('pet_dewormed', False),
        #     sterilized = request.POST.get('pet_sterilized', False),
        # )
        # return HttpResponseRedirect('/myapp/pets')
        if form.is_valid():
            form.save()
            return redirect('pets')
        # else:
        #     print("Lỗi")

    return render(
        request=request,
        template_name='add_pet.html',
        context={
            'form': form
        }
    )

@login_required(login_url='/myapp/login')
def update_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    form = PetForm(instance = pet)
    pet_name = pet.name
    if request.method == "POST":
        # pet.age = int(request.POST['pet_age'])
        # pet.weight = request.POST['pet_weight']
        # pet.length = request.POST['pet_length']
        # pet.color = request.POST['pet_color']
        # pet.vacinated = request.POST.get('pet_vacinated', False)
        # pet.dewormed = request.POST.get('pet_dewormed', False)
        # pet.sterilized = request.POST.get('pet_sterilized', False)
        form = PetForm(request.POST, instance = pet)
        if form.is_valid():
            form.save()
        pet.save()
        return redirect('pets')

    return render(
        request=request,
        template_name='update_pet.html',
        context={
            'form': form,
            'pet_id': pet_id,
            'pet_name': pet_name,
        },
    )

@login_required(login_url='/myapp/login')
def delete_pet(request, pet_id):
    pet = Pet.objects.get(id = pet_id)
    pet.delete()
    return redirect('pets')
