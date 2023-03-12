from rest_framework.permissions import BasePermission


class IsAuthenticatedRequired(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.method in ["PUT", "DELETE"]:
            if "changed_password" in request.path.split("/"):
                return True
            else:
                return request.user and request.user.is_authenticated
        else:
            return True
