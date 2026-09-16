from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from .views import (TaskListCreateView,TaskDetailView,RegisterView, register_page,login_page, dashboard, add_task,edit_task, logout_view,delete_task,)


urlpatterns = [

    path('tasks/',TaskListCreateView.as_view(),name='student-list-create'),
    path('tasks/<int:pk>/',TaskDetailView.as_view(),name='student-detail'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='token-obtain-pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token-refresh'),
    path('web/login/', login_page, name='web-login'),
    path('web/dashboard/', dashboard, name='dashboard'),
    path('web/task/add/', add_task, name='add-task'),
    path('web/logout/', logout_view, name='logout'),
    path('web/task/edit/<int:pk>/', edit_task, name='edit-task'),
    path('web/task/delete/<int:pk>/',delete_task,name='delete-task'),
    path('web/register/',register_page,name='web-register'),
]