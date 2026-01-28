from rest_framework.permissions import BasePermission

class IsUzytkownik(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.uzytkownik == request.user