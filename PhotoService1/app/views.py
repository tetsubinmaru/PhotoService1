from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Photo
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
    # Photoインスタンスを全件取得
    photos = Photo.objects.all().order_by('-created_at')
    # 取得したPhotoインスタンスをテンプレートに渡す
    return render(request, 'app/index.html', {'photos': photos})

def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    # userに紐づく写真一覧を取得
    photos = user.photo_set.all().order_by('-created_at')
    # Photosを追加
    return render(request, 'app/users_detail.html', {'user': user, 'photos': photos})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})