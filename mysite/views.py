
from django.contrib.auth.forms import PasswordResetForm
from google.appengine.api import mail
import logging
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def form(request):
    authentication_classes = ()
    permission_classes = ()
    if request.method == 'POST':
        form=PasswordResetForm(request.data)
        if form.is_valid():
            form.email= request.POST['email']
            users=form.get_users(form.cleaned_data["email"])
            # form.save(from_email="ads71993@gnail.com")
            for user in users:
                message = mail.EmailMessage(sender="Example.com Support <ads71993@gmail.com>",
                            subject="Your account has been approved")

                message.to = user.email
                message.body =urlsafe_base64_encode(force_bytes(user.pk))
                message.send()
                #
                # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # 'token': token_generator.make_token(user),
            return Response(users)
        return Response("hello")
# class ResetPasswordRequestView(FormView):
#     template_name = "account/test_template.html"    #code for template is given below the view's code
#     success_url = 'test_template.html'
#     form_class = PasswordResetRequestForm
#
#     @staticmethod
#     def validate_email_address(email):
#         try:
#             validate_email(email)
#             return True
#         except ValidationError:
#             return False
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             data= form.cleaned_data["email_or_username"]
#         if self.validate_email_address(data) is True:                 #uses the method written above
#             '''
#             If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
#             '''
#             associated_users= User.objects.filter(email=data)
#             if associated_users.exists():
#                 logger.info("hello world 1")
#                 logger.info(associated_users)
#                 for user in associated_users:
#                         c = {
#                             'email': user.email,
#                             'domain': request.META['HTTP_HOST'],
#                             'site_name': 'your site',
#                             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                             'user': user,
#                             'token': default_token_generator.make_token(user),
#                             'protocol': 'http',
#                             }
#                         subject_template_name='registration/password_reset_subject.txt'
#                         # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
#                         email_template_name='registration/password_reset_email.html'
#                         # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
#                         subject = loader.render_to_string(subject_template_name, c)
#                         # Email subject *must not* contain newlines
#                         subject = ''.join(subject.splitlines())
#                         email = loader.render_to_string(email_template_name, c)
#                         send_mail(subject, email, 'ads71993@gmail.com' , [user.email], fail_silently=False)
#                 result = self.form_valid(form)
#                 messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
#                 return result
#             result = self.form_invalid(form)
#             messages.error(request, 'No user is associated with this email address')
#             return result
#         else:
#             '''
#             If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
#             '''
#             associated_users= User.objects.filter(username=data)
#             if associated_users.exists():
#                 logger.info("hello world 2")
#                 for user in associated_users:
#                     logger.info(user.email)
#                     c = {
#                         'email': user.email,
#                         'domain': 'example.com', #or your domain
#                         'site_name': 'example',
#                         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                         'user': user,
#                         'token': default_token_generator.make_token(user),
#                         'protocol': 'http',
#                         }
#                     subject_template_name='registration/password_reset_subject.txt'
#                     email_template_name='registration/password_reset_email.html'
#                     subject = loader.render_to_string(subject_template_name, c)
#                     # Email subject *must not* contain newlines
#                     subject = ''.join(subject.splitlines())
#                     email = loader.render_to_string(email_template_name, c)
#                     send_mail(subject, email, 'ads7993@gmail.co' , [user.email], fail_silently=False)
#                 result = self.form_valid(form)
#                 messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
#                 return result
#             result = self.form_invalid(form)
#             messages.error(request, 'This username does not exist in the system.')
#             return result
#         messages.error(request, 'Invalid Input')
#         return self.form_invalid(form)