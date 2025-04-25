from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from functools import wraps
from .models import Agent, Post, Service

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Session key for admin authentication
ADMIN_AUTH_KEY = 'custom_admin_authenticated'

# Decorator to check if user is authenticated as custom admin
def custom_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get(ADMIN_AUTH_KEY, False):
            return redirect('custom_admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Login view
def admin_login(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            request.session[ADMIN_AUTH_KEY] = True
            return redirect('custom_admin_dashboard')
        else:
            error_message = "Invalid username or password"

    return render(request, 'admin/login.html', {'error_message': error_message})

# Logout view
@custom_admin_required
def admin_logout(request):
    if ADMIN_AUTH_KEY in request.session:
        del request.session[ADMIN_AUTH_KEY]
    return redirect('custom_admin_login')

# Dashboard view
@custom_admin_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')

# Agent management
@custom_admin_required
def admin_agent(request):
    agent = Agent.objects.first()  # Assuming only one agent

    if request.method == 'POST':
        agent.name = request.POST.get('name')
        agent.email = request.POST.get('email')
        agent.phone = request.POST.get('phone')
        agent.bio = request.POST.get('bio')

        if 'profile_picture' in request.FILES:
            agent.profile_picture = request.FILES['profile_picture']

        agent.save()
        messages.success(request, 'Agent profile updated successfully')
        return redirect('custom_admin_agent')

    return render(request, 'admin/agent_edit.html', {'agent': agent})

# Posts management
@custom_admin_required
def admin_posts_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'admin/posts_list.html', {'posts': posts})

# Services management
@custom_admin_required
def admin_services_list(request):
    services = Service.objects.all()
    return render(request, 'admin/services_list.html', {'services': services})

@custom_admin_required
def admin_post_add(request):
    if request.method == 'POST':
        post = Post(
            title=request.POST.get('title'),
            description=request.POST.get('description')
        )

        if 'image' in request.FILES:
            post.image = request.FILES['image']

        post.save()
        messages.success(request, 'Post added successfully')
        return redirect('custom_admin_posts')

    return render(request, 'admin/post_form.html')

@custom_admin_required
def admin_post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.description = request.POST.get('description')

        if 'image' in request.FILES:
            post.image = request.FILES['image']

        post.save()
        messages.success(request, 'Post updated successfully')
        return redirect('custom_admin_posts')

    return render(request, 'admin/post_form.html', {'post': post})

@custom_admin_required
def admin_post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post deleted successfully')
    return redirect('custom_admin_posts')

@custom_admin_required
def admin_service_add(request):
    if request.method == 'POST':
        service = Service(
            name=request.POST.get('name'),
            icon=request.POST.get('icon'),
            description=request.POST.get('description') or None,  # Handle empty description
            order=request.POST.get('order', 0)
        )
        service.save()
        messages.success(request, 'Service added successfully')
        return redirect('custom_admin_services')

    return render(request, 'admin/service_form.html')

@custom_admin_required
def admin_service_edit(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.icon = request.POST.get('icon')
        service.description = request.POST.get('description') or None  # Handle empty description
        service.order = request.POST.get('order', service.order)
        service.save()
        messages.success(request, 'Service updated successfully')
        return redirect('custom_admin_services')

    return render(request, 'admin/service_form.html', {'service': service})

@custom_admin_required
def admin_service_delete(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    messages.success(request, 'Service deleted successfully')
    return redirect('custom_admin_services')
