from django import forms
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template.defaultfilters import safe
from django.views import View
from django.views.generic import FormView

from forms import status
from forms.multi_form import get_multi_form

_GENERIC_ERRORS_DIV = '<div class="generic-errors" data-name="__all___error"></div>'
_TOP_ERRORS_WRAPPER_DIV = '<div data-name="%s_error" class="form-error"></div>%s'
_BOTTOM_ERRORS_WRAPPER_DIV = '%s<div data-name="%s_error" class="form-error"></div>'


class AjaxFormErrorsLocation:
    TOP = 0
    BOTTOM = 1


class AjaxFormMixin:
    error_orient = AjaxFormErrorsLocation.TOP
    generic_errors = safe(_GENERIC_ERRORS_DIV)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (_, field) in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

    def __getitem__(self, name):
        item = super().__getitem__(name)
        prefix = "" if self.prefix is None else self.prefix + "-"

        if self.error_orient == AjaxFormErrorsLocation.TOP:
            return safe(_TOP_ERRORS_WRAPPER_DIV % (prefix + name, item))
        elif self.error_orient == AjaxFormErrorsLocation.BOTTOM:
            return safe(_BOTTOM_ERRORS_WRAPPER_DIV % (item, prefix + name))

    def __iter__(self):
        for (field_name, field) in self.fields.items():
            yield (self[field_name], {
                "label": field.label,
                "help_text": field.help_text,
                "required": field.required,
                "name": field_name,
                "hidden": isinstance(field.widget, forms.HiddenInput)
            })


class AjaxForm(AjaxFormMixin, forms.Form):
    pass


class AjaxModelForm(AjaxFormMixin, forms.ModelForm):
    pass


class FormAjaxValidator(View):
    form = None

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/')

    def get_errors(self, form):
        errors = []
        prefix = "" if form.prefix is None else form.prefix + "-"

        for k, v in form._errors.items():
            text = {'desc': ', '.join(v), 'key': prefix + k}
            errors.append(text)

        return errors

    def post(self, request, *args, **kwargs):
        forms = get_multi_form(self.form, request.POST)
        errors = []

        for form in forms:
            if not form.is_valid():
                errors += self.get_errors(form)

        if len(errors) == 0:
            return JsonResponse({}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
