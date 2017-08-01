def require_permissions(permissions, get_instance_functor=None):
    def decorator(func):
        def inner(request, *args, **kwargs):
            instance = None

            if get_instance_functor is not None:
                instance = get_instance_functor(*args, **kwargs)

            if instance is not None:
                pass  # TODO: implement

            func(request, *args, **kwargs)

        return inner

    return decorator
