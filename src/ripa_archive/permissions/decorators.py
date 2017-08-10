from django.core.exceptions import PermissionDenied


def require_permissions(permissions, get_instance_functor=None):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if request.user.is_anonymous:
                raise PermissionDenied()

            instance = None

            if get_instance_functor is not None:
                instance = get_instance_functor(*args, **kwargs)

            has_perm = True

            for permission in permissions:
                if instance is not None:
                    has_perm = has_perm and instance.is_user_has_permission(request.user, permission)
                else:
                    has_perm = has_perm and request.user.group.has_permission(permission)

            if not has_perm:
                raise PermissionDenied()

            return func(request, *args, **kwargs)

        return inner

    return decorator
