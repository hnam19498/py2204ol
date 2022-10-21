from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from myapp.forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse

def register_user(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:login')
    return render(
        request = request,
        template_name = 'signup.html',
        context={
            'form': form,
        }
    )

def login_user(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
            if user:
                login(request=request, user=user)
                return redirect('myapp:pets')
            else:
                message = "Sai tài khoản hoặc mật khẩu!"
            
    return render(
        request=request,
        template_name='login.html',
        context={
            'form': form,
            'message': message,
        }
    )

def validate_username(request):
    if request.method == 'POST':
        username  = request.POST['username']
        try:
            User.objects.get(username=username)
            return JsonResponse({'message': f'Username: {username} có người sử dụng!'}, status=409)
        except User.DoesNotExist:
            return JsonResponse({'message': 'OK'}, status=200)