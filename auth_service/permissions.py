from rest_framework.permissions import BasePermission


class HasScopePermission(BasePermission):
    """
    Scope-based permission.

    - ADMIN: full access
    - USER: must have required scopes
    """

    message = "You do not have permission to perform this action."

    def __init__(self, required_scopes=None):
        self.required_scopes = required_scopes or []

    def has_permission(self, request, view):
        """
        Admin bypass
        """
        if getattr(request.user, "role", None) == "ADMIN":
            return True

        
        """
        Extract scopes from token
        """
        scopes = getattr(request, "auth_scopes", [])

        if not scopes:
            return False

        """
        Check required scopes
        """
        for scope in self.required_scopes:
            if scope not in scopes:
                return False

        return True
