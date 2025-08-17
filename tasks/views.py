from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.utils import timezone
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
import re
from .models import Task, TaskCategory, TaskComment, TaskAttachment
from .serializers import (
    TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer, TaskStatusUpdateSerializer,
    TaskCategorySerializer, TaskCommentSerializer, TaskAttachmentSerializer,
    TaskCommentCreateSerializer, TaskAttachmentCreateSerializer
)

# Django Views
@login_required
def dashboard(request):
    user = request.user
    
    # Get tasks based on user role
    if user.is_admin():
        tasks = Task.objects.all()
    elif user.is_manager():
        tasks = Task.objects.filter(
            Q(created_by=user) | Q(assigned_to=user) | Q(assigned_to__role='employee')
        )
    else:
        tasks = Task.objects.filter(
            Q(created_by=user) | Q(assigned_to=user)
        )
    
    # Dashboard statistics
    total_tasks = tasks.count()
    pending_tasks = tasks.filter(status='pending').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    completed_tasks = tasks.filter(status='completed').count()
    overdue_tasks = tasks.filter(status__in=['pending', 'in_progress', 'review']).filter(due_date__lt=timezone.now()).count()
    
    # Recent tasks with permissions
    recent_tasks = tasks.select_related('category', 'assigned_to').order_by('-created_at')[:5]
    
    # Add permission information for each task
    for task in recent_tasks:
        task.can_edit = task.can_be_edited_by(user)
        task.can_delete = task.can_be_deleted_by(user)
    
    context = {
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'recent_tasks': recent_tasks,
    }
    
    return render(request, 'tasks/dashboard.html', context)

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20
    
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.select_related('category', 'created_by', 'assigned_to')
        
        # Apply status filter if provided in query parameters
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if user.is_admin():
            return queryset
        elif user.is_manager():
            return queryset.filter(
                Q(created_by=user) | Q(assigned_to=user) | Q(assigned_to__role='employee')
            )
        else:
            return queryset.filter(
                Q(created_by=user) | Q(assigned_to=user)
            )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = TaskCategory.objects.all()
        context['statuses'] = Task.STATUS_CHOICES
        context['priorities'] = Task.PRIORITY_CHOICES
        
        # Add permission information for each task
        for task in context['tasks']:
            task.can_edit = task.can_be_edited_by(self.request.user)
            task.can_delete = task.can_be_deleted_by(self.request.user)
        
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    
    def get_queryset(self):
        return Task.objects.select_related('category', 'created_by', 'assigned_to').prefetch_related('comments__author', 'attachments__uploaded_by')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add permission information for the task
        task = self.object
        task.can_edit = task.can_be_edited_by(self.request.user)
        task.can_delete = task.can_be_deleted_by(self.request.user)
        
        return context

class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'category', 'priority', 'assigned_to', 'due_date', 'estimated_hours', 'tags']
    
    def test_func(self):
        return self.request.user.can_manage_tasks()
    
    def get_success_url(self):
        # Try to redirect back to the referring page if it's from our app
        referrer = self.request.META.get('HTTP_REFERER')
        
        if referrer:
            # Check if the referrer is from our app
            if '/dashboard/' in referrer:
                return '/'
            elif '/tasks/' in referrer:
                return '/tasks/'
        
        # Default fallback to task list
        return '/tasks/'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'category', 'priority', 'status', 'assigned_to', 'due_date', 'estimated_hours', 'actual_hours', 'tags']
    
    def test_func(self):
        task = self.get_object()
        return task.can_be_edited_by(self.request.user)
    
    def get_success_url(self):
        # Try to redirect back to the referring page if it's from our app
        referrer = self.request.META.get('HTTP_REFERER')
        if referrer:
            # Check if the referrer is from our app
            if '/dashboard/' in referrer:
                return '/'
            elif '/tasks/' in referrer:
                # Check if this is a task detail page (pattern: /tasks/123/)
                task_detail_pattern = r'/tasks/\d+/$'
                if re.search(task_detail_pattern, referrer):
                    # Coming from a task detail page - redirect back to the same task
                    return f'/tasks/{self.object.pk}/'
                # If coming from task list or other task pages, stay there
                return referrer
        
        # Default fallback to task list
        return '/tasks/'
    
    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    
    def test_func(self):
        task = self.get_object()
        return task.can_be_deleted_by(self.request.user)
    
    def get_success_url(self):
        # Try to redirect back to the referring page if it's from our app
        referrer = self.request.META.get('HTTP_REFERER')
        if referrer:
            # Check if the referrer is from our app
            if '/dashboard/' in referrer:
                return '/'
            elif '/tasks/' in referrer:
                # Check if this is a task detail page (pattern: /tasks/123/)
                task_detail_pattern = r'/tasks/\d+/$'
                if re.search(task_detail_pattern, referrer):
                    # Coming from a task detail page - redirect to task list to avoid 404
                    # NEVER redirect back to a task detail page after deletion
                    return '/tasks/'
                # If coming from task list or other task pages, stay there
                return referrer
        
        # Default fallback to task list
        return '/tasks/'
    
    def delete(self, request, *args, **kwargs):
        # Store the task ID before deletion for potential use
        task_id = self.get_object().pk
        
        # Perform the deletion
        response = super().delete(request, *args, **kwargs)
        
        # Add success message
        messages.success(request, 'Task deleted successfully!')
        
        # Force redirect to task list to avoid any 404 errors
        # This ensures we never try to redirect to a deleted task's detail page
        # The get_success_url method is bypassed to prevent redirect issues
        return redirect('tasks:task-list')

# API Views
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('category', 'created_by', 'assigned_to')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category', 'assigned_to', 'created_by']
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        if user.is_admin():
            return queryset
        elif user.is_manager():
            return queryset.filter(
                Q(created_by=user) | Q(assigned_to=user) | Q(assigned_to__role='employee')
            )
        else:
            return queryset.filter(
                Q(created_by=user) | Q(assigned_to=user)
            )
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        serializer = TaskStatusUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        tasks = self.get_queryset().filter(
            Q(created_by=request.user) | Q(assigned_to=request.user)
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        overdue_tasks = self.get_queryset().filter(
            status__in=['pending', 'in_progress', 'review'],
            due_date__lt=timezone.now()
        )
        serializer = self.get_serializer(overdue_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        tasks = self.get_queryset()
        stats = {
            'total': tasks.count(),
            'pending': tasks.filter(status='pending').count(),
            'in_progress': tasks.filter(status='in_progress').count(),
            'review': tasks.filter(status='review').count(),
            'completed': tasks.filter(status='completed').count(),
            'cancelled': tasks.filter(status='cancelled').count(),
            'overdue': tasks.filter(
                status__in=['pending', 'in_progress', 'review'],
                due_date__lt=timezone.now()
            ).count(),
        }
        return Response(stats)

class TaskCategoryViewSet(viewsets.ModelViewSet):
    queryset = TaskCategory.objects.all()
    serializer_class = TaskCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TaskComment.objects.filter(task_id=self.kwargs['task_pk'])
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCommentCreateSerializer
        return TaskCommentSerializer
    
    def perform_create(self, serializer):
        task = get_object_or_404(Task, pk=self.kwargs['task_pk'])
        serializer.save(author=self.request.user, task=task)

class TaskAttachmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAttachment.objects.all()
    serializer_class = TaskAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TaskAttachment.objects.filter(task_id=self.kwargs['task_pk'])
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TaskAttachmentCreateSerializer
        return TaskAttachmentSerializer
    
    def perform_create(self, serializer):
        task = get_object_or_404(Task, pk=self.kwargs['task_pk'])
        serializer.save(uploaded_by=self.request.user, task=task)
