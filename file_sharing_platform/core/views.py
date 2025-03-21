from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, FileUploadForm, ShareFileForm
from .models import File, SharedFile

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
    sharedfiles = SharedFile.objects.filter(shared_with = request.user)
    print(f"Logged-in user: {request.user.username}")
    print(f"Shared files for {request.user.username}: {sharedfiles}")
    return render(request,'core/dashboard.html', {'files':files, 'totalfiles':totalfiles , 'sharedfiles':sharedfiles})


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
def share_file(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)
    if request.method == 'POST':
        form = ShareFileForm(request.POST)
        if form.is_valid():
            shared_with = form.cleaned_data['shared_with']
            if shared_with == request.user:
                messages.error(request, "You cannot share a file with yourself!")
            elif SharedFile.objects.filter(file=file, shared_with=shared_with).exists():
                messages.error(request, "This file is already shared with that user!")
            else:
                shared_instance = SharedFile.objects.create(file=file, shared_with=shared_with)
                messages.success(request, f"File shared with {shared_with.username}!")
                # Debug: Print to console
                print(f"Shared {file.name} with {shared_with.username}, ID: {shared_instance.id}")
            return redirect('dashboard')
    else:
        form = ShareFileForm()
    return render(request, 'core/share.html', {'form': form, 'file': file})

@login_required(login_url='login')
def delete_file(request, file_id):
    file = get_object_or_404(File,id=file_id,user=request.user)
    if request.method == "POST":
        file.delete()
        messages.success(request, f"{file.name} is deleted")
        return redirect('dashboard')
    return render(request, "core/delete_confirm.html",{'file':file})