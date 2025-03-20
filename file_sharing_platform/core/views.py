from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, FileUploadForm
from .models import File

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
            username= user.username
        except User.DoesNotExist:
            messages.error("Invalid Username or Password")
            return redirect("login")
        
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "core/login.html")

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    files = File.objects.filter(user=request.user)
    totalfiles = files.count()

    return render(request,'core/dashboard.html', {'files':files, 'totalfiles':totalfiles})

@login_required(login_url='login')
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instace = form.save(commit=False)
            file_instace.user = request.user
            file_instace.save()
            messages.success(request, "File uploaded successfully!")
            return redirect('dashboard')
    else:
        form = FileUploadForm()
    return render(request, 'core/upload.html', {'form': form})

@login_required(login_url='login')
def file_list(request):
    files = File.objects.all()
    return render(request, "core/file_list.html", {'files':files})

