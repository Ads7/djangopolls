import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from google.appengine.ext import ndb


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Create your models here.
class Choice(ndb.Model):
    choice_text = ndb.StringProperty()
    votes = ndb.IntegerProperty(default=0)
    def __unicode__(self):
    	return self.choice_text

class Question(ndb.Model):
    question_text =  ndb.TextProperty()
    pub_date = ndb.DateTimeProperty(auto_now_add=True)
    image = ndb.StringProperty()
    choices=ndb.StructuredProperty(Choice, repeated=True)

    def __unicode__(self):
    	return self.question_text

