from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Task
from .permissions import IsOwner
from .serializers import TaskSerializer, RegisterSerializer


class TaskListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(created_by=request.user)

        serializer = TaskSerializer(tasks, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TaskDetailView(APIView):

    permission_classes = [IsAuthenticated, IsOwner]

    def get_task(self, pk, user):

        try:
            return Task.objects.get(
                id=pk,
                created_by=user
            )

        except Task.DoesNotExist:
            return None

    def get(self, request, pk):

        task = self.get_task(pk, request.user)

        if task is None:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(task)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        task = self.get_task(pk, request.user)

        if task is None:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(
            task,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        task = self.get_task(pk, request.user)

        if task is None:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        task = self.get_task(pk, request.user)

        if task is None:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        task.delete()

        return Response(
            {"message": "Task deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "User registered successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
        
# login page
def login_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        else:

            return render(
                request,
                "login.html",
                {
                    "error": "Invalid username or password"
                }
            )

    return render(request, "login.html")

def register_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if User.objects.filter(username=username).exists():

            return render(
                request,
                "register.html",
                {
                    "error": "Username already exists"
                }
            )

        if password != confirm_password:

            return render(
                request,
                "register.html",
                {
                    "error": "Passwords do not match"
                }
            )

        if len(password) < 8:

            return render(
                request,
                "register.html",
                {
                    "error": "Password must be at least 8 characters"
                }
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("web-login")

    return render(
        request,
        "register.html"
    )
@login_required
def dashboard(request):

    tasks = Task.objects.filter(
        created_by=request.user
    )

    context = {
        "tasks": tasks,
        "total_tasks": tasks.count(),
        "pending_tasks": tasks.filter(status="pending").count(),
        "in_progress_tasks": tasks.filter(status="in_progress").count(),
        "completed_tasks": tasks.filter(status="completed").count(),
    }

    return render(
        request,
        "dashboard.html",
        context
    )
    
@login_required
def add_task(request):

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        status_value = request.POST.get("status")
        priority = request.POST.get("priority")
        due_date = request.POST.get("due_date")

        Task.objects.create(
            title=title,
            description=description,
            status=status_value,
            priority=priority,
            due_date=due_date if due_date else None,
            created_by=request.user
        )

        return redirect("dashboard")

    return render(
        request,
        "task_form.html"
    )
    
def logout_view(request):

    logout(request)

    return redirect("web-login")        

@login_required
def edit_task(request, pk):

    try:
        task = Task.objects.get(
            id=pk,
            created_by=request.user
        )
    except Task.DoesNotExist:
        return redirect("dashboard")

    if request.method == "POST":

        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.status = request.POST.get("status")
        task.priority = request.POST.get("priority")

        due_date = request.POST.get("due_date")
        task.due_date = due_date if due_date else None

        task.save()

        return redirect("dashboard")

    return render(
        request,
        "task_form.html",
        {
            "task": task,
            "edit_mode": True
        }
    )
    
 
@login_required
def delete_task(request, pk):

    try:
        task = Task.objects.get(
            id=pk,
            created_by=request.user
        )
    except Task.DoesNotExist:
        return redirect("dashboard")

    if request.method == "POST":
        task.delete()

    return redirect("dashboard")    