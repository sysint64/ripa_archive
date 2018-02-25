import inspect


def get_multi_form(form_class, data, files=None, instance=None, ignore_first=False, get_instance=None):
    forms_prefixes = data.get(form_class.__name__.lower() + "_prefixes")
    print(data)

    if instance is not None:
        forms = [form_class(data, files, instance=instance)] if not ignore_first else []
    elif get_instance is not None:
        forms = [form_class(data, files, instance=get_instance())] if not ignore_first else []
    else:
        forms = [form_class(data, files)] if not ignore_first else []

    if forms_prefixes is not None and forms_prefixes.strip() != "":
        for prefix in forms_prefixes.split(","):
            if get_instance is not None:
                forms.append(form_class(data, files, prefix=prefix, instance=get_instance(prefix)))
            else:
                forms.append(form_class(data, files, prefix=prefix))

    return forms
