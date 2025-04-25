from django.shortcuts import render
from .models import Agent, Post, Service

def home(request):
    agent = Agent.objects.first()  # Assuming only one agent
    posts = Post.objects.all().order_by('-created_at')
    services = Service.objects.all()  # Get all services ordered by the order field
    context = {
        'agent': agent,
        'posts': posts,
        'services': services,
        'user': request.user  # Pass the user object to the template
    }
    return render(request, 'home.html', context)

# Post management functionality moved to Django admin panel

