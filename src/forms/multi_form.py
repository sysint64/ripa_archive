def get_multi_form(form_class, data):
    forms_prefixes = data.get("forms_prefixes", None)
    forms = [form_class(data)]

    if forms_prefixes is not None and forms_prefixes.strip() != "":
        for prefix in forms_prefixes.split(","):
            forms.append(form_class(data, prefix=prefix))

    return forms
