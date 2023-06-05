from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.contrib import messages
# Create your views here.

from .models import Task
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, TemplateView 
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class HomePageView(TemplateView):
    template_name='home.html'

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('tasks')

#Register Form.
class RegisterPage(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Account created successfully!')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().get(request, *args, **kwargs)

# Display all tasks for the logged in user
class TaskList(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'task.html'
    context_object_name ='task_list'
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

# Specific Task Data and status
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'

# User create new task 
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    template_name = 'task_new.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

#Update task data
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    template_name = 'task_edit.html'
    success_url = reverse_lazy('tasks')
    fields = ['title', 'description','complete',]
    

# User delete task
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('tasks')


