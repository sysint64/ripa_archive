from django import forms
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
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

    @classmethod
    def prefixes_field(cls, id=None):
        field_name = cls.__name__.lower() + "_prefixes"

        if id is None:
            return "<input type='hidden' name='%s' value=''>" % field_name
        else:
            return "<input type='hidden' name='%s' id='%s' value=''>" % (field_name, id)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            if field.widget.attrs.get("class", "") == "":
                field.widget.attrs.update({"class": "form-control"})

    def __getitem__(self, name):
        item = super().__getitem__(name)
        prefix = "" if self.prefix is None else self.prefix + "-"

        if self.error_orient == AjaxFormErrorsLocation.TOP:
            return safe(_TOP_ERRORS_WRAPPER_DIV % (prefix + name, item))
        elif self.error_orient == AjaxFormErrorsLocation.BOTTOM:
            return safe(_BOTTOM_ERRORS_WRAPPER_DIV % (item, prefix + name))

    def __iter__(self):
        for field_name, field in self.fields.items():
            yield (self[field_name], {
                "label": field.label,
                "help_text": field.help_text,
                "required": field.required,
                "name": field_name,
                "hidden": isinstance(field.widget, forms.HiddenInput),
                "is_file": isinstance(field.widget, forms.FileInput)
            })

    def is_valid(self):
        try:
            return super().is_valid()
        except KeyError:
            raise SuspiciousOperation()


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


class CompositeAjaxFormValidator(View):
    forms = []
    instance_cls = None
    instance_query_field = None

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/')

    def get_errors(self, form):
        errors = []
        prefix = "" if form.prefix is None else form.prefix + "-"

        for k, v in form._errors.items():
            text = {'desc': ', '.join(v), 'key': prefix + k}
            errors.append(text)

        return errors

    def get_forms_errors(self, form_class, instance, ignore_first):
        forms = get_multi_form(form_class, self.request.POST, self.request.FILES, instance,
                               ignore_first)
        errors = []

        for form in forms:
            if not form.is_valid():
                errors += self.get_errors(form)

        return errors

    def post(self, request, *args, **kwargs):
        if self.instance_query_field is not None:
            query_kwargs = {
                self.instance_query_field: kwargs[self.instance_query_field]
            }
            instance = get_object_or_404(self.instance_cls, **query_kwargs)
        else:
            instance = None

        errors = []

        for form_class in self.forms:
            errors += self.get_forms_errors(form_class, instance, form_class != self.forms[0])

        if len(errors) == 0:
            return JsonResponse({}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
