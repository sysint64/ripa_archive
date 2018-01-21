from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse


@login_required(login_url="accounts:login")
def chat(request):
    context = {
    }

    return TemplateResponse(template="chat/chats.html", request=request, context=context)
