from django import forms
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template.defaultfilters import safe
from django.views.generic import FormView

from forms import status


_GENERIC_ERRORS_DIV = '<div class="generic-errors" data-name="__all___error"></div>'
_TOP_ERRORS_WRAPPER_DIV = '<div data-name="%s_error" class="form-error"></div>%s'
_BOTTOM_ERRORS_WRAPPER_DIV = '%s<div data-name="%s_error" class="form-error"></div>'


class AjaxFormErrorsLocation:
    TOP = 0
    BOTTOM = 1


class AjaxFormMixin:
    error_orient = AjaxFormErrorsLocation.TOP
    generic_errors = safe(_GENERIC_ERRORS_DIV)

    def __getitem__(self, name):
        item = super().__getitem__(name)

        if self.error_orient == AjaxFormErrorsLocation.TOP:
            return safe(_TOP_ERRORS_WRAPPER_DIV % (name, item))
        elif self.error_orient == AjaxFormErrorsLocation.BOTTOM:
            return safe(_BOTTOM_ERRORS_WRAPPER_DIV % (item, name))

    def __iter__(self):
        for field_tuple in self.fields.items():
            field_name, field = field_tuple
            yield (self[field_name], {
                "label": field.label,
                "help_text": field.help_text,
                "required": field.required,
                "name": field_name
            })


class AjaxForm(AjaxFormMixin, forms.Form):
    pass


class AjaxModelForm(AjaxFormMixin, forms.ModelForm):
    pass


class FormAjaxValidation(FormView):
    form = None

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        data = []
        print(form.data)

        for k, v in form._errors.items():
            text = {'desc': ', '.join(v), 'key': k}
            data.append(text)

        return JsonResponse({"errors": data}, status=status.HTTP_400_BAD_REQUEST)

    def form_valid(self, form):
        return JsonResponse({}, status=status.HTTP_200_OK)

    def get_form_class(self):
        return self.form

    def get_form_kwargs(self):
        kwargs = super(FormAjaxValidation, self).get_form_kwargs()
        cls = self.get_form_class()

        if hasattr(cls, 'get_arguments'):
            kwargs.update(cls.get_arguments(self))

        return kwargs
