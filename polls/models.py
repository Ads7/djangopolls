import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from google.appengine.ext import ndb


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Create your models here.
class Question(ndb.Model):
    question_text =  ndb.TextProperty(max_length=200)
    pub_date = ndb.DateTimeProperty(name='date published')
    image = ndb.StringProperty()
    def __unicode__(self):
    	return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    

class Choice(ndb.Model):
    question = ndb.KeyProperty(kind=Question)
    choice_text = ndb.StringProperty(max_length=200)
    votes = ndb.IntegerProperty(default=0)

    def __unicode__(self):
    	return self.choice_text 
