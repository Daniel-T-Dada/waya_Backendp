from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import Task
from .serializers import (
    TaskCreateUpdateSerializer,
    TaskReadSerializer,
    TaskStatusUpdateSerializer,
)
from .permissions import IsParentOfTask, IsChildAssignedToTask  # Import the child permission


@extend_schema(
    tags=['Tasks'],
    summary='Create a new task',
    description='Create a new task/chore for a child assigned by the parent.',
    examples=[
        OpenApiExample(
            'Create Task Example',
            value={
                'title': 'Clean your room',
                'description': 'Organize toys and make the bed',
                'reward': 5.00,
                'due_date': '2025-06-01',
                'assignedTo': '456e7890-e89b-12d3-a456-426614174001',
                'parentId': '123e4567-e89b-12d3-a456-426614174000'
            }
        )
    ],
    responses={
        201: {
            'description': 'Task created successfully',
            'content': {
                'application/json': {
                    'example': {
                        'id': '789e1234-e89b-12d3-a456-426614174002',
                        'title': 'Clean your room',
                        'description': 'Organize toys and make the bed',
                        'reward': '5.00',
                        'due_date': '2025-06-01',
                        'assignedTo': '456e7890-e89b-12d3-a456-426614174001',
                        'parentId': '123e4567-e89b-12d3-a456-426614174000',
                        'status': 'pending',
                        'created_at': '2025-05-29T10:30:00Z',
                        'completed_at': None
                    }
                }
            }
        }
    }
)
class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        parent = self.request.user
        assigned_to = serializer.validated_data['assigned_to']
        if assigned_to.parent != parent:
            raise permissions.PermissionDenied("You cannot assign chores to a child that is not yours.")
        serializer.save(parent=parent)


class TaskListView(generics.ListAPIView):
    serializer_class = TaskReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Return all chores for all children of the parent
        return Task.objects.filter(parent=user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOfTask]
    queryset = Task.objects.all()


class TaskStatusUpdateView(generics.UpdateAPIView):
    serializer_class = TaskStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

    def get_object(self):
        task = super().get_object()
        # Here you would verify the child is the one updating the status
        # For now, assuming only parents access backend API
        return task

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ChildChoreListView(generics.ListAPIView):
    serializer_class = TaskReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        child_id = self.request.query_params.get('childId')
        user = self.request.user
        if not child_id:
            return Task.objects.none()
        return Task.objects.filter(parent=user, assigned_to__id=child_id)


class ChildChoreStatusUpdateView(generics.UpdateAPIView):
    serializer_class = TaskStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsChildAssignedToTask]  # Added child permission here
    queryset = Task.objects.all()

    def get_object(self):
        task = super().get_object()
        # Enforce object-level permission check for assigned child
        self.check_object_permissions(self.request, task)
        return task
