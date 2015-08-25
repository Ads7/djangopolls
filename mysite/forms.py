from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.forms.fields import EmailField
from django.template import loader
from google.appengine.api import mail


class CustomPasswordResetForm(PasswordResetForm):
    email = EmailField(label="Email", max_length=254)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        message = mail.EmailMessage(sender=from_email,
                            subject=subject)

        message.to =to_email
        message.body =body
        message.send()
