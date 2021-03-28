from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PhotoForm
from .models import Photo



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
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(
                username=input_username,
                password=input_password,
            )
            if new_user is not None:
                login(request, new_user)
                return redirect('app:users_detail', pk=new_user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

@login_required
def photos_new(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, "投稿が完了しました！")
        return redirect('app:users_detail', pk=request.user.pk)
    else:
        form = PhotoForm()
    return render(request, 'app/photos_new.html', {'form': form})