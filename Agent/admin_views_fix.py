@custom_admin_required
def admin_agent(request):
    agent = Agent.objects.first()  # Assuming only one agent
    
    if agent is None:
        # Create a new agent if none exists
        agent = Agent(
            name="Your Name",
            email="your.email@example.com",
            phone="123-456-7890",
            bio="Professional insurance agent with over 15 years of experience."
        )
        agent.save()

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
