from rest_framework.permissions import IsAdminUser


class PermissionPolicyMixin:
    def check_permissions(self, request):
        try:
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
                handler
                and self.permission_classes_per_method
                and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(handler.__name__)

        super().check_permissions(request)


class PermissionAdminOrOwner(IsAdminUser):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        if request.user.pk == int(view.kwargs.get('pk')):
            return True
        return False
