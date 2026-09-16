from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    
    # Custom permission to only allow owners of an object to edit it.
    
    message = "You can only access your own student records."
    
    def has_object_permission(self, request, view, obj):
        
        return obj.created_by == request.user