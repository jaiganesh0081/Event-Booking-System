from rest_framework.permissions import BasePermission,SAFE_METHODS


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
    
class AdminOnlyOrReadOnly(BasePermission):
    def has_permission(self, request, view):

        if request.method in SAFE_METHODS: #Checking that the request method in GET (safemethod)
            return request.user.is_authenticated #Checking the user is authenticated
        
        return request.user.is_authenticated and request.user.is_admin #Checking the user is authenticated and user is admin ro not 