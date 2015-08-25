import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import CustomPasswordResetForm
from django.core.urlresolvers import reverse

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def reset_form(request):

    customform=CustomPasswordResetForm
    if request.method == 'POST':
        form=customform(request.data)
        if form.is_valid():
            users=form.get_users(form.cleaned_data["email"])
            form.save(from_email="ads71993@gnail.com",request=request)
            return Response("We've e-mailed you instructions for setting your password to the e-mail address you submitted",status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)

    if request.method == "GET":
        form = customform
        context = {
        'form': form,
        'title': ('Password reset'),
        }
        return render(request, 'registration/password_reset_form.html', context)

#
# @api_view(['GET', 'POST'])
# def password_reset_confirm(request, uidb64=None, token=None,
#                            template_name='registration/password_reset_confirm.html',
#                            token_generator=default_token_generator,
#                            set_password_form=SetPasswordForm):
#
#     UserModel = get_user_model()
#     assert uidb64 is not None and token is not None  # checked by URLconf
#     post_reset_redirect = reverse('password_reset_complete')
#     try:
#         # urlsafe_base64_decode() decodes to bytestring on Python 3
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = UserModel._default_manager.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
#         user = None
#
#     if user is not None and token_generator.check_token(user, token):
#         validlink = True
#         title = ('Enter new password')
#         if request.method == 'POST':
#             form = set_password_form(user, request.POST)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect(post_reset_redirect)
#         else:
#             form = set_password_form(user)
#     else:
#         validlink = False
#         form = None
#         title = ('Password reset unsuccessful')
#     context = {
#         'form': form,
#         'title': title,
#         'validlink': validlink,
#         }
#
#     return TemplateResponse(request, template_name, context)


