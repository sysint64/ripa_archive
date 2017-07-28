def get_multi_form(form_class, data, files=None, instance=None, ignore_first=False):
    forms_prefixes = data.get(form_class.__name__.lower() + "_prefixes")

    if instance is not None:
        forms = [form_class(data, files, instance=instance)] if not ignore_first else []
    else:
        forms = [form_class(data, files)] if not ignore_first else []

    if ignore_first:
        print(forms_prefixes)

    if forms_prefixes is not None and forms_prefixes.strip() != "":
        for prefix in forms_prefixes.split(","):
            forms.append(form_class(data, files, prefix=prefix))

    return forms
