from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from dal import autocomplete



@login_required
def index(request):
    tasks = Task.objects.filter(owner=request.user).order_by('-id')  # filter(title__contains='экл')
    return render(request, 'main/index.html', {'title': 'Main page', 'tasks': tasks})


def about(request):
    return render(request, 'main/about.html')


@login_required
def add(request):
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect('home')
        else:
            error = 'Неверные данные формы'
    form = TaskForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/add.html', context)
