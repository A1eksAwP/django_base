from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from todo_app.models import TodoTask, TodoStatus, TodoList
from django.contrib.auth.models import User


def home_page(request: WSGIRequest):
    return render(request, 'home_page.html')


def todo_main(request: WSGIRequest):
    users = User.objects.all()
    task_status = 'all'
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'create':
            __create_new_task(request)
        if form_type == 'complete':
            __change_todo_status(request)
        if form_type == 'clear':
            __clear_completed(request)
        if form_type == 'destroy':
            TodoTask.objects.get(pk=request.POST.get('task_id')).delete()
    else:
        task_status = request.GET.get('status')
    all_task = TodoTask.objects.filter(todo_list__user=request.user)
    match task_status:
        case 'completed': all_task = all_task.filter(status_id=TodoStatus.COMPLETED)
        case 'active': all_task = all_task.filter(status_id=TodoStatus.NOT_COMPLETED)

    return render(request, 'todo_main.html', {
        'tasks_list': all_task.order_by('-id'),
        'filter_status': task_status,
        'users': users,
    })


def __change_todo_status(request):
    task = TodoTask.objects.get(pk=request.POST.get('task_id'))
    if task.status == TodoStatus.objects.get(pk=TodoStatus.NOT_COMPLETED):
        task.status = TodoStatus.objects.get(pk=TodoStatus.COMPLETED)
        task.complete_at = datetime.now()
    else:
        task.status = TodoStatus.objects.get(pk=TodoStatus.NOT_COMPLETED)
        task.complete_at = None
    task.save()


def __clear_completed(request):
    TodoTask.objects.filter(todo_list__user=request.user)\
        .filter(status_id=TodoStatus.COMPLETED)\
        .delete()


def __create_new_task(request):
    from_user = request.user.username
    to_user = User.objects.filter(username=request.POST.get('to_user')).first()
    todo_list = TodoList.objects.filter(user=to_user).first()
    if todo_list is None:
        todo_list = TodoList(user=request.user, date=datetime.now())
        todo_list.save()
    todo = TodoTask()
    todo.title = request.POST.get('title')
    todo.status = TodoStatus.objects.get(pk=TodoStatus.NOT_COMPLETED)
    todo.create_at = datetime.now()
    todo.text = ''
    todo.todo_list = todo_list
    todo.by_user = from_user
    todo.save()
