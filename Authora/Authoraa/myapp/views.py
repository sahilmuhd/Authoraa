from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Post
from .forms import PostForm 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from django.conf import settings


from .models import CustomUser, Role, UserProfile, Post, Category, PostImage


# =======================
# 🏠 Home View
# =======================
def home(request):
    return render(request, 'home.html')


# =======================
# 👤 Registration View
# =======================
def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role_name = request.POST.get('role')

        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            messages.error(request, "Invalid role selected.")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                role=role
            )
            UserProfile.objects.create(user=user)
            messages.success(request, "User registered successfully.")
            return redirect('login')

    roles = Role.objects.exclude(name__iexact="admin")
    return render(request, 'register.html', {'roles': roles})


# =======================
# 🔐 Login & Logout
# =======================
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# =======================
# 📊 Dashboard by Role
# =======================
@login_required
def dashboard(request):
    role = request.user.role.name.lower()

    template_map = {
        'admin': 'dashboard/admin.html',
        'reader': 'dashboard/reader.html',
        'writer': 'dashboard/writer.html',
        'verifier': 'dashboard/verifier.html',
        'publisher': 'dashboard/publisher.html'
    }

    if role in template_map:
        return render(request, template_map[role])
    else:
        return HttpResponse("Unauthorized role", status=403)


# =======================
# 📝 Basic Post Creation
# =======================
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        categories = request.POST.get('categories')

        Post.objects.create(
            title=title,
            content=content,
            categories = categories,
        )
        return redirect('home')

    return render(request, 'writer.html')


# =======================
# 🖋️ Quill Editor Preview
# =======================
def quill_editor_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        return HttpResponse(f"<h1>Submitted Content</h1><div>{content}</div>")

    return render(request, 'writer.html')


# =======================
# ✍️ Create Article + Categories
# =======================


def create_article(request):
    data = Category.objects.all()
    return render(request,'writer.html',{'data':data})

def list_article(request):
        title = request.POST.get("title")
        content = request.POST.get("content")
        categories = request.POST.get("categories")

        queryset= Category.objects.all()
        Category.objects.create(title=title,content=content,categories=categories)

        return redirect('/article_list/')


# =======================
# ➕ Add Category
# =======================
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.get_or_create(name=name)
            return HttpResponse('<script>window.close(); window.opener.location.reload();</script>')
    return render(request, "add_category.html")


def add_category_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        if name:
            cat, created = Category.objects.get_or_create(name=name)
            return JsonResponse({'id': cat.id, 'name': cat.name})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# =======================
# 📃 Article Table View
# =======================

def submit_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_ids = request.POST.getlist("categories")
        images = request.FILES.getlist("images")  # handles multiple images

        print("Form submitted with:", title, content, category_ids)

        post = Post.objects.create(
            title=title,
            content=content,
            is_published=False
        )

        if category_ids:
            post.categories.set(category_ids)

        # Save images using PostImage model
        for img in images:
            PostImage.objects.create(post=post, image=img)

        return redirect('article_list')

    
def article_list(request):
    posts = Post.objects.all().order_by('-id')  # newest first
    return render(request, 'article_list.html', {'posts': posts})

def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('article_list') 

def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.content = request.POST.get("content")
            post.is_published = 'is_published' in request.POST
            post.save()

            # ✅ Update selected categories
            selected_categories = request.POST.getlist('categories')
            post.categories.set(selected_categories)

            # ✅ Handle multiple image uploads
            images = request.FILES.getlist('images')
            for image in images:
                PostImage.objects.create(post=post, image=image)

            return redirect('article_list')

    else:
        form = PostForm(instance=post)

    categories = Category.objects.all()
    return render(request, 'edit_post.html', {
        'form': form,
        'data': categories,
        'post': post  # pass post to show existing images if needed
    })

def delete_post_image(request, id):
    image = get_object_or_404(PostImage, id=id)
    if request.method == "POST":
        image.delete()
    return redirect(request.META.get('HTTP_REFERER', 'article_list'))



def preview_post(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'preview_post.html', {'post': post})

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_path, exist_ok=True)

        image_path = os.path.join(upload_path, image.name)
        with open(image_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        image_url = f"{settings.MEDIA_URL}uploads/{image.name}"
        return JsonResponse({'url': image_url})

    return JsonResponse({'error': 'Upload failed'}, status=400)
