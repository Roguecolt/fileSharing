from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import File

# Create your views here.
def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
        
    else:
        form = FileUploadForm()
    
    return render(request, 'core/upload.html', {'form':form})

def file_list(request):
    files = File.objects.all()
    return render(request, "core/file_list.html", {'files':files})

