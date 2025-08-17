from rest_framework import serializers
from .models import Task, TaskCategory, TaskComment, TaskAttachment
from users.serializers import UserSerializer
from django.utils import timezone

class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = '__all__'

class TaskCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = TaskComment
        fields = ['id', 'content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TaskAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    
    class Meta:
        model = TaskAttachment
        fields = ['id', 'file', 'filename', 'uploaded_by', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at']

class TaskSerializer(serializers.ModelSerializer):
    category = TaskCategorySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    comments = TaskCommentSerializer(many=True, read_only=True)
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    is_overdue = serializers.ReadOnlyField()
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'started_at', 'completed_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'assigned_to', 
                 'due_date', 'estimated_hours', 'tags']

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'status', 
                 'assigned_to', 'due_date', 'estimated_hours', 'actual_hours', 'tags']

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']
    
    def update(self, instance, validated_data):
        new_status = validated_data.get('status')
        
        # Update timestamps based on status changes
        if new_status == 'in_progress' and instance.status != 'in_progress':
            instance.started_at = timezone.now()
        elif new_status == 'completed' and instance.status != 'completed':
            instance.completed_at = timezone.now()
        
        instance.status = new_status
        instance.save()
        return instance

class TaskCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ['content']

class TaskAttachmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = ['file']
    
    def create(self, validated_data):
        file_obj = validated_data['file']
        validated_data['filename'] = file_obj.name
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data) 