from django.core.exceptions import PermissionDenied
from django.db import transaction


@transaction.atomic
def check_permissions(request, permissions, instance=None, use_or=False):
    if request.user.is_anonymous:
        raise PermissionDenied()

    has_perm = not use_or

    for permission in permissions:
        print(permission)
        if instance is not None:
            if use_or:
                has_perm = has_perm or instance.is_user_has_permission(request.user, permission)
            else:
                has_perm = has_perm and instance.is_user_has_permission(request.user, permission)
        else:
            if use_or:
                has_perm = has_perm or request.user.group.has_permission(permission)
            else:
                has_perm = has_perm and request.user.group.has_permission(permission)

    if not has_perm:
        raise PermissionDenied()


def require_permissions(permissions, get_instance_functor=None):
    def decorator(func):
        def inner(request, *args, **kwargs):
            instance = None

            if get_instance_functor is not None:
                instance = get_instance_functor(*args, **kwargs)

            check_permissions(request, permissions, instance)

            return func(request, *args, **kwargs)

        return inner

    return decorator


def require_at_least_one_permission(permissions, get_instance_functor=None):
    def decorator(func):
        def inner(request, *args, **kwargs):
            instance = None

            if get_instance_functor is not None:
                instance = get_instance_functor(*args, **kwargs)

            check_permissions(request, permissions, instance, use_or=True)

            return func(request, *args, **kwargs)

        return inner

    return decorator
