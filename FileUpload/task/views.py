from django.shortcuts import render 
from django.http import HttpResponse
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from .models import File
import os

def upload_file(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return HttpResponse('No file provided')
        print(uploaded_file.name)
        print(uploaded_file.content_type)
        _, file_extension = os.path.splitext(uploaded_file.name)
        allowed_extensions = ['.pdf', '.txt', '.jpg', '.png']
        if file_extension.lower() not in allowed_extensions:
            return HttpResponse('Invalid file type')
        if uploaded_file.size > 10 * 1024 * 1024:
            return HttpResponse('File size exceeds limit')
        file_instance = File.objects.create(name=name, file=uploaded_file)
        return HttpResponse('File uploaded successfully.')
    return render(request,'upload.html')


def list_files(request):
    file = File.objects.all()
    return render(request,'list.html',{'files':file})


def download_file(request, pk):
    try:
        file_instance = File.objects.get(pk=pk)
    except File.DoesNotExist:
        return HttpResponse('File not found')
    file_path = file_instance.file.path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
